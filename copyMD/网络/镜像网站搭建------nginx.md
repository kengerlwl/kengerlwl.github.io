---
title: 镜像网站搭建------nginx
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- nginx
- 镜像网站
categories:
- 代理
---

# 代理

- 代理后登录服务一般都会用不了。
- 一般只能针对单个域名进行代理，如果使用子域名一多，就无法代理了。





# 关于国内域名备案与解析

国内每一个服务器，如果要部署用户可以访问的web页面服务，都是要针对域名和服务器进行备案的。

如果该服务器没有备案，则不可以被域名解析访问到。

不过，我们可以使用dns解析ip的服务还是可以使用，以及一些常见的tcp，udp的请求，

**也就是说，可以在不备案的情况下使用tcp，udp的frp，v2ray之类的代理穿透程序**

所以就针对内网而言，仅仅使用该服务即可。

**域名仅通过web端访问就会拦截**



# 坑





### 1

我的cloudflare的域名，并不支持四级域名的CNAME解析。只支持A解析。



### 2

只有使用灵活模式才能申请宝塔的免费ssl

![image-20230407222716842](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/9d912c55b95bf6659a9d54cba521cd3f/f8c694ef52aacee0ebeea1988ec1a14a.png)



# ref

https://5656t.com/archives/1868

[Cloudflare免费SSL配置使用教程](https://cloud.tencent.com/developer/article/2255105)

https://blog.laoda.de/archives/try-cloudflare-free-15-year-ssl-certificate?cid=3757
