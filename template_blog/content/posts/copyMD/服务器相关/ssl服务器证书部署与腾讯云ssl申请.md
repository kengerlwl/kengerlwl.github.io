---
title: ssl服务器证书部署与腾讯云ssl申请
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- 服务器
- ssl
categories:
- 服务器
---
# 背景

鉴于http的安全性问题，以及对于ldap以及部分安全性效验较强的场景。因此必须在访问web服务时部署https服务，采用ssl加密提高安全性。



说明：

- 由于我没有做服务器备案（也不想做），**因此域名解析到服务器ip是不可以进行正常的浏览器web访问的，但是其他tcp访问是没问题的**
- 我的机器大多放在实验室和宿舍两个场景。主要使用人是我自己。云服务有一台
- 我的目的是对我的本地服务器搭建ssl



# 腾讯云申请ssl证书

**要求**

- 拥有一个腾讯云域名
- 拥有一个服务器，无论云端还是本地，（vps云端如果不备案用不了）

## 腾讯云免费SSL申请

**1、登录腾讯云ssl管理控制台**

控制台地址：[https://console.cloud.tencent.com/ssl/](https://link.zhihu.com/?target=https%3A//console.cloud.tencent.com/ssl/)

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/9d01b0a126164afb713932382fce16f7/590d7be83374b8aed2e9759b03d9531b.png)

**2、进入申请流程**

点击上图标记的“申请免费证书”按钮，进入申请流程。

首先选择要申请的证书类型，这里默认是亚洲诚信的，当然你也可以选择其他机构证书。

**备注：如果你选择的是其他机构证书，可能就会涉及到费用问题了，而不是免费的了，需要在选择是看清楚是否需要付费。**

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/9d01b0a126164afb713932382fce16f7/3f957bce5a3f1e4824906c3b294641ee.png)

**3、提交申请域名的基本信息**

这里将你要用来申请证书的域名信息和基本的证书信息进行选择和填写。其中关于算法根据需求进行选择，如果没有特殊需求可以直接默认RSA算法。

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/9d01b0a126164afb713932382fce16f7/0dd4d7b2c3d8bb7aae7c5cc6084ca4a9.png)

**4、选择证书验证方式**

这里证书验证方式常规提供两种方式：

- **DNS验证**

这种方式就是需要你去你的域名控制台进行域名解析设置，将记录值指向证书这边。

- **文件验证**

这种方式需要你在相应域名解析的站点下面创建指定的文件（一般都会提供现有文件进行上传），然后进行验证。

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/9d01b0a126164afb713932382fce16f7/ae5ffb578eaa99907d18e7e63ec7c718.png)

**5、进行证书验证**

当选择后可以点击界面中的按钮进行证书申请校验，如果校验通过就可以拥有属于你的1年的免费ssl证书了。

如果出现像我一样的以下错误可以根据腾讯官方的错误描述进行排查问题。

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/9d01b0a126164afb713932382fce16f7/73b9e0b8d16f764a721d37767b121144.png)

**6、证书申请完成**

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/9d01b0a126164afb713932382fce16f7/6fa5eecdbe084f0617bffdab436f6e26.png)

证书申请完成后腾讯云提供了两种安装方式，第一种我们自己手动安装，另一种他们人工安装。

这里我选择自己手动安装方式进行证书安装使用。

# 证书部署

背景

- 我这里用的是linux，nginx服务器



腾讯云，下载效验文件

![image-20230629203700271](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/9d01b0a126164afb713932382fce16f7/7da6b2f2b8048951ecd53907993ad385.png)

文件目录为

```
~/Dow/hw.c/hw.chatgpt.kenger.work_nginx ❯ tree                          Py base
.
├── hw.chatgpt.kenger.work.csr
├── hw.chatgpt.kenger.work.key  (key)
├── hw.chatgpt.kenger.work_bundle.crt
└── hw.chatgpt.kenger.work_bundle.pem (pem)
0 directories, 4 files
```



宝塔面板，找到相应站点的ssl设置，复制粘贴进去

![image-20230629203946622](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/9d01b0a126164afb713932382fce16f7/cb1d74bf9bdc42676cddf89a5235974b.png)





# 附录

DNS验证和文件验证是SSL证书颁发机构（CA）用于**验证域名所有权的两种常见方法。**

1. DNS验证：**在DNS验证中，您需要向CA提供一个特定的DNS记录以证明您对域名的控制权。**通常，CA会要求您在域名的DNS设置中添加一个特定的TXT记录或CNAME记录。一旦您成功添加了该记录，并且DNS记录已经生效并传播到全球的DNS服务器上，CA就可以通过查询这个DNS记录来验证您对该域名的控制权。这种方式适用于各种类型的SSL证书。

2. 文件验证：**在文件验证中，您需要在您的网站根目录中放置一个由CA提供的验证文件**。该验证文件的名称和内容是根据CA的要求生成的。验证过程中，CA会尝试从指定的URL下载该验证文件。如果成功下载并匹配到正确的内容，就验证通过。这种方式适用于某些类型的SSL证书，特别是使用通配符或多域名证书时较为常见。

**这两种验证方法都是为了确保SSL证书只颁发给真正拥有该域名的人或组织。**验证成功后，CA会签发SSL证书，您可以将其安装在您的服务器上，启用加密连接和安全通信。

因此，不难得知，域名解析，以及云服务器使用ssl。与通过域名ssl是没有必须关系的。

**本地服务器也可以使用ssl验证。**







**常用域名类型**

1. **域名验证证书（DV）：这是最基本的SSL证书类型，只验证域名的所有权**。它们可以快速颁发，并且适用于个人网站、博客等非商业用途。
2. 组织验证证书（OV）：这种证书会对域名和组织进行验证，以确保您的组织合法存在。它们提供更高级别的身份验证和可信度，适用于中小型企业和机构。
3. 增强验证证书（EV）：EV证书是最高级别的SSL证书，提供了最严格的身份验证标准。在浏览器地址栏中显示绿色的公司名称，向用户传达更高的信任感。EV证书适用于电子商务、金融机构等需要建立强大信任的网站。
4. **泛域名证书（Wildcard）：泛域名证书允许您保护一个主域名及其所有子域名。通过使用通配符（*），您可以轻松地覆盖多个子域名的安全性**。
5. 多域名证书（SAN）：也称为主题备用名称证书，它允许您在单个证书中保护多个不同域名。这对于拥有多个相关网站或应用程序的企业非常有用。



