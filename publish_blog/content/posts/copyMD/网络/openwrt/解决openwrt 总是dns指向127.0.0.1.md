---
title: 解决openwrt 总是dns指向127.0.0.1
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- openwrt
- 代理
categories:
- 代理
---


# 背景

有一个openwrt，其每次开机后的` /tmp/resolv.conf`文件一直自动生成将dns指定为本地的`127.0.0.1`.

导致以该openwrt为路由的时候无法访问任何网站。



## 原因

dnsmasq的锅，每次开机都会重新生成。

在找不到合适的配置修改项的情况下。我参考了reddit论坛里面大佬的做法，直接修改dnsmasq程序。

**其实该程序也是一个shell脚本，只不过比较大而已。**





# 方法

修改`/etc/init.d/dnsmasq `

该文件的1000多行。直接修改函数：`dnsmasq_start`

在该函数尾部加入。

之所以这么做，是因为

` /etc/resolv.conf`指向` /tmp/resolv.conf`

```
	rm /tmp/resolv.conf
	echo "nameserver 8.8.8.8" >> /tmp/resolv.conf
	echo "search lan." >> /tmp/resolv.conf
```

# ref

https://www.reddit.com/r/openwrt/comments/10pc11i/openwrt_problem_with_dns/



# 感想

傻逼的openwrt，

