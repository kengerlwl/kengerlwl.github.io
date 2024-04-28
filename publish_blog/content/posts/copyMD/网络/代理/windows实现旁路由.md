---
title: windows实现旁路由
top: false
cover: false
toc: true
mathjax: true
date: 2023-10-25 15:27:31
password:
summary:
tags:
- windows
- 旁路由
- 代理
categories:
- 代理
---

# 背景

使用linux的时候，用op作为网关，openclash做分发。有dns污染问题。

机缘巧合之下，使用windows的clash代理，加上开启路由转发功能。实现了没有dns污染的旁路由。



# 操作

windows上启用clash。

![image-20231025002302280](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/570acd47f145aa15f9d6903e5f42a41c/9554d49bbd5359348167667fb0e686ce.png)



![image-20231025002507591](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/570acd47f145aa15f9d6903e5f42a41c/24ab1e1adcf01835d009b5c2b5bd7f7f.png)





然后其他机器设置网关即可。







# ref

https://www.youtube.com/watch?v=dpmnkKhBFtc&t=221s&ab_channel=%E4%B8%8D%E8%89%AF%E6%9E%97
