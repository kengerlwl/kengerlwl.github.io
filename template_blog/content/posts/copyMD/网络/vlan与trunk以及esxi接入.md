---
title: v2ray使用基本，校园网代理frp
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- v2ray
- 代理
categories:
- 代理
---

# 背景需求介绍

有一个机器，要通过一个网口，同时在vlan1和2。





# solution

- 将该端口设置为trunk
- 将该端口在交换机上加入两个vlan
- 在esxi上新建不同的端口组，并指定vlan id

![image-20230622215847377](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cbbb7644e3da38099708c7ef6845178b/aa445631645c9b0d948ac904ce1e790d.png)



**ESXI 标准 vSwitch 支持自定义 VLAN ID，以实现网络隔离！**
根据 VLAN ID 的不同，可分为三种网络：

- VLAN ID `0` **阻止**任何携带了 VLAN tag 的数据包
- VLAN ID `4095` **允许**通过携带任何 VLAN tag 的数据包（trunk）
- VLAN ID `1~4094` **仅允许**携带指定 VLAN ID tag 的数据包





# ref

[tplink 官方的案例](https://smb.tp-link.com.cn/service/detail_article_134.html)

[ESXI 虚拟交换机配置 Trunk 端口组](https://blog.csdn.net/shida_csdn/article/details/93899127)
