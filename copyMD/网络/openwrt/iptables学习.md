---
title: iptables学习
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- openwrt
- iptable
categories:
- 网络
---

# 背景

很多地方都要用到iptables。深入学习一下



![image-20230923120614113](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/dc9807ef471018a8a65a3d4d15e27f92/aafce896aada7b5170b28fbe1fd42128.png)

例子

 **在已知链末尾添加规则（举例，拒绝某个ip的访问）**

```
iptables -t filter -A INPUT -s 59.45.175.62 -j REJECT
```

`-A` 表示Append,其后紧跟的是链的名称，表示该条规则要被添加到哪个链中。 `-s` 表示包的来源ip即source。除了指定固定的ip外，我们还可以指定ip范围，比如`59.45.175.0/24` `-j` 表示jump 也即是我们最终的动作，这里的动作是拒绝

## 介绍

iptables 是一个用于 Linux 操作系统的强大的**防火墙工具**，它用于配置和管理网络规则，以控制数据包在计算机网络上的流动。

iptables 允许系统管理员定义哪些数据包可以**进入系统、离开系统或者在系统内部传递**。它可以用于实现网络安全策略、端口转发、网络地址转换（NAT）、数据包过滤等多种网络任务。



### 结构

![image-20230923115927378](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/dc9807ef471018a8a65a3d4d15e27f92/4e0d1e7a8556d67c4c4df7e888ad8d15.png)

。iptables 的主要组成结构包括：

1. 表格（Tables）：iptables 规则被组织成不同的表格，每个表格用于不同类型的操作。常见的表格有三个：
   - **filter 表格**：用于数据包过滤，控制哪些数据包可以通过系统，哪些需要被丢弃或拒绝。
   - **nat 表格**：用于配置网络地址转换（NAT）规则，允许将内部网络的地址映射到外部网络。
   - **mangle 表格**：用于修改数据包的头部信息，如修改 TTL（Time To Live）等。
   - **raw**：这里面的链条，规则，能基于数据包的状态进行规则设定
2. 链（Chains）：每个**表格包含多个链**，链是规则集合的容器，用于分类不同类型的规则。常见的链包括：
   - **INPUT 链**：处理**传入系统的数据包**。
   - **OUTPUT 链**：处理由系统生成的数据包，即**从系统出发的数据包**。
   - **FORWARD 链**：处理**经过系统的数据包**，即既不是传入也不是输出的数据包。
   - 其他自定义链：可以根据需要创建自定义链，以实现特定的功能或策略。



**具体的表与链的结构如下**

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/dc9807ef471018a8a65a3d4d15e27f92/2a8d3d0aa0d83dab2f9093940b20e8b0.png)

​			**mangle表中的链有：**

```text
PREROUTING：包在到达网口时，进行规则匹配 （一般是最先执行的）
INPUT：含义同filter
FORWARD: 含义同filter
OUTPUT: 含义同filter
POSTROUTING: 包离开网口的时候匹配
```

​			**注意，虽然不同的表中有同名的链，但他们并不是同一个链，并且一个链只能引用同一个表中的链，不能跨表引用。**



**总之无外乎两种走向**

- 本机发出的包：本机进程 -> OUTPUT 链 -> 路由选择 -> POSTROUTING 链 -> 出口网卡
- 本机收到的包：入口网卡 -> PREROUTING 链 -> 路由选择 -> 此时有两种可能的情况：
  - 目的地址为本机：INPUT 链 -> 本机进程
  - 目的地址不为本机：FORWARD 链 -> POSTROUTING 链 -> 网卡出口（内核允许网卡转发的情况下）

3. 规则（Rules）：**规则是具体定义了数据包匹配条件和操作的部分**。每个规则由若干匹配条件和一个或多个操作组成。匹配条件用于决定哪些数据包适用于这条规则，而操作则指定了对匹配的数据包应该执行什么操作。

​		例如，一条规则可以指定匹配来自特定源 IP 地址的数据包，并要求将这些数据包丢弃或重定向到另一个端口。

4. 目标（Target）：目标是规则的一部分，它指定了当数据包**匹配规则时应该采取的操作**。常见的目标包括：

- **ACCEPT**：允许数据包通过。
- **DROP**：丢弃数据包，不响应。
- **REJECT**：拒绝数据包，并向发送端发送拒绝消息。
- **DNAT**：目标地址转换，用于端口转发和 NAT 操作。
- **SNAT**：源地址转换，也用于 NAT 操作。

i**ptables 规则的执行顺序非常重要，通常规则会按照添加的顺序逐一匹配，当匹配到第一条规则后，就会执行该规则对应的操作，不再继续匹配后续规则。**



# 网络流量原理

## **规则表之间的优先顺序：**

**Raw——mangle——nat——filter**

规则链之间的优先顺序（分三种情况）：

**第一种情况：入站数据流向**

从外界到达防火墙的数据包，先被PREROUTING规则链处理（是否修改数据包地址等），之后会进行路由选择（判断该数据包应该发往何处），**如果数据包 的目标主机是防火墙本机（比如说Internet用户访问防火墙主机中的web服务器的数据包），那么内核将其传给INPUT链进行处理**（决定是否允许通 过等），通过以后再交给系统上层的应用程序（比如Apache服务器）进行响应。

**第二冲情况：转发数据流向**

来自外界的数据包到达防火墙后，首先被PREROUTING规则链处理，之后会进行路由选择，**如果数据包的目标地址是其它外部地址（比如局域网用户通过网 关访问QQ站点的数据包），则内核将其传递给FORWARD链进行处理（是否转发或拦截），然后再交给POSTROUTING规则链（**是否修改数据包的地 址等）进行处理。

**第三种情况：出站数据流向**

**防火墙本机向外部地址发送的数据包**（**比如在防火墙主机中测试公网DNS服务器时**），首先被OUTPUT规则链处理，之后进行路由选择，然后传递给POSTROUTING规则链（是否修改数据包的地址等）进行处理。

# ref

[OpenWRT/Linux多WAN带宽叠加使用iptables标记策略路由负载均衡](https://www.haiyun.me/archives/iptables-nth-mark-route-load.html)

[超级详细的iptable教程文档](https://www.cnblogs.com/Dicky-Zhang/p/5904429.html)

[Linux 的封包过滤软件： iptables](http://cn.linux.vbird.org/linux_server/0250simple_firewall_3.php#netfilter)
