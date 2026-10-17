# 产品共用内容：IR100 / IR200 / JR100

## 目录与语言

中文是默认语言，直接使用产品名作为文件名；英文放在 `en/` 下：

```text
content/products/
├─ ir100.json
├─ ir200.json
├─ jr100.json
└─ en/
   ├─ ir100.json
   ├─ ir200.json
   └─ jr100.json
```

中英文的图片地址共用 `_data/catalog/<产品名>.json`，仅填写一次 `src`。
英文图片说明写在英文内容源的 `image_alts`，不会重复维护图片地址。
源码文件名不带语言后缀，但官网元数据中的 `lang: zh-CN` / `lang: en` 保留，用于语言切换和 SEO。

## 日常使用

在仓库根目录双击 `generate-products.bat`。需要 Python 3，无额外 Python 包。
一次生成全部已迁移产品，成功后打开产品预览索引，可选择官网、千牛及桌面/窄屏对比；命令窗口会显示生成结果。

也可从命令行运行：

```powershell
python scripts/generate-products.py all
python scripts/generate-products.py all --check
# 也可只生成一个产品
python scripts/generate-products.py ir200
python scripts/generate-products.py ir200 --check
python scripts/generate-products.py en/ir200
python scripts/generate-products.py en/ir200 --check
```

`--check` 校验源文件、模板及生成文件是否同步，不写文件。
运行 `preview-local.bat` 也会先生成全部产品页面。预览运行期间修改共用源后，
需要重新运行生成命令，Jekyll 才能看到新的生成内容。

## 哪些文件需要编辑

| 文件 | 用途 |
| --- | --- |
| `_data/catalog/ir200.json` | 型号参数、发布状态、选型表、接法表和共用图片地址 |
| `content/products/ir200.json` | 官网元数据、产品定位、卖点、场景、方案、FAQ、清单等正文 |
| `templates/products/website.html` | 官网正文外观 |
| `templates/products/taobao.html` | 千牛详情页外观 |
| `scripts/generate-products.py` | 共用模块渲染、校验和生成逻辑 |

IR100 和 JR100 使用相同结构：`_data/catalog/ir100.json`、`_data/catalog/jr100.json`
保存型号事实和共用图片；`content/products/ir100.json`、`content/products/jr100.json`
保存内容和官网元数据。`all` 自动发现 `content/products/*.json` 和 `content/products/en/*.json`，后续新增产品无需逐一修改启动脚本。

采用 UTF-8 JSON，而非 YAML，是为了让本机已有的 Python 直接解析，无需安装额外依赖。
Jekyll 同样能读取 `_data` 下的 JSON。JSON 字符串中换行使用 `\n`，双引号使用 `\"`。

正文的模块按 `blocks` 数组顺序显示，支持：

- `heading`：二、三级标题，`id` 必须唯一。
- `paragraph`：纯文本段落。
- `list`：列表，可用 `ordered` 选择编号列表。
- `table`：正文表格，包含 `headers` 和 `rows`。
- `catalog_table`：通过 `key` 引用参数源中的表格。
- `image`：通过 `key` 引用图片；每张图只配置一个 `src` HTTPS 地址，官网与千牛共用。
- `channel_support`：官网输出联系、下载和案例链接；千牛输出平台客服说明。

段落和列表支持 `**强调**`、`[文字](https://地址)` 及站内相对链接；不支持任意 HTML，特殊字符会自动转义。
千牛正文将链接转为文字，下载、订购及联系方式模块可设置 `"channels": ["website"]`，
千牛使用平台客服说明。`channels` 省略时模块在两端共用。
参数引用写成 `{{ models.d.max_speed }}`，生成时从参数源取值。
IR100 / JR100 的单型号事实使用 `{{ models.main.isolation }}` 等引用。
型号对比与关键参数表使用相同型号数据。正文中的参数改动也应通过引用表达，
新增说明时避免重新手写同一参数；自然语言中的近义表达不会自动识别或同步。

## 生成文件

- `_products/ir200.md`：Jekyll 入口，保留 `/products/ir200/` 和英文对应链接。
- `_includes/generated/products/ir200.html`：官网正文，由 Jekyll 包含进页面。
- `exports/taobao/ir200.html`：复制到千牛详情源码编辑器的 HTML 片段。
- `exports/taobao/ir200-preview.html`：本地预览用完整 HTML 文档，不用于粘贴。
- `exports/website/ir200-preview.html`：官网正文独立预览，不含 Jekyll 主题，不替代完整站点构建检查。
- `exports/ir200-compare-mobile.html`、`exports/ir200-compare-desktop.html`：390px / 680px 两端并排预览。

