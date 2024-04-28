---
title: zerotier组网.md
top: false
cover: false
toc: true
mathjax: true
date: 2023-06-20 15:27:31
password:
summary:
tags:
- zerotier
- 路由表
- route
categories:
- 网络
---





# 需求

我再实验室和宿舍各有一套网络。

由于没有足够的公网ip带宽，所以导致我访问者两个服务通常会很痛苦。

zerotier的方案就不错：

在全球有一个大的服务器，用来记录这些小的组网，然后针对每个网络，比如我的实验室PC和宿舍PC。都在学校内，那肯定在一个大的局域网里面，那么zerotier服务器就会逐层的探查是否可以在学校这层就直接建立这两台机器的P2P连接。如果是我的手机流量连接，那么可能不在学校的同一个交换机上，可以选择继续往上一层级中继。

zerotier也可以选择自己建立中继服务器，但是由于我的服务器带宽较低，所以不考虑。





# 实操

### 服务器端配置

设置网段和路由

![image-20230620234524500](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/899a82b23714fc31a927eb619c6ba0f8/007f4cfec5c224bf911f48ed2a322ada.png)

### 设置ip分配

可以针对每个设备分配不同的ip，**前面的复选框要选中，才能分配出ip**。这得当一个设备尝试接入该网络时才会有这个情况，复选后重新运行zerotier

![image-20230620234557239](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/899a82b23714fc31a927eb619c6ba0f8/f0f95eae659a34f6c6521fd3788b6368.png)



# 坑

## 1 单方面ping通

可能会出现一方能ping通，一方不能ping通的情况。这种时候。建议检查路由表。可能服务器上显示该设备上线了，但是你去改设备查看路由表以及ip分配，其实是不对的。**建议重启zerotier服务。**

**每当网络环境改变，换了个wifi，走动了一段距离。导致连不上，都重启一下zerotier看看**



### 2 docker使用

docker使用注意清理缓存，有些目录建议不挂载。每次重新分配也无所谓



### 3 truenas

truenas由于使用经验不多，truenas对网络管理极其严格，不能命令行使用docker上网。要么做很多修改才能使用一个阉割版的docker。不如直接只用truenas官方提供的。

如果nas访问不了其他端口解决办法：

Add Routes，Destination填写局域网网段，Via填写zerotier给NAS分配的虚拟IP，建立连接后使用局域网中的NAS IP+端口访问。补充，如果应用开启host网络就可以直接使用虚拟IP+端口访问。(评论区看见的)

# 结论

- linux使用docker这套是完全可行的
- 





# ref

[truenas换源与开启zerotier](https://www.bilibili.com/video/BV1GM4y1q7xV/?spm_id_from=..top_right_bar_window_history.content.click&vd_source=56312c73bc0637fc9a7e871063e28f0f)





