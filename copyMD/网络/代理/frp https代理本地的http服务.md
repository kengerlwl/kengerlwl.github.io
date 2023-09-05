---
title: frp https代理本地的http服务
top: false
cover: false
toc: true
mathjax: true
date: 2023-06-30 15:27:31
password:
summary:
tags:
- https
- frp
categories:
- 代理
---

# 背景

我有一个bitwarden服务需要https访问，并代理到公网。

- frp可以代理本地的http服务到公网https访问
- 用到frp的一个插件（frp自带的），`https2http` 将服务器端的https请求转到本地的http服务

不适用浏览器访问，就不会被封控





# 实操





## 服务器端

配置，添加两行

`vhost_http_port = 10080
vhost_https_port = 10443`

这是指定其他端口作为https或者http端口，这两个端口可以一样

```
[common]
# frp监听的端口，默认是7000，可以改成其他的
bind_port = 7000
# 授权码，请改成更复杂的
token = xxx

#allow_ports = 2000-3000,6081,4000-50000 #端口白名单
vhost_http_port = 10080
vhost_https_port = 10443
# frp管理后台端口，请按自己需求更改
dashboard_port = 7500
# frp管理后台用户名和密码，请改成自己的
dashboard_user = admin
dashboard_pwd = xxx
enable_prometheus = true


# TLS
tls_only = true


# frp日志配置
log_file = /var/log/frps.log
log_level = info
log_max_days = 3
```





## 客户端



**注意看说明：**

```
# 客户端配置
[common]
server_addr = tx.kenger.work
server_port = 7000
token = WKcqDgd8k5WgF2Xp2koj


# TLS
tls_enable = true
disable_custom_tls_first_byte = true


[bitwarden_https_port]
type = https
#（这个域名解析到服务器端，然后服务器端访问该 域名：vhost_https_ip）
custom_domains = txs.kenger.work  

plugin = https2http
#(指定我本地需要代理的端口)
plugin_local_addr = 127.0.0.1:8080

# HTTPS 证书相关的配置
#txs.kenger.work的ssl证书
plugin_crt_path = /etc/frp/ssl/server.crt    
plugin_key_path = /etc/frp/ssl/server.key
plugin_host_header_rewrite = 127.0.0.1
plugin_header_X-From-Where = frp

```



最后可以通过测试：

```
root@VM-4-7-ubuntu:~/docker_demo/frp/frps# curl https://txs.kenger.work:10443
<!doctype html></script></body></html>
```









# 坑

### bitwarden的需要代理的端口是80端口

bitwarden的3012 端口作为其 Web Vault 的默认端口，但并不是我需要代理到公网的端口。

我用docker映射80到了8080端口









# ref

[给 Frp 穿透的内网 Web 上 https](https://blog.csdn.net/boazheng/article/details/113805793?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2-113805793-blog-121888173.235%5Ev38%5Epc_relevant_default_base&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2-113805793-blog-121888173.235%5Ev38%5Epc_relevant_default_base&utm_relevant_index=3)

[bitwarden全流程，frps穿透到公网](https://sspai.com/post/61976)

