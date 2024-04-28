---
title: 关于web服务中的认证，授权，会话
top: false
cover: false
toc: true
mathjax: true
date: 2023-09-01 15:27:31
password:
summary:
tags:
- web
- Spring
- Session
categories:
- 技术
---



# 背景

在学习过程中，认证与授权通常是绕不过去的一部分，很多服务都有身份限制，不是特定的用户不能执行部分的资源操作，也不能访问到其他用户。

个人在学习过程中对这个学的还不够透彻，经常是一知半解。需要深入的学习一下里面的常见的技术以及整体的架构。

故有本文，来解决这个问题。



# web服务（说明场景需求）

在基础的web服务中，我们的会话往往是无状态的，也就是说，上一次的访问时的结果等信息这一次并不知道，每次都是一次独立的访问。（**HTTP 是无状态的协议（对于事务处理没有记忆能力，每次客户端和服务端会话完成时，服务端不会保存任何会话信息**））

而在常见的用户会话中，我上次登陆后，这次应该知道我已经登陆，并开放部分权限。

这就会设计到很多常见的概念，例如Cookie，Session和Token等等。





### Cookie

Cookie本身可以理解为一个键值对

**cookie 存储在客户端：** cookie 是服务器发送到用户浏览器并保存在本地的一小块数据，它会在浏览器下次向同一服务器再发起请求时被携带并发送到服务器上。

**服务器端修改客户端的Cookie**：服务器端可以通过设置setCookie的Response的header来修改客户端的Cookie。



### Session

- **session 是另一种记录服务器和客户端会话状态的机制**

注意，Session仅仅只是一种机制，实现方式有很多，

![v2-369c25ea411974a1cd4d6ed69d533bcb_b](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/1c96dc0740678a515e90ba0f3ee8ff6f/b5b07d10863a53a4cb4e74fd08677838.png)



- **session 认证流程：**

- - 用户第一次请求服务器的时候，服务器根据用户提交的相关信息，创建对应的 Session
  - 请求返回时将此 Session 的唯一标识信息 SessionID 返回给浏览器
  - 浏览器接收到服务器返回的 SessionID 信息后，会将此信息存入到 Cookie 中，同时 Cookie 记录此 SessionID 属于哪个域名
  - 当用户第二次访问服务器的时候，请求会自动判断此域名下是否存在 Cookie 信息，如果存在自动将 Cookie 信息也发送给服务端，服务端会从 Cookie 中获取 SessionID，再根据 SessionID 查找对应的 Session 信息，如果没有找到说明用户没有登录或者登录失效，如果找到 Session 证明用户已经登录可执行后面操作。

根据以上流程可知，**SessionID 是连接 Cookie 和 Session 的一道桥梁**，大部分系统也是根据此原理来验证用户登录状态。

- **Session是一种链式的**

- 注意：Sessionid是存储在服务器端的，服务器端也可以对Sessionid记录一些信息在服务器上类似Cookie记录当前会话的信息在客户端上。



# 关于Token

Token和前面提到的Cookie和Sessionid很像，都是为了验证鉴权整出来的东西。

**是一种令牌机制。Token 使服务端无状态化，不会存储会话信息。Token认证适用于分布式系统和跨域认证场景**

- **访问资源接口（API）时所需要的资源凭证**

- **特点：**

- - **服务端无状态化、可扩展性好**
  - **支持移动端设备**
  - 安全
  - 支持跨程序调用
  - 通常也是放header里面传递
- **移动端对 cookie 的支持不是很好，而 session 需要基于 cookie 实现，所以移动端常用的是 token**

## **什么是 JWT**

- - JSON Web Token（简称 JWT）是目前最流行的**跨域认证**解决方案。
  - 是一种**认证授权机制**。
  - JWT 是为了在网络应用环境间**传递声明**而执行的一种基于 JSON 的开放标准（RFC 7519）

## **Token 和 JWT 的区别**

**区别：**

- Token：服务端验证客户端发送过来的 Token 时，还需要查询数据库获取用户信息，然后验证 Token 是否有效。
- JWT：将 Token 和 Payload 加密后存储于客户端，服务端只需要使用密钥解密进行校验（校验也是 JWT 自己实现的）即可，不需要查询或者减少查询数据库，因为 JWT 自包含了用户信息和加密的数据。





# **分布式架构下 session 共享方案**

- 基于持久化第三方组件，例如Redis，mysql。Spring Session就支持Redis存储

# ref

[还分不清 Cookie、Session、Token、JWT？](https://zhuanlan.zhihu.com/p/164696755)
