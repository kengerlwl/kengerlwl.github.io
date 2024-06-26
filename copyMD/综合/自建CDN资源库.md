---
title: 自建CDN资源库
top: false
cover: false
toc: true
mathjax: true
date: 2024-5-07 05:27:31
password:
summary:
tags:
- CDN
categories:
- 综合
---




# 背景

我的个人博客的图床之前是基于github的免费的，但是由于众所周知的原因，国内访问还是太慢了，决定换位自己的国内云服务器的CDN。

CDN（Content Delivery Network）即**内容分发网络，是一种分布式网络服务，其目的是通过在全球范围内的多个地理位置部署边缘服务器节点，来优化互联网上内容的分发和访问速度。**

cdn 主要作用都是优化用户的访问路径，在距离上离用户更近，工作中接触过的两个场景：

1、通过**动静分离**，优化用户访问速度；因为静态资源（如图片、css、js等）通过cdn的缓存分发，减轻了服务器的访问和流量压力。

2、**海外加速**，通过设置cdn回源加速用户的访问；针对海外用户访问国内应用慢的问题，回源(相当于cdn不缓存了，直接访问后端服务，而cdn的服务器和国内的服务器是有专线连接)保障了请求响应的高效。

## 技术选择

- cdnfly
- goEdge 最后我**选择了这个**



## 结果

太重量级了，放弃使用这个作为我的CDN。

# 方法

通过docker可以部署，我的`docker_demo`里面有

有一个主控`admin`管理面板中心

**然后有若干的分布在不同地方的节点可以注册到admin。**

类似于K8S。会实现统一入口访问，然后分发到不同的节点。







# ref

[自建cdn系统 - goedge - 知乎](https://zhuanlan.zhihu.com/p/678075231)

[使用Docker快速部署GoEdge 搭建自己专属的CDN服务 – iCodex's Blog](https://icodex.org/2024/02/24/use-docker-to-quickly-deploy-goedge/)

