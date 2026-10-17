"""Generate product pages using Python's standard library. Run from any directory."""
import argparse
import copy
import html
import json
from pathlib import Path
import re
from string import Template

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def resolve(value, data, depth=0):
    if depth > 20:
        raise ValueError('Circular or excessively nested content reference')
    if isinstance(value, str):
        def reference(match):
            result = data
            for key in match[1].split('.'):
                result = result[key]
            if not isinstance(result, str):
                raise ValueError('Reference must point to text: ' + match[1])
            return resolve(result, data, depth + 1)
        return re.sub(r'\{\{\s*([\w.]+)\s*\}\}', reference, value)
    if isinstance(value, list):
        return [resolve(v, data, depth) for v in value]
    if isinstance(value, dict):
        return {k: resolve(v, data, depth) for k, v in value.items()}
    return value


def text(value):
    return html.escape(str(value), quote=True)


def inline(value, channel):
    """Render only emphasis and safe links; marketplace copies omit external links."""
    parts = re.split(r'(\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*)', str(value))
    result = []
    for part in parts:
        link = re.fullmatch(r'\[([^\]]+)\]\(([^)]+)\)', part)
        if link:
            label, url = link.groups()
            if not (url.startswith(('https://', 'mailto:')) or (url.startswith('/') and not url.startswith('//'))):
                raise ValueError('Unsupported content link: ' + url)
            result.append('<a href="' + text(url) + '">' + text(label) + '</a>' if channel == 'website' else text(label))
        elif part.startswith('**') and part.endswith('**'):
            result.append('<strong>' + text(part[2:-2]) + '</strong>')
        else:
            result.append(text(part))
    return ''.join(result)


def image(asset, channel):
    url = asset['src']
    if not url.startswith('https://'):
        raise ValueError('Image must use HTTPS: ' + url)
    # Marketplace editors and local previewers may not trigger lazy image loading.
    # Avoid forwarding the preview's local URL to the external image host.
    loading = 'eager' if channel == 'taobao' else 'lazy'
    return '<img src="{}" alt="{}" style="display:block;width:100%;height:auto;margin:18px auto;border:0;" loading="{}" referrerpolicy="no-referrer">'.format(text(url), text(asset['alt']), loading)


def render_blocks(blocks, catalog, channel, language='zh-CN'):
    output = []
    for block in blocks:
        if channel not in block.get('channels', ['website', 'taobao']):
            continue
        kind = block['type']
        if kind == 'heading':
            level = block['level']
            if level not in (2, 3):
                raise ValueError('Only heading levels 2 and 3 are supported')
            output.append('<h{0} id="{1}" style="font-size:{2}px;line-height:1.4;color:#0f172a;margin:28px 0 14px;">{3}</h{0}>'.format(level, text(block['id']), 28 if level == 2 else 22, text(block['text'])))
        elif kind == 'paragraph':
            output.append('<p style="margin:12px 0;color:#334155;line-height:1.9;">' + inline(block['text'], channel) + '</p>')
        elif kind == 'list':
            tag = 'ol' if block.get('ordered') else 'ul'
            output.append('<' + tag + ' style="padding-left:24px;color:#334155;">' + ''.join('<li style="margin:8px 0;">' + inline(item, channel) + '</li>' for item in block['items']) + '</' + tag + '>')
        elif kind in ('table', 'catalog_table'):
            table = catalog['tables'][block['key']] if kind == 'catalog_table' else block
            headers, rows = table['headers'], table['rows']
            if not headers or any(len(row) != len(headers) for row in rows):
                raise ValueError('Invalid table column count')
            if channel == 'taobao':
                # Stacked cards remain readable in mobile editors without media queries.
                if kind == 'catalog_table' and block['key'] == 'specifications':
                    cards = [(headers[col], [(row[0], row[col]) for row in rows]) for col in range(1, len(headers))]
                else:
                    cards = [(row[0], list(zip(headers[1:], row[1:]))) for row in rows]
                for name, fields in cards:
                    output.append('<div style="background:white;border:1px solid #cbd5e1;border-radius:8px;padding:18px;margin:14px 0;overflow-wrap:anywhere;"><div style="color:#0369a1;font-size:21px;font-weight:800;margin-bottom:12px;">' + text(name) + '</div>' + ''.join('<p style="margin:10px 0;color:#334155;"><strong style="color:#0f172a;">' + text(label) + '：</strong>' + inline(value, channel) + '</p>' for label, value in fields) + '</div>')
                continue
            head = ''.join('<th scope="col" style="padding:12px 10px;border:1px solid #cbd5e1;background:#0f172a;color:white;text-align:left;">' + inline(cell, channel) + '</th>' for cell in headers)
            body = ''.join('<tr>' + ''.join('<td style="padding:12px 10px;border:1px solid #cbd5e1;vertical-align:top;">' + inline(cell, channel) + '</td>' for cell in row) + '</tr>' for row in rows)
            hint = 'Swipe the table horizontally to view all specifications.' if language == 'en' else '窄屏可左右滑动表格，查看完整参数。'
            output.append('<p style="font-size:14px;color:#64748b;margin:12px 0 4px;">' + hint + '</p><div role="region" aria-label="' + hint + '" tabindex="0" style="overflow-x:auto;max-width:100%;margin:16px 0;"><table style="width:100%;min-width:680px;border-collapse:collapse;font-size:16px;background:white;line-height:1.7;"><thead><tr>' + head + '</tr></thead><tbody>' + body + '</tbody></table></div>')
        elif kind == 'image':
            output.append(image(catalog['images'][block['key']], channel))
        elif kind == 'channel_support':
            if channel == 'website':
                resources = catalog.get('resources', {'downloads': '/downloads/' + catalog['id'] + '/', 'case': '/cases/'})
                output.append('<p>产品选型、项目支持和资料获取，请<a href="/about/">联系工程师</a>。参阅<a href="' + text(resources['downloads']) + '">' + text(catalog['id'].upper()) + ' 资料</a>与<a href="' + text(resources['case']) + '">应用案例</a>。</p>')
            else:
                support = 'Before ordering, contact the marketplace support team to confirm the model, interfaces, power supply, storage, and project requirements.' if language == 'en' else '下单前请通过平台客服确认型号、接口、供电、存储和项目需求，最终以当前商品配置及客服确认为准。'
                output.append('<p style="color:#334155;">' + support + '</p>')
        else:
            raise ValueError('Unknown content block: ' + kind)
    return '\n'.join(output)


