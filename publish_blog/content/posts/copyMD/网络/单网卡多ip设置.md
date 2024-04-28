---
title: 单网卡多ip设置
top: false
cover: false
toc: true
mathjax: true
date: 2023-03-06 15:27:31
password:
summary:
tags:
- 实验室
- 路由表
categories:
- 实验室
---




# 我自己的设备实操

ip 网卡信息，网关192.168.0.1。子网掩码是24位。目的是获取多个ip地址

## 查看设备信息

`ip addr`

```
2: enp2s0: <BROADCAST,MULTICAST,PROMISC,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:e0:67:0d:05:bb brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.208/24 brd 192.168.0.255 scope global enp2s0
       valid_lft forever preferred_lft forever
    inet6 fdae:4172:ab77:4a06:2e0:67ff:fe0d:5bb/64 scope global dynamic mngtmpaddr noprefixroute 
       valid_lft 1739sec preferred_lft 1739sec
    inet6 fe80::2e0:67ff:fe0d:5bb/64 scope link 
       valid_lft forever preferred_lft forever
```

不难看出，我的设备网卡名字是enp2s0



## 配置设备信息

`vim /etc/network/interfaces`配置文件是这个

```
auto lo
iface lo inet loopback



auto enp2s0
iface enp2s0 inet dhcp

auto enp2s0:0
iface enp2s0:0 inet static
address 192.168.1.209
netmask  255.255.255.0
gateway  192.168.1.1

auto enp2s0:1
iface enp2s0:1 inet static
address 192.168.1.210
netmask  255.255.255.0
gateway  192.168.1.1
```



## 重启动网卡

```
sudo ifdown enp2s0 && ifup enp2s0
```



## 坑点

- 不要在服务器端设置ip绑定，否则会导致ip配置了也分配不上去
- 该方法不可照搬与Ubuntu20.04，网路配置文件不一样







## 补充，对于Ubuntu20.04的单卡多ip配置（建议这个方法，对其他版本也通用）

配置文件是`/etc/netplan/00-installer-config.yaml` (后面的yaml文件可以有别的名字)

```
# This is the network config written by 'subiquity'
network:
  version: 2
  ethernets:
    ens160:
      dhcp4: true
    ens192:
      dhcp4: true
			
			# 这里就是配置多ip
      addresses:   
        - 10.10.127.12/16
        - 10.10.127.13/16
      gateway4: 10.10.10.10
      optional: true
      nameservers:
          addresses: [114.114.114.114,8.8.8.8]
```



应用配置命令

```
netplan apply  
```