IR100 / JR100 的输出路径只需把上述文件名中的 `ir200` 替换为 `ir100` / `jr100`。
`exports/index.html` 是全部产品的本地预览入口。

千牛端的对比表和参数表输出为逐项卡片，避免手机端列宽过窄；官网保留表格，窄屏在表格内部横向滚动。

生成文件不要手工修改，下一次生成会覆盖。Git 只提交内容源、参数源、模板、工具和配置；
`_products/ir100.md`、`_products/ir200.md`、`_products/jr100.md` 及对应的 `_products/en/` 生成入口、`_includes/generated/`、`exports/`（含检查截图）均已忽略。
已跟踪的生成入口从 Git 索引移除，但本地文件保留，可随时重新生成。
内容源、工具、模板和千牛导出已加入 Jekyll 排除列表。

## 从源码构建与部署

新克隆仓库后，先运行产品生成器，再运行 Jekyll。`bundle exec rake build` 和
`preview-local.bat` 已接入生成步骤。直接运行 `jekyll build/serve` 则需自行先运行生成器。

`.github/workflows/pages.yml` 定义了 GitHub Pages 源码构建：生成产品文件 → Jekyll 构建 → 上传站点产物 → 部署。
提交工作流后，需要在 GitHub 仓库 Settings → Pages → Build and deployment 中将 Source
设置为 GitHub Actions；传统“从分支发布”不会执行 Python 预生成步骤。
本地仅新增了工作流文件，没有更改远程设置，也没有提交、推送或部署。

## 迁移范围与待确认信息

本次以迁移前官网 IR200 系列正文为内容基线，保留全部章节及 9 张图片。
千牛稿用于确定深色首屏、蓝白正文、790px 最大宽度和内联样式方向。
官网较新的 IR200-H 无人机/航空物流定位继续保留。

原参数表的 IR200-H 供电同时写有“DC 5~36V”和“选型表按 DC 9~36V 标注”，
本次原样保留，未擅自选择其一；应对照规格书和交付配置确认后更新参数源。
IR200-C 的研发状态会自动生成首屏提示。

已迁移中文 IR100（12 节、5 张图）、IR200（9 张图）和 JR100（7 节、1 张图），以及这三款产品已有的英文介绍。
各自原网址和中英文关联保持不变；IR200 M/D/C 单型号页仍独立维护，未自动接管。
英文源使用原英文页面内容，不是对中文源自动翻译；修改描述时应同步维护相应语言文件。
英文输出在 `_products/en/`、`_includes/generated/products/en/`、`exports/website/en/`、`exports/taobao/en/`，
英文对比页在 `exports/en/`；`all` 与预览索引同时涵盖中英文。
IR100 的原始误码率 `10e-6` 与连续测试数据量 `10e6 字节` 原样保留，未替换成未经确认的新指标。
JR100 保留原文 2kV 隔离描述，未补写未经确认的 g 值、温度范围或振动谱。

新产品图片优先使用淘宝图片空间提供的阿里图片地址。IR200 已使用阿里图床；
IR100/JR100 本次保留原站 `pic.zlinktek.com` 的真实图片地址，尚未上传到淘宝图片空间。
拿到对应阿里图片地址后替换各自 `src` 即可；生成器不会自行编造或自动上传图片地址。
每张图片只维护 `src` 和 `alt`，
更换 `src` 后重新生成即可同时更新官网与千牛。官网缩略图也引用 `{{ images.hero.src }}`，
不重复填写主图地址。两端的图片尺寸和加载方式仍由各自排版控制。

```json
"hero": {
  "alt": "IR200 系列工业数据记录仪合照",
  "src": "https://img.alicdn.com/……图片地址……"
}
```

## 发布前检查

1. 运行生成与 `--check`。
2. 使用已有 Ruby/Jekyll 环境运行 `preview-local.bat`，检查官网桌面与窄屏页面。
3. 将片段粘贴到千牛，保存后检查平台实际桌面和手机预览；本地 HTML 预览不能证明平台保留了所有样式。
4. 检查图片、型号状态、关键参数及平台客服说明后分别发布。

没有自动登录、修改商品或发布官网。生成器只写入本地生成文件。