def generate(product, check=False):
    if not re.fullmatch(r'(?:en/)?[a-z0-9-]+', product):
        raise ValueError('Invalid product ID')
    product_id = product.split('/')[-1]
    language = 'en' if product.startswith('en/') else 'zh-CN'
    raw = load(ROOT / '_data/catalog' / (product_id + '.json'))
    source = load(ROOT / 'content/products' / (product + '.json'))
    if raw['id'] != product_id or source['id'] != product_id:
        raise ValueError('Product IDs do not match')
    if source['website']['lang'] != language:
        raise ValueError('Content language does not match its directory: ' + product)
    for model in raw['models'].values():
        if model['status'] not in ('released', 'development'):
            raise ValueError('Invalid release status')
        if model['status'] == 'development' and not model.get('notice'):
            raise ValueError('Development model requires a notice')
    catalog = resolve(copy.deepcopy(raw), raw)
    content = resolve(source, raw)
    for key, alt in content.get('image_alts', {}).items():
        catalog['images'][key]['alt'] = alt
    ids = [b['id'] for b in content['blocks'] if b['type'] == 'heading']
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate heading IDs')
    products = {}
    for channel in ('website', 'taobao'):
        body = render_blocks(content['blocks'], catalog, channel, language)
        notices = content.get('notice', '') if language == 'en' else content.get('notice') or '；'.join(m['name'] + '：' + m['notice'] for m in catalog['models'].values() if m['status'] == 'development')
        values = dict(title=text(content['title']), subtitle=text(content['subtitle']), description=text(content['description']), notice=text(notices), hero=image(catalog['images']['hero'], channel), body=body)
        template = Template((ROOT / 'templates/products' / (channel + '.html')).read_text(encoding='utf-8'))
        rendered = template.substitute(values)
        if channel == 'website':
            products[ROOT / '_includes/generated/products' / (product + '.html')] = rendered
            products[ROOT / 'exports/website' / (product + '-preview.html')] = '<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>' + values['title'] + ' — 官网正文预览</title></head><body style="margin:0;padding:16px;font:18px Arial,Microsoft YaHei,sans-serif;background:white;"><p style="font-size:14px;color:#64748b;">官网正文预览 · 未加载 Jekyll 导航、页脚及主题样式</p>' + rendered + '</body></html>\n'
        else:
            products[ROOT / 'exports/taobao' / (product + '.html')] = rendered
            products[ROOT / 'exports/taobao' / (product + '-preview.html')] = '<!doctype html>\n<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>' + values['title'] + '</title></head><body style="margin:0;background:#e2e8f0;">' + rendered + '</body></html>\n'
    entry = '---\n' + '\n'.join(k + ': ' + json.dumps(v, ensure_ascii=False) for k, v in content['website'].items()) + '\n---\n\n{% comment %}Generated by scripts/generate-products.py. Edit content/products and _data/catalog instead.{% endcomment %}\n{% include generated/products/' + product + '.html %}\n'
    products[ROOT / '_products' / (product + '.md')] = entry
    for mode, width in [('desktop', 680), ('mobile', 390)]:
        products[ROOT / 'exports' / (product + '-compare-' + mode + '.html')] = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>IR200 两端排版对比</title></head>
