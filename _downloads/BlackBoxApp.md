---
title: BlackBoxApp 数据记录仪客户端
excerpt: 面向智联电能数据记录仪的 Windows 图形界面和命令行客户端，支持设备状态查看、数据下载、配置维护、时间同步和网络日志调试
layout: single
classes: wide
order: 0
# header:
#   teaser: 
---

<!-- <p align="center">
<img width="60%" alt="BlackBoxApp 数据记录仪客户端读取数据示意" src="" />
</p> -->

BlackBoxApp 是深圳智联电能科技有限公司为工业数据记录仪配套提供的上位机客户端，用于在 Windows 电脑上连接数据记录仪，完成设备状态查询、文件列表读取、当前数据下载、历史数据下载、配置维护和现场调试等工作。

购买智联电能数据记录仪的客户可免费使用 BlackBoxApp，不额外收取软件授权费用。

<p>
  <a class="btn btn--primary" href="https://gitee.com/zlinktek/zlinktek/releases/download/Software/%E6%95%B0%E6%8D%AE%E8%AE%B0%E5%BD%95%E4%BB%AA%E5%AE%A2%E6%88%B7%E7%AB%AF-1.2.0-windows-x64.zip">免费下载 Windows 客户端</a>
  <a class="btn btn--primary" href="https://gitee.com/zlinktek/zlinktek/releases/download/Software/BlackBoxUserUpgradeApp0.1.1.zip">记录仪固机升级软件</a>
  <a class="btn btn--info" href="https://zlinktek.com/products/">查看适配产品</a>
</p>

## 适用对象

BlackBoxApp 适合已经购买或正在评估智联电能数据记录仪的工程师、测试人员和现场运维人员使用，尤其适合以下场景：

- 试验现场快速读取数据记录仪中的 CSV 文件
- 设备运行过程中下载当前正在记录的数据快照
- 批量导出历史记录文件，用于故障复盘和数据分析
- 查看设备 IP、存储容量、RTC 时间、软件版本等运行状态
- 维护设备配置文件，完成记录策略和网络参数相关调试
- 在集成测试或自动化系统中使用命令行工具完成数据拉取

## 主要功能

| 功能 | 说明 |
| --- | --- |
| 设备状态查看 | 读取设备 IP、存储空间、软件版本、网络状态、RTC 时间等信息 |
| 文件列表读取 | 查看记录仪中已经生成的 CSV 数据文件 |
| 当前数据下载 | 支持对正在记录的数据生成一致性快照后下载 |
| 历史文件下载 | 按文件名下载指定历史记录文件，适合批量归档 |
| 文件上传与删除 | 支持上传配置或辅助文件，并可删除指定设备端文件 |
| Config 编辑 | 图形界面中维护设备配置，降低现场调试门槛 |
| RTC 时间同步 | 将设备时间与本机时间同步，便于记录数据追溯 |
| 网络日志查看 | 查看设备网络日志，辅助定位连接和传输问题 |
| 设备重启 | 支持通过客户端发起设备重启请求 |

## 图形界面与命令行双模式

BlackBoxApp 同时提供图形界面客户端和命令行客户端。

图形界面客户端适合现场工程师直接操作，常用功能集中在一个窗口中，不需要记忆命令参数。连接设备后，可以刷新状态、查看文件、下载数据、编辑配置、同步时间并查看日志。

命令行客户端适合自动化脚本、测试流程和批量数据导出。常用命令示例：

```powershell
# 查看设备信息
.\tftp_cmd_client.exe -ip 192.168.0.10 --info

# 查看文件列表
.\tftp_cmd_client.exe -ip 192.168.0.10 --list

# 下载当前正在记录的数据
.\tftp_cmd_client.exe -ip 192.168.0.10 --download-active --output-dir .\data

# 下载指定历史文件
.\tftp_cmd_client.exe -ip 192.168.0.10 --download 2026-05-24.csv --output-dir .\data
```

## 传输方式

客户端默认通过以太网连接数据记录仪。小型控制与状态数据使用 TFTP/UDP 69 端口，大文件上传和下载使用 TCP 5004 高速传输通道。工具会自动选择合适的传输方式，用户通常只需要确认电脑与设备位于同一网络，并填写正确的设备 IP 地址。

默认设备 IP 为：`192.168.0.10`

如现场网络使用了交换机、路由器或防火墙，请确认电脑可以访问设备的 UDP 69 端口和 TCP 5004 端口。

## 当前版本

| 项目 | 说明 |
| --- | --- |
| 软件名称 | BlackBoxApp 数据记录仪客户端 |
| 当前版本 | v1.2.0 |
| 支持系统 | Windows |
| 下载文件 | 数据记录仪客户端-1.2.0-windows-x64.zip |
| 默认设备 IP | 192.168.0.10 |
| 控制与状态通道 | TFTP/UDP 69 |
| 大文件传输通道 | TCP 5004 |

## 适配产品

BlackBoxApp 面向智联电能数据记录仪系列产品提供配套支持。不同型号的具体功能会随设备固件和接口配置有所差异。

- [IR100 工业数据记录仪](https://zlinktek.com/products/ir100/)
- [IR200 工业级隔离数据记录仪](https://zlinktek.com/products/ir200/)
- [IR200C CANFD 数据记录仪](https://zlinktek.com/products/ir200c/)
- 其他定制型数据记录仪

## 获取方式

BlackBoxApp 可免费提供给购买智联电能数据记录仪的客户使用。当前 Windows x64 版本可直接下载：

[免费下载 BlackBoxApp 数据记录仪客户端 v1.2.0](https://gitee.com/zlinktek/zlinktek/releases/download/Software/%E6%95%B0%E6%8D%AE%E8%AE%B0%E5%BD%95%E4%BB%AA%E5%AE%A2%E6%88%B7%E7%AB%AF-1.2.0-windows-x64.zip)

- 客户购买数据记录仪后可免费使用
- 支持远程协助完成首次连接和数据读取
- 如需命令行批量导出、自动化测试接入或定制功能，可联系技术支持确认方案

如需获取用户手册、命令行接口说明或与设备固件匹配的历史版本，请通过[联系方式](https://zlinktek.com/about/)联系获取。

## 使用前准备

1. 使用网线连接电脑与数据记录仪，或接入同一局域网。
2. 将电脑网卡 IP 设置到与设备相同网段，例如 `192.168.0.x`。
3. 打开 BlackBoxApp，填写设备 IP，默认通常为 `192.168.0.10`。
4. 点击刷新设备状态，确认网络连接正常。
5. 根据需要下载当前数据、下载历史文件或维护设备配置。

## 技术支持

如果现场连接失败、文件下载速度异常、设备状态读取失败或需要接入自动化测试系统，请联系智联电能技术支持，并尽量提供以下信息：

- 数据记录仪型号和设备编号
- 设备固件版本或软件版本
- 电脑系统版本和网络配置
- 客户端报错截图或命令行输出
- 现场网络连接方式

联系邮箱：zlinktek@outlook.com  
联系方式：13032953404（仅微信）
