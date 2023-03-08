---
title: 基于宝塔nginx的多站点管理
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- 服务器
- 宝塔
- nginx
categories:
- 服务器
---
# 应用的场景

有若干服务需要访问，他们或者ip不一样，或者端口不一样。

如果一个个的去绑定隐形url域名挺麻烦的。也没必要。

一个优秀的办法是，通过不同的域名访问过去。然后根据域名不同做反向代理。



# demo

我服务器上有一个wordpress，其端口是8081。我想要通过`blog.kenger.com`去访问该服务。



## 设置二级域名

先直接将域名指向服务器ip。或者服务器www域名也可以。总之就是直接到80端口。

![image-20221217203603861](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7d3fdd730213faafd876f5c39adc98ca/7c600b883827b37010c4aa5fd5a6ad04.png)

## 设置宝塔面板nginx

然后去宝塔

![image-20221217203731037](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7d3fdd730213faafd876f5c39adc98ca/4478ddcc4224e5f5fa0ba799d09c245e.png)



添加一个站点

![image-20221217203751574](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7d3fdd730213faafd876f5c39adc98ca/96411d22da4f6290b0c8645b93df94af.png)



设置反向代理到本地

![image-20221217204302535](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7d3fdd730213faafd876f5c39adc98ca/0a0df8a8546b32df15f96a5226a75713.png)

### 错误注意

尽量不要用localhost。用127.0.0.1更好。

![image-20221217203808588](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7d3fdd730213faafd876f5c39adc98ca/d1fb124357b45b2d75a26dcfa362255f.png)



然后就可以访问了



![image-20221217204312605](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7d3fdd730213faafd876f5c39adc98ca/510f3b91cd60dcc1840fc5194894106a.png)





# 伪静态设置

通俗来讲其实就是一种seo的方式。

伪静态是相对真实静态来讲的，通常我们为了增强搜索引擎的友好面，都将文章内容生成静态页面，但是为了实时的显示一些信息，就损失了对搜索引擎的友好面。 伪静态即是**网站本身是动态网页，url后有"?** **"加参数来读取不同数据，伪静态就是做url重写操作(rewrite)**。

```
// 监听80端口
//访问www.test.com/wangla.html跳转到百度
//访问www.test.com/纯数字至少一个数字.html跳转到QQ官网
//访问www.test.com/匹配字母或数字或下划线组合.html 跳转到百度对应页面。
server {
    listen       80;
    server_name      www.test.com;
    index    index.html index.htm index.php;
 
    rewrite  ^/wangla.html$  http://www.baidu.com/ permanent;
    rewrite  ^/(\d+).html$   http://www.qq.com/ permanent;
    rewrite  ^/(\w+).html$   http://www.baidu.com/index_wd_v5.html permanent;
}
```

