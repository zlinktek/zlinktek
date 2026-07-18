---
title: "应用案例"
permalink: /cases/
lang: zh-CN
alternate_url: /en/cases/
layout: archive
collection: cases
entries_layout: list
classes: wide
sort_by: order
sort_order: forward
---

{% assign entries = site.cases | sort: page.sort_by %}
<div class="entries-list">
  {% for post in entries %}
    {% unless post.lang == "en" %}
      {% include archive-single.html type="list" %}
    {% endunless %}
  {% endfor %}
</div>
