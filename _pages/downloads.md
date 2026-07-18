---
layout: archive
permalink: /downloads/
lang: zh-CN
alternate_url: /en/downloads/
collection: downloads
entries_layout: list
classes: wide
title: 下载中心
sort_by: order
sort_order: forward
---

{% assign entries_layout = page.entries_layout | default: 'list' %}
{% assign downloads_collection = site.collections | where: 'label', page.collection | first %}
{% assign entries = downloads_collection.docs | sort: page.sort_by %}
{% if page.sort_order == 'reverse' %}
	{% assign entries = entries | reverse %}
{% endif %}
<div class="entries-{{ entries_layout }}">
	{%- for post in entries -%}
		{% unless post.lang == "en" %}
		{% include archive-single.html type=entries_layout %}
		{% endunless %}
	{%- endfor -%}
</div>
