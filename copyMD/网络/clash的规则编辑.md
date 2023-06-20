---
title: clash的规则编辑
top: false
cover: false
toc: true
mathjax: true
date: 2023-04-13 15:27:31
password:
summary:
tags:
- nginx
- 镜像网站
categories:
- 代理
---

# 结构



## 节点proxy



`Proxy` 部分是 Clash 配置文件的一部分，用于定义代理服务器列表及其属性。

```
proxies:
	- {cipher: auto, name: test2, alterId: 0, port: 52333, server: gpu2.csubot.cn, type: vmess, uuid: 8FF6627C-C247-44EB-A9AA-A7EAB8385D4A}

```



## 节点组

`proxy-groups` 是 Clash 配置文件中的一部分，用于定义代理服务器组列表及其属性。与 `Proxy` 部分不同的是，`proxy-groups` 中的每个代理服务器组实际上并不包含代理服务器的配置信息，而是用来指定在该组中应该使用哪些代理服务器。

在 `proxy-groups` 中，你可以定义多个代理服务器组，并为每个代理服务器组设置以下基本属性：

- `name`：代理服务器组名称。
- `type`：代理服务器组类型，如 select、url-test、fallback 等。
- `proxies`：该代理服务器组应该使用的代理服务器名称列表。

```

  - name: google
    interval: 300
    proxies:
    - DIRECT
    - 香港1
    # - oss
    tolerance: 100
    type: select
    url: http://www.gstatic.com/generate_204
```

`type`说明：

在 Clash 的 `proxy-groups` 部分，有三种常见的代理服务器组类型：`select`、`url-test` 和 `fallback`。它们分别表示以下内容：

- `select`：从列表中选择一个可用的代理服务器作为当前请求的代理。可以通过设置每个代理服务器的权重值来进行负载均衡。
- `url-test`：通过向特定 URL 发送测试请求来检查代理服务器是否可用，然后选择可用的代理服务器作为当前请求的代理。可以设置每个代理服务器的 URL 和超时时间等属性。
- `fallback`：按照预定义顺序依次尝试不同的代理服务器，直到找到一个可用的代理服务器并将其用作当前请求的代理。可以设置每个代理服务器的优先级和延迟时间等属性。

这些代理服务器组类型在 Clash 配置文件中的规则配置部分起着至关重要的作用，可以根据流量类型、目标地址等条件选择不同的代理服务器组来进行流量转发。

`url`说明`url: http://www.gstatic.com/generate_204`

generate_204接口通常用于检测网络是否连接，其要求如下：

1. 返回HTTP状态码204，表示请求成功但没有内容返回。
2. 不需要任何参数或请求体，只需返回空响应即可。
3. 接口的地址可以是任意的，不需要特定的格式或路径。

# `Rule`，规则列表，用于指定流量如何匹配代理服务器。



在 Clash 配置文件的 `Rule` 部分中，你可以定义一系列规则来指定流量如何匹配代理服务器。每个规则由一个匹配模式和一个代理服务器组构成，当流量匹配特定的条件时，将会使用对应的代理服务器组来进行转发。以下是 Clash 支持的几种基本的匹配模式：

- `DOMAIN-SUFFIX`：域名后缀匹配。例如，`DOMAIN-SUFFIX,google.com` 表示匹配以 `google.com` 结尾的所有域名。
- `DOMAIN`：域名匹配。例如，`DOMAIN,www.google.com` 表示精确匹配 `www.google.com` 域名。
- `IP-CIDR`：IP 地址段匹配。例如，`IP-CIDR,10.0.0.0/8` 表示匹配以 10. 开头的所有 IP 地址。
- `GEOIP`：地理位置匹配。例如，`GEOIP,CN` 表示匹配位于中国的所有 IP 地址。
- `DOMAIN-KEYWORD` 是 Clash 规则配置中用于匹配域名的一种匹配模式，它可以匹配包含特定关键字的域名。例如，`DOMAIN-KEYWORD,google` 可以匹配包含 `google` 关键字的所有域名，如 `www.google.com`、`mail.google.com` 等。





## demo



```
rules:

  # google和openai
  - DOMAIN-KEYWORD,openai,openai   # 
  - DOMAIN-KEYWORD,google,google

  - DOMAIN-KEYWORD,bing.com,bing

  # 我的实验室内网服务
  - DOMAIN-KEYWORD,oss.kenger,oss_kenger

  # 博客单独走
  - DOMAIN-SUFFIX,kenger.top,Teacat

  - DOMAIN-SUFFIX,dl.acm.org,SchoolLAN
  - DOMAIN-SUFFIX,csubot.cn,SchoolLAN
```



## 优先级问题

在 Clash 的规则配置中，规则的优先级是按照从上到下的顺序依次匹配的。也就是说，当一个请求到达时，Clash 会从第一条规则开始逐一匹配，直到找到与请求最匹配的规则为止，然后使用该规则所对应的代理服务器组来进行流量转发。

**如果多个规则同时匹配了同一个请求，那么匹配顺序靠前的规则将具有更高的优先级，并且会覆盖靠后的规则**





# `DNS`，DNS 服务器列表及其属性。



# ref

来自chatgpt以及我查阅的资料

