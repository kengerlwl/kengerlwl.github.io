---
title: openwrt的dhcp绑定与设置详解
top: false
cover: false
toc: true
mathjax: true
date: 2023-09-09 15:27:31
password:
summary:
tags:
- dhcp
- openwrt
categories:
- 网络
---

# 背景

计划将openwrt作为主路由，然后通过dhcp绑定来绑定ip与mac地址。





# 方法

我这里使用的esir的高大全固件

**设置**

![image-20230918160554220](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cd73dd14663bf3d11348686e8bea3748/57a136d23f09a045112ac69872e7d015.png)





## 客户端刷新

```
# win
>ipconfig /release

# mac
sudo ipconfig set en9 DHCP #en9是网卡名字

# linux
dhclient -r
```

