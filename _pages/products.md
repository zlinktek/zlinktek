---
title: 产品中心
layout: archive
permalink: /products/
collection: products
entries_layout: grid
classes: wide
sort_by: order
sort_order: forward
---

{% assign entries_layout = page.entries_layout | default: 'grid' %}
<div class="entries-{{ entries_layout }}">
	{% include documents-collection.html collection=page.collection sort_by=page.sort_by sort_order=page.sort_order type=entries_layout %}
</div>

<div style="clear: both;"></div>

## 产品选型表

| 产品型号 | 主要定位 | 典型接口 / 协议 | 核心能力 | 推荐场景 |
| --- | --- | --- | --- | --- |
| [IR100](/products/ir100/) | 通用工业数据记录仪 | RS422、RS485、RS232、TTL、以太网 | 多接口透明记录、TF 卡存储、TFTP 取数 | 常规工业现场、实验室调试、小批量试制 |
| [IR200](/products/ir200/) | 工业隔离加强款 | 以太网、RS422 / RS485、TTL | 全接口隔离、宽压供电、宽温运行、防浪涌防静电 | 干扰较强、电气环境复杂、可靠性要求更高的现场 |
| [IR200M](/products/ir200m/) | Modbus 数据记录仪 | Modbus TCP | PLC 寄存器周期采集、CSV 工程化记录、TFTP 取数 | PLC 运行数据留痕、设备故障追溯、售后远程诊断 |
| [IR200D](/products/ir200d/) | 双网口数据记录仪 | 双以太网口，协议按项目配置 | 串接部署、多设备集中监控、本地存储、网络取数 | 100 套记录仪集中管理、产线联调、现场调试保留链路 |
| [IR200C](/products/ir200c/) | CANFD 数据记录仪 | CAN / CANFD | 总线报文记录、时间戳留痕、网络取数 | BMS、电机控制器、车辆设备、机器人、测试台架 |
| [CR100](/products/cr100/) | 高保密数据记录仪 | 多接口，可按项目定制 | 数据加密、软件自毁、硬件自毁选项 | 敏感任务、野外部署、设备可能丢失但数据不能泄露 |
| [JR100](/products/jr100/) | 抗高过载数据记录仪 | 以太网、RS422 / RS485 等 | 抗高过载、抗振动冲击、宽温、隔离防护 | 航天飞行试验、无人机、弹载/车载强冲击环境 |
