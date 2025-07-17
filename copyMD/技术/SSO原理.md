---
title: SSO原理
top: false
cover: false
toc: true
mathjax: true
date: 2025-07-10 15:27:31
password:
summary:
tags:
- spring
- sso
categories:
- 技术
---

# 背景

目前而言，一个公司往往会有多个系统，而每个系统都需要登录才能访问资源。
SSO（单点登录）就是为了解决这个问题而出现的。
SSO 的主要思想是**在一个系统中登录一次，就可以访问其他系统**。（同域）

# 实现
假设S系统提供了SSO服务。
A系统和B系统都依赖S系统提供的SSO服务。
A系统和B系统都需要登录才能访问资源。
A系统登录后，B系统不需要再次登录就可以访问资源。
![alt text](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cfd513337dda68d87f2963ab48f95794/508ac8cc56f6e45c5a4fe6da34889b74.png)


流程就是
1. 用户访问A系统，没有权限需要登陆，向S系统发起请求
2. S系统判断用户没有登陆，返回A系统的登陆页面
3. 用户输入账号密码，向S系统发起请求
4. S系统判断用户输入的账号密码正确，返回A系统的登陆成功页面
5. A系统登陆成功，将用户信息保存到cookie中
6. A系统访问B系统，B系统判断用户已经登陆，直接返回资源

# 方案CAS
目前比较流行的SSO方案就是CAS（Central Authentication Service）
CAS是一个开源的SSO解决方案，它提供了一套完整的SSO解决方案，包括身份认证、授权、会话管理等功能。
CAS的核心思想是**在一个系统中登录一次，就可以访问其他系统**。（同域）