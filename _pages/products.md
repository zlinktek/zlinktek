---
title: 产品中心
layout: single
permalink: /products/
lang: zh-CN
alternate_url: /en/products/
classes: wide
sidebar: false
toc: false
---

根据使用环境、接口类型和数据量，选择适合的产品系列。

## 如何选择？

**先看环境，再看接口与数据量：**

1. **有高过载、飞行振动或落地冲击要求 → JR100**：面向飞行器、无人机及回收试验。
2. **工业现场需要多串口、高速网口或 Modbus → IR200**：根据接口、协议和记录负载选择具体配置。
3. **常规串口、低速以太网记录 → IR100**：适合基础数据记录、实验室调试和成本敏感项目。

{% include product-selection-styles.html %}

<div class="product-selection-grid">
  <section class="product-selection-card">
    <h2>IR100 系列</h2>
    <p class="product-position">入门级数据记录</p>
    <ul>
      <li>常规串口与低速以太网数据记录</li>
      <li>适用于实验室调试及常规工业现场</li>
      <li>强调简单易用与成本控制</li>
    </ul>
    <a class="btn btn--primary" href="{{ '/products/ir100/' | relative_url }}">查看 IR100 产品</a>
  </section>
  <section class="product-selection-card">
    <h2>IR200 系列</h2>
    <p class="product-position">工业级多接口记录</p>
    <ul>
      <li>覆盖多串口、高速网口及 Modbus 记录需求</li>
      <li>面向复杂工业现场与设备故障追溯</li>
      <li>按具体型号选择接口、协议和隔离配置</li>
    </ul>
    <a class="btn btn--primary" href="{{ '/products/ir200/' | relative_url }}">查看 IR200 产品</a>
  </section>
  <section class="product-selection-card">
    <h2>JR100 系列</h2>
    <p class="product-position">高过载环境数据记录</p>
    <ul>
      <li>专为飞行器、无人机及落地回收场景设计</li>
      <li>{{ site.data.catalog.jr100.models.main.shock_overload }} 抗冲击过载，适应飞行振动</li>
      <li>{{ site.data.catalog.jr100.models.main.operating_temperature }} 稳定工作，支持回收后取数</li>
    </ul>
    <a class="btn btn--primary" href="{{ '/products/jr100/' | relative_url }}">查看 JR100 产品</a>
  </section>
</div>

各系列的接口速率范围与具体配置请查看产品详情。网口连接速率不等同于实际持续记录速度，选型时需结合数据负载确认。

## 不确定如何选择？

提供 **接口类型与数量、数据速率、记录时长和使用环境**，我们协助确定系列和配置。软件、外形、存储及数据保密等特殊需求可按项目评估定制。

[联系工程师，获取选型建议]({{ '/about/' | relative_url }}){: .btn .btn--primary}
