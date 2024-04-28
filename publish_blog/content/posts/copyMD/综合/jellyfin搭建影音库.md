---
title: jellyfin搭建影音库
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- jellyfin
categories:
- 综合
---
# 背景

已经有了nas很久了，但是一直没有根据里面的资源弄自己的影音库。市面上其他的影音库大多收费，例如plex，emby。

于是决定采取开源的jellyfin，官网https://jellyfin.org



# method

首先在电脑上安装。

一些跟着引导走的就不多说了。

**注：jellyfin支持访问smb的nas资源。**



## 关于转码

为什么影片需要转码

1. 影片格式目标机器可能不支持，例如mkv
2. 影片分辨率等参数可以调整，方便不同的网络以及硬件环境。

如何做。

1. 我的设备：x99虚拟机，还没搞显卡。操作系统：Win10。由于没有相应的硬件，没有集显没有独显，所以采用软解

2. 分类
   1. **硬解**是利用专用硬件解码器GPU处理视频数据以提高解码效率和速度。
   2. **软解**是通过通用处理器CPU执行解码算法以实现更广泛的视频格式和参数支持。

3. 设置

4. ![image-20240216160642142](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/713f10a9e5b3df6f9ca55da80e92bcfe/5036bbc0c719a85f5c88ed56db2d5434.png)

5. 选择需要的分辨率

  ![image-20240216160725449](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/713f10a9e5b3df6f9ca55da80e92bcfe/c99c9da429eea43214d2670fed9e67f1.png)





# ref

