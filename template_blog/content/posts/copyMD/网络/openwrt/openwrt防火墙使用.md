---
title: openwrt防火墙使用
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- 服务器
- linux
- openwrt
categories:
- 服务器
---
# 防火墙



## linux防火墙组成

iptables：用户空间工具

netfilter：内核里的工具









## iptables

**主要用来配置防火墙规则**

关键是几个概念

入站，出站，转发



### 四表五链

![这里写图片描述](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/677e020a01cbbf8630aa5c684df44ad4/9b4049c74857bf1f98e3e95864babb59.png)



1. **表（Tables）**：`iptables` 使用不同的表来组织和存储不同类型的规则。常见的表包括：
   - **filter 表**：用于过滤网络数据包，允许或拒绝它们通过系统。这是最常用的表。
   - **nat 表**：用于网络地址转换（Network Address Translation），允许将内部网络的私有IP地址映射到外部网络的公共IP地址。
   - **mangle 表**：用于修改数据包的头部信息，如TTL（生存时间）等。
   - **raw 表**：用于配置连接跟踪规则，通常用于配置一些特殊的连接跟踪规则。
2. **链（Chains）**：每个表包含多个链，这些链是规则的集合点。常见的链包括：
   - **INPUT 链**：用于处理进入系统的数据包。
   - **OUTPUT 链**：用于处理从系统出去的数据包。
   - **FORWARD 链**：用于处理通过系统的数据包，但不是目的地或来源于系统的数据包（通常用于路由转发）。
   - 其他用户自定义的链：可以根据需要创建其他链，以实现特定的过滤和操作。



###  **规则（Rules）**
规则是定义在链中的，它们**决定了如何处理传入或传出的数据包**。规则由匹配条件和动作组成。当**数据包与规则中的匹配条件匹配时，将执行指定的动**作。常见的动作包括接受（ACCEPT）、拒绝（DROP）或重定向（REDIRECT）等。



开放指定tcp端口

```
iptables -A INPUT -p tcp --dport 52333 -j ACCEPT
```

开放所有链接端口：允许已经建立或相关的连接的数据包从系统的输出链。一定程度上，就是all开放 

```
 iptables -A OUTPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```

**注意：修改规则后，要重启防火墙才生效**

```
/etc/init.d/firewall restart

# 存储目前的规则
iptables-save > rules.v4  # IPv4 规则
# 加载目前的规则
iptables-restore < rules.v4  # IPv4 规则

```



### **匹配条件（Matching Criteria）**
规则中的匹配条件用于确定何时应用规则的动作。匹配条件可以基于源IP地址、目标IP地址、端口号、协议类型等。



## ref

https://www.right.com.cn/forum/forum.php?mod=viewthread&tid=4982313&highlight=%B7%C0%BB%F0%C7%BD


万字讲解OpenWrt防火墙iptables，并使用UCI配置防火墙 原创
https://blog.51cto.com/u_15346415/3694634