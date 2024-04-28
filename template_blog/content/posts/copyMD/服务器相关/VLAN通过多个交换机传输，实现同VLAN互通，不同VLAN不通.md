---
title: VLAN通过多个交换机传输，实现同VLAN互通，不同VLAN不通 
top: false
cover: false
toc: true
mathjax: true
date: 2023-06-05 15:27:31
password:
summary:
tags:
- 服务器
- linux
- 组网
categories:
- 服务器
---


# 说明

网络拓扑图：

![VLAN通过多个交换机传输，实现同VLAN互通，不同VLAN不通_运用](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/27585c10df88135ff438aec38b8370e5/18366101eb0c1a747752dcb59c9d34fe.png)

**思路：LSW1~3每个交换机都创建了两个VLAN，所以交换机连接交换的那个端口应该设置trunk端口，连接PC机的两个端口类型都设置为access。**
**vlan数据经过LSW4时，LSW4里没有配置vlan 2和vlan 3 ，所以LSW4无法识别VLAN数据的目标MAC。所以LSW4上应该也要创建VLAN 2和VLAN 3，**
**但是不需要添加端口到VLAN里。LSW4的三个端口都是连接的trunk接口，所以为了允许vlan 2和vlan 3的数据能通过LSW4，LSW4的三个端口也应该全部设置为trunk端口。**

1）配置PC机IP地址PC1~PC6一次设置IP地址为：192.168.1.1~6，子网掩码统一为：255.255.255.0
标识每台主机的IP地址

2）配置LSW1~3的VLAN端口以及TRUNK接口，命令如下：
system-view //进入系统视图
vlan batch 2 3 //创建vlan 2，vlan 3
interface GigaibitEthernet 0/0/1 //进入端口 GE 0/0/1
port link-type access //配置端口类型为access
port default vlan 2 //将端口添加到vlan 2中
interface GigabitEthernet 0/0/2 //进入端口GE 0/0/2
port link-type access //配置端口类型为access
port default vlan 3 //将端口添加到vlan 3中
interface GigabitEthernet 0/0/3 //进入端口GE 0/0/3
port link-type trunk //配置端口类型为trunk
port trunk allow-pass vlan all //配置端口允许通过所有vlan
按照以上命令，依次配置LSW1~3,并标识出VLAN和TRUNK

3)在LSW上创建VLAN 2,VLAN 3，并将设备上的GE 0/0/1~3都设置为trunk端口。命令如下：
system-view //进入系统视图
vlan batch 2 3 //创建vlan 2，vlan 3
interface GigabitEthernet 0/0/1 //进入端口GE 0/0/1
port link-type trunk //配置端口类型为trunk
port trunk allow-pass vlan all //配置端口允许通过所有vlan
interface GigabitEthernet 0/0/1 //进入端口GE 0/0/2
port link-type trunk //配置端口类型为trunk
port trunk allow-pass vlan all //配置端口允许通过所有vlan
interface GigabitEthernet 0/0/1 //进入端口GE 0/0/3
port link-type trunk //配置端口类型为trunk
port trunk allow-pass vlan all //配置端口允许通过所有vlan
标识trunk端口
