---
title: frp代理vhost使用ssl加密
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- v2ray
- 代理
categories:
- 代理
---



# 背景

- nginx已经把443端口占用了
- 为了实现更加优雅的访问，而不是`ip:vhost_port`的方式-
- 使用nginx反向代理所有指域名的443端口的https请求到vhost_port端口去



# 配置

不要在站点设置ssl

![image-20230630001554800](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/11bf76605aba903c1ec0b31c60df5727/d3ab6b082bdd7072479cf6501421994e.png)



记住不能写127.0.0.1.因为frp也是根据路由匹配是否转发的。

![image-20230630001541198](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/11bf76605aba903c1ec0b31c60df5727/b3f2ff4cc0a6f7e5a3a5368b0fba52d8.png)









# ref

[给 Frp 穿透的内网 Web 上 https](https://blog.csdn.net/boazheng/article/details/113805793?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2-113805793-blog-121888173.235%5Ev38%5Epc_relevant_default_base&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2-113805793-blog-121888173.235%5Ev38%5Epc_relevant_default_base&utm_relevant_index=3)

[bitwarden全流程，frps穿透到公网](https://sspai.com/post/61976)