<body style="margin:0;background:#e2e8f0;font:16px Arial,Microsoft YaHei,sans-serif;">
<header style="padding:16px;background:#0f172a;color:white;">IR200 两端对比 · <a style="color:#7dd3fc;" href="ir200-compare-desktop.html">桌面</a> / <a style="color:#7dd3fc;" href="ir200-compare-mobile.html">390px 窄屏</a><p style="margin:8px 0 0;font-size:14px;">左：官网生成正文（不含 Jekyll 主题）；右：千牛本地 HTML（不代表平台保存后的最终效果）。各栏可独立滚动。</p></header>
<main style="display:flex;gap:20px;padding:20px;width:max-content;">
<section><h2 style="font-size:18px;">官网正文 · WIDTHpx</h2><iframe title="官网正文" src="website/ir200-preview.html" style="width:WIDTHpx;height:780px;border:1px solid #94a3b8;background:white;"></iframe></section>
<section><h2 style="font-size:18px;">千牛详情 · WIDTHpx</h2><iframe title="千牛详情" src="taobao/ir200-preview.html" style="width:WIDTHpx;height:780px;border:1px solid #94a3b8;background:white;"></iframe></section>
</main></body></html>
'''.replace('WIDTH', str(width)).replace('ir200', product_id).replace('IR200', product_id.upper())
    if language == 'en':
        for path, value in products.items():
            value = value.replace('lang="zh-CN"', 'lang="en"').replace('官网正文预览 · 未加载 Jekyll 导航、页脚及主题样式', 'Website content preview · Jekyll theme not loaded').replace('官网正文预览', 'Website preview')
            if '-compare-' in path.name:
                value = value.replace('src="website/', 'src="../website/en/').replace('src="taobao/', 'src="../taobao/en/')
                for old, new in [('两端排版对比','Channel comparison'),('两端对比','Channel comparison'),('390px 窄屏','390px mobile'),('窄屏','Mobile'),('桌面','Desktop'),('左：官网生成正文（不含 Jekyll 主题）；右：千牛本地 HTML（不代表平台保存后的最终效果）。各栏可独立滚动。','Left: website content without the Jekyll theme. Right: marketplace HTML before platform processing. Scroll each panel independently.'),('官网正文','Website content'),('千牛详情','Marketplace detail')]:
                    value = value.replace(old, new)
            products[path] = value
    stale = []
    for path, value in products.items():
        if check:
            if not path.exists() or path.read_text(encoding='utf-8') != value:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value, encoding='utf-8', newline='\n')
            print('Generated: ' + str(path.relative_to(ROOT)))
    if stale:
        raise ValueError('Generated files need updating: ' + ', '.join(stale))
    if check:
        print('Validated sources and generated files: ' + product)


def generate_all(check=False):
    content_root = ROOT / 'content/products'
    sources = sorted(content_root.glob('*.json')) + sorted((content_root / 'en').glob('*.json'))
    if not sources:
        raise ValueError('No product sources found')
    for source in sources:
        generate(source.relative_to(content_root).with_suffix('').as_posix(), check)
    links = ''
    for source in sources:
        key = source.relative_to(content_root).with_suffix('').as_posix()
        label = source.stem.upper() + (' / English' if key.startswith('en/') else ' / 中文')
        links += '<li><strong>' + text(label) + '</strong> · <a href="' + key + '-compare-mobile.html">窄屏对比</a> · <a href="' + key + '-compare-desktop.html">桌面对比</a> · <a href="website/' + key + '-preview.html">官网正文</a> · <a href="taobao/' + key + '-preview.html">千牛详情</a></li>'
    index = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>产品预览</title><body style="max-width:900px;margin:40px auto;padding:20px;font:18px Arial,Microsoft YaHei,sans-serif;line-height:2;"><h1>产品预览</h1><p>官网正文预览不含主题；千牛本地预览需在平台保存后复核。</p><ul>' + links + '</ul></body></html>\n'
    path = ROOT / 'exports/index.html'
    if check:
        if not path.exists() or path.read_text(encoding='utf-8') != index:
            raise ValueError('Preview index needs updating')
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(index, encoding='utf-8', newline='\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('product', nargs='?', default='all', help='Product ID (ir200 or en/ir200), or all (default)')
    parser.add_argument('--check', action='store_true', help='Validate without writing files')
    args = parser.parse_args()
    try:
        if args.product == 'all':
            generate_all(args.check)
        else:
            generate(args.product, args.check)
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, 'Generation failed: ' + str(error) + '\n')
