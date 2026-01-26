---
title: Clash Verge 内网域名 + 代理共存配置指南
top: false
cover: false
toc: true
mathjax: true
date: 2026-01-25 15:27:31
password:
summary:
tags:
- clash
- 代理
categories:
- 代理
---

# Clash Verge 内网域名 + 代理共存配置指南

## 问题场景

公司内网有自部署域名（如 `*.tencent.com`），需要通过内网 DNS 解析并直连访问；同时需要代理访问外网。

在 Clash Verge 开启 TUN 模式后，内网域名无法访问，报错 `dns resolve failed: couldn't find ip`。

## 问题原因

1. **DNS 劫持**：TUN 模式的 `dns-hijack: any:53` 会劫持所有 DNS 请求，包括发往内网 DNS 的请求
2. **fake-ip 模式**：域名被分配虚假 IP，走 DIRECT 时反查真实 IP 失败
3. **配置覆盖**：Clash Verge 的「DNS 覆写」会覆盖订阅文件中的 DNS 配置

## 解决方案

### 1. 修改 DNS 劫持配置

**设置 → 虚拟网卡模式 → DNS 劫持**

将 `any:53` 改为只劫持公共 DNS：

```
223.5.5.5:53,223.6.6.6:53,8.8.8.8:53,1.1.1.1:53
```

这样内网 DNS（如 `11.xx.xx.xx`）的请求不会被劫持。

### 2. 配置 DNS 覆写

**设置 → DNS 覆写 → 高级**

使用 `redir-host` 模式，并添加 `nameserver-policy`：

```yaml
dns:
  enable: true
  listen: ':53'
  enhanced-mode: 'redir-host'
  default-nameserver:
    - 'system'
    - '223.6.6.6'
  nameserver:
    - 'https://doh.pub/dns-query'
    - 'https://dns.alidns.com/dns-query'
  nameserver-policy:
    '*.tencent.com': '11.xx.xx.xx'
    'tencent.com': '11.xx.xx.xx'
    '*.your-company.com': 'your-internal-dns-ip'
  fallback-filter:
    geoip: true
    geoip-code: 'CN'
```

**关键配置说明**：

- `enhanced-mode: redir-host`：直接返回真实 IP，避免 fake-ip 问题
- `nameserver-policy`：指定内网域名使用内网 DNS 解析

### 3. 添加直连规则

在订阅配置或规则中添加内网域名直连：

```yaml
rules:
  - DOMAIN-SUFFIX,sankuai.com,DIRECT
  - DOMAIN-SUFFIX,your-company.com,DIRECT
```

## 为什么用 redir-host 而不是 fake-ip

| 模式       | 优点                   | 缺点                                        |
| ---------- | ---------------------- | ------------------------------------------- |
| fake-ip    | 性能好，首次连接快     | 需要配置 fake-ip-filter，内网域名容易出问题 |
| redir-host | 兼容性好，内网域名友好 | 首次连接稍慢（需等待 DNS 解析）             |

Clash Verge 的 `fake-ip-filter` 配置可能不会正确传递给内核，导致内网域名仍被分配 fake-ip。使用 `redir-host` 可以彻底避免这个问题。

## 验证配置

```bash
# TUN 模式下测试 DNS 解析
nslookup your-internal-domain.com your-internal-dns-ip

# 应返回真实内网 IP，而不是 198.18.x.x
```

## 总结

1. DNS 劫持只劫持公共 DNS，放行内网 DNS
2. 使用 redir-host 模式避免 fake-ip 问题
3. 通过 nameserver-policy 指定内网域名使用内网 DNS
4. 添加 DIRECT 规则让内网流量直连
