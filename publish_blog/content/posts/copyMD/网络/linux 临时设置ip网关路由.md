---
title: linux 临时设置ip网关路由.md
top: false
cover: false
toc: true
mathjax: true
date: 2023-07-4 15:27:31
password:
summary:
tags:
- 实验室
- 静态ip
- route
categories:
- 实验室
---


# 背景

目前在配一台机器，不对劲。接入了交换机，该亮的已经亮了。驱动也确保安装好了。但是就是没有dhcp分配ip。

于是决定手动设置静态ip，先试试能不能链接交换机管理，然后试试能不能链接实验室路由。



# solution



**配置IP地址**
使用ifconfig命令：
格式：ifconfig <接口名> <ip地址> netmask <子网掩码> up
命令：`ifconfig ens33 192.168.191.138 netmask 255.255.255.0 up`
**查看ip地址**
ip地址已经修改为192.168.191.138
![在这里插入图片描述](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7350ba19c0fe09009479d4ff4f4fcffb/d7b7336e97cc0a77510139991a2013eb.png)

使用ip命令：
格式：ip addr add <ip地址>/掩码 dev <接口名>
命令：`ip addr add 192.168.191.137/24 dev ens33`
查看ip地址
新增了一个192.168.191.137的IP地址
![在这里插入图片描述](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7350ba19c0fe09009479d4ff4f4fcffb/998f1846ac0a72b8a055532dfc8fa6ad.png)
**注：以上关于IP地址的配置在重启之后会失效**

## 配置网关

临时配置，重启失效
**查看网关**
查看网关的命令有很多，route –n, ip route show等
命令：`route -n`
![在这里插入图片描述](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7350ba19c0fe09009479d4ff4f4fcffb/ec66e15b0a77c1c382beac8481f209d6.png)
**配置网关**
命令：`route add default gw 192.168.191.1`
查看网关
使用`route –n`命令可以看到新增了一个192.168.191.1的网关
![在这里插入图片描述](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7350ba19c0fe09009479d4ff4f4fcffb/48ab2498532b9d5f1c9306c85aa0e0fe.png)

**删除网关**
命令：`route del default gw 192.168.191.1`
查看网关
使用`route –n`命令可以看到192.168.191.1的网关已经被删除
![在这里插入图片描述](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7350ba19c0fe09009479d4ff4f4fcffb/6b12de69682be8bab079a225d7c109cb.png)

**注：以上关于网关的配置在重启之后会失效**

## 配置DNS

临时配置，重启失效
**查看DNS**
命令：`cat /etc/resolv.conf`
![在这里插入图片描述](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7350ba19c0fe09009479d4ff4f4fcffb/10c0dc7327c5c3e23ba8ef5bc85f98c0.png)
**配置DNS**
直接修改resolv.conf文件
命令：`vi /etc/resolv.conf`
添加

```bash
nameserver 8.8.8.8
```

**重启网络**
配置完成，使用命令`/etc/init.d/networking restart`重启网络，也可以不重启
**注意：以上关于DNS的配置在重启之后会失效**





# ref

[good md](https://blog.csdn.net/QJing_shijia/article/details/116448245)

