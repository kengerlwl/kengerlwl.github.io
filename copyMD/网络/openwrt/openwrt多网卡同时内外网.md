---
title: openwrt多网卡同时内外网
top: false
cover: false
toc: true
mathjax: true
date: 2023-06-7 15:27:31
password:
summary:
tags:
- 实验室
- 路由表
- route
categories:
- 实验室
---


# 关于esxi上的双网卡

![image-20230607170105323](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/35b2c633405925134851417309e82253/18c82d1a73aa80e23a8db2c3e380c254.png)

首先由两个网卡

然后分别新建两个交换机

![image-20230607170145633](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/35b2c633405925134851417309e82253/c26c673670225c0e0699bff3a796774e.png)



![image-20230607170201197](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/35b2c633405925134851417309e82253/84b711ae77464e99f539d8afa7d3a266.png)

然后新建两个端口组

![image-20230607170224050](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/35b2c633405925134851417309e82253/b395c8f6be551c53b8c76b9e88e8de8d.png)

虚拟机使用不同的端口组

![image-20230607170249482](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/35b2c633405925134851417309e82253/165ee8927e4f3e458d99a0f386e73c1f.png)



进入openwrt。网络设置

![image-20230607170322376](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/35b2c633405925134851417309e82253/12940517f5a6aa47035e407c526ac09a.png)

分别绑定两个网卡

得到路由表

```
root@OpenWrt:/# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         183.169.79.254  0.0.0.0         UG    0      0        0 eth1
10.10.0.0       *               255.255.0.0     U     0      0        0 br-lan
172.17.0.0      *               255.255.0.0     U     0      0        0 docker0
183.169.64.0    *               255.255.240.0   U     0      0        0 eth1

该路由表，10.10.0.0/16仅通内网
其他流量默认走外网
符合我的调配要求
```















# 添加内网作为默认网关，测试用

```
ip route add default dev br-lan via 10.10.10.10
```



# 虚拟化网卡

我在某个具有基本网络命令的docker容器里运行一下命令。

结果：宿主机上也出现了该虚拟网卡。实测该方案可行。

```
ip link add link eth1 name vth1 type macvlan
ifconfig vth1 up
```





# speedtest网速测试

```
docker run --rm robinmanuelthiel/speedtest:latest
```

终端

```
docker run -it  --rm robinmanuelthiel/speedtest:latest bash
```





