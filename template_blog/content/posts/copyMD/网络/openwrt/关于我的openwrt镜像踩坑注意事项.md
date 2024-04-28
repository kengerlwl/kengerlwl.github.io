---
title: 关于我的openwrt镜像踩坑注意事项
top: false
cover: false
toc: true
mathjax: true
date: 2023-09-09 15:27:31
password:
summary:
tags:
- linux
- openwrt
categories:
- 网络
---

# 背景

目前我已经把我的openwrt打包成了一个img镜像，但是在如何使用该镜像方面有一些需要注意的坑如下



# 重大踩坑事项



## 最好不要通过中间交换机中转

由于我想偷懒，于是用交换机直接冲学校的光猫上组vlan然后链接到我工位的软路由上。

然后尝试虚拟网口出来。结果是网口确实是虚拟出来了，dhcp也自动获取到了ip和网关什么的，但是很尴尬，10.1.1.1的登录页面时灵时不灵。有时候连的上，有时候连不上。困惑了很久。

尝试

- 修改esxi里的交换机配置
- 更换软路由固件版本（用最新的）
- 删除所有无关的插件，openclash。mwan
- 更换软路由
- 统统无效。



最后，尝试直连光猫，成功。

办法：不用虚拟机esxi安装软路由，选择直接按照openwrt到物理机。

## 针对多个wan设置路由表

在实践过程中，出现了一个获取了多个wan口的ip。但是不可以实际访问的情况。

其中一个现象是，多个wan口都可以ping通



# 内容



## 我做了docker的挂载目录更改

**如需还想继续扩容root。可以考虑直接从ubuntu启动，然后用正常的硬盘分区扩容思路来扩容。**

所以该镜像暂定为2gb大小。



## /根目录扩容

docker目录扩容很简单，但是根目录比较麻烦。

踩坑1： 忘记做复制操作了。

踩坑2：给的目录太小了。导致根目录直接挂满。于是我重新ubuntu启动，然后给root目录手动扩容到2.5g
```
mkdir -p /tmp/introot
mkdir -p /tmp/extroot
mount --bind / /tmp/introot
mount /dev/sda4 /tmp/extroot
tar -C /tmp/introot -cvf - . | tar -C /tmp/extroot -xf -
umount /tmp/introot
umount /tmp/extroot
```

## overlay软件包目录扩容
- 扩容到1g







## 放入了一些常用的容器

主要5个



## 修改了访问权限

让web和ssh默认可访问



## 设置了openclash

放入了常见的openclash的内核，并加入了可用的常见配置



## 含有mwan

**这是一个坑**

由于加入了mwan。在校园网需要登陆的环境内，我的流量默认走不上登录页面。这主要是指openwrt路由器的客户端走不了登录页面。但是openwrt本身是可以的。很逆天。



## 修改了dns默认配置

通过dnsmasq修改了默认配置文件，具体可以参考另一篇。



## 加入了开机自动启动的脚本

myscript



# 安装python环境

pip



# ref



## 固件下载

https://openwrt.club/dl

