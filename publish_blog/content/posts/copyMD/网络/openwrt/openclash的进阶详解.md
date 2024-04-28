---
title: openclash的进阶详解
top: false
cover: false
toc: true
mathjax: true
date: 2023-09-09 15:27:31
password:
summary:
tags:
- openclash
- openwrt
categories:
- 网络
---

# 背景

最近使用openclash遇到了很多问题



# 过程

- OpenClash 运行模式：

1. Fake-IP（增强）模式：

```
客户端进行通讯时会先进行DNS查询目标IP地址，拿到查询结果后再尝试进行连接。

Fake-IP 模式在客户端发起DNS请求时会立即返回一个保留地址（198.18.0.1/16），同时向上游DNS服务器查询结果，如果判定返回结果为污染或者命中代理规则，则直接发送域名至代理服务器进行远端解析。

此时客户端立即向Fake-IP发起的请求会被快速响应，节约了一次本地向DNS服务器查询的时间。

实际效果：客户端响应速度加快，浏览体验更加顺畅，减轻网页加载时间过长的情况。
```

1. Redir-Host（兼容）模式：

```
客户端进行通讯时DNS由Clash先进行并发查询，等待返回结果后再尝试进行规则判定和连接。

当判定需要代理时，使用fallback组DNS的查询结果进行通讯

实际效果：客户端响应速度一般，可能出现网页加载时间过长的情况。
```



1. Redir-Host（TUN）模式

```
此模式与Redir-Host（兼容）模式类似，不同在于能够代理所有UDP链接，提升nat等级，改善游戏联机体验。
```



1. Fake-IP（TUN）模式：

```
此模式与Fake-IP（增强）模式类似，不同在于能够代理使用域名的UDP链接。
```



1. Redir-Host（游戏）模式

```
此模式与Redir-Host（兼容）模式类似，不同在于能够代理所有UDP链接，提升nat等级，改善游戏联机体验。
```

1. Fake-IP（游戏）模式：

```
此模式与Fake-IP（增强）模式类似，不同在于能够代理所有UDP链接，提升nat等级，改善游戏联机体验。
```



------

- 模式选择建议：

1. 首选`Fake-IP（增强）模式`
2. 有稳定需求，或对NAT敏感时选择`Redir-Host（兼容）模式`
3. 其他模式均处于测试阶段，按需选择



# dns使用

通过如下方式设置dns。

![image-20230924135537598](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/dcbf708235ccb7410a7dabaf4b4d275c/e08ae1b99c500569ed648b7ab1742d73.png)



# ref



https://github.com/vernesong/OpenClash/issues/3079







https://github.com/vernesong/OpenClash/wiki/%E5%B8%B8%E8%A7%84%E8%AE%BE%E7%BD%AE
