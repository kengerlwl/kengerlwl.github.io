---
title: clash定制化的订阅构建
top: false
cover: false
toc: true
mathjax: true
date: 2023-05-26 15:27:31
password:
summary:
tags:
- clash
- 代理
- 分流
categories:
- 代理
---

# 需求

我目前工作环境和家庭环境是分布两个不同的内网环境，并且我分别给两个环境搭建了v2ray代理，实现从公网代理到内网。因此，我需要：

- 在内网环境就直接直连，走内网
- 在公网环境，就走代理，代理到内网

另一方面，由于购买的节点可能需要更新，导致我这里的订阅可能也需要及时更新，那么我自己编写的规则经常被覆盖，需要重新弄。

- 编写自己的流量规则
- 经常更新机场订阅节点，但保留原有的规则。

- 提供在线托管的订阅



# 自动切换节点问题

使用`type: url-test`。

```
  - name: SchoolLAN
    interval: 300
    proxies:
    - DIRECT
    - csuoss
    - csuoss_inner
    # - oss
    tolerance: 100
    type: url-test
    url: https://oa.csuoss.cn/api/generate_204

```

规则，指定域名走该节点组

```
  - DOMAIN-SUFFIX,csuoss.cn,SchoolLAN
```

`interval`: 测试请求的间隔时间，这里是300秒（5分钟）。Clash将每隔一段时间发送测试请求来评估节点的性能。





# proxy-providers配置

用这个实现保留规则的节点更新

分为以下几个部分，订阅更新部分，将所有节点分为多个块，分别进行进行，我这里用的Github私有仓库进行订阅管理。

```
  csj_all:
    type: http
    url: "https"
    interval: 86400
    path: ./csj_ssr.yaml
    health-check:
      enable: true
      interval: 600
      url: http://www.gstatic.com/generate_204

  csj_us:
    type: http
    url: "https:"
    interval: 86400
    path: ./csj_us.yaml
    filter: 'US|美国'
    health-check:
      enable: true
      interval: 600
      url: http://www.gstatic.com/generate_204


  inner:
    type: http
    url: "https:"
    interval: 86400
    path: ./inner.yaml
    health-check:
      enable: true
      interval: 600
      url: http://www.gstatic.com/generate_204
```

然后是将这些节点引入节点组

```
proxy-groups:

  - name: OutProxy
    interval: 300
    proxies:
      - DIRECT
    use:
      - csj_all
    tolerance: 60
    type: select
    url: https://oa.csuoss.cn/api/generate_204



  - name: SchoolLAN
    interval: 300
    proxies:
      - DIRECT
    use:
      - inner
    tolerance: 60
    type: url-test
    url: https://oa.csuoss.cn/api/generate_204

```

最后是配置规则

```
  # google和openai
  - DOMAIN-KEYWORD,openai,openai
  - DOMAIN-KEYWORD,google,OutProxy


  # git
  - DOMAIN-SUFFIX,git.io,OutProxy
  - DOMAIN-KEYWORD,github,OutProxy

  - DOMAIN-KEYWORD,bing.com,bing

  # # 我的实验室内网服务
  # - DOMAIN-KEYWORD,oss.kenger,oss_kenger


  # 宿舍网络直连。clash是优先级匹配，先匹配到的就成功
  - DOMAIN-SUFFIX,208.kenger.top,DIRECT

  # 博客单独走
  - DOMAIN-SUFFIX,kenger.top,OutProxy

  - DOMAIN-SUFFIX,dl.acm.org,SchoolLAN
  - DOMAIN-SUFFIX,csubot.cn,SchoolLAN
  - DOMAIN-SUFFIX,csu.edu.cn,SchoolLAN
  - DOMAIN-SUFFIX,sciencedirect.com,SchoolLAN
  - DOMAIN-SUFFIX,springer.com,SchoolLAN
  - DOMAIN-SUFFIX,csuoss.cn,SchoolLAN
  - DOMAIN-SUFFIX,ieee.org,SchoolLAN
  - DOMAIN-SUFFIX,cnki.net,SchoolLAN

```













# ref

https://lancellc.gitbook.io/clash/clash-config-file/proxy-groups/auto

