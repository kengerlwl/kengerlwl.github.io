---
title: docker实践自部署Overleaf
top: false
cover: false
toc: true
mathjax: true
date: 2023-04-15 15:27:31
password:
summary:
tags:
- pytorch
categories:
- 学术
---
# 安装overleaf的社区版

[github 链接](https://github.com/overleaf/overleaf)

上面是github的链接，访问然后里面有个docker compose.yml文件。

集成了overleaf， Redis， MongoDB

一键部署。

我修改了一下数据的挂载，改成相对目录

![image-20230413234939354](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/72eba7038b7a0441bc4cabfa1b6703c9/ad50ab79944109ff4ada7a17760076a3.png)

```
docker-compose -f docker-compose.yml up
```





# 初始化管理员

Overleaf 实例运行后，访问该`/launchpad`页面以设置您的第一个管理员用户。

访问：

```
ip:port/launchpad
```







# 升级到完整版

安装的过程中，相关脚本会创建一个名为sharelatex的container，根据Overleaf Wiki上的[说明](https://github.com/overleaf/overleaf/wiki/Server-Pro:-setup)，**目前安装的Overleaf中的TexLive版本仅为精简版，因此我们需要先安装上完整版的TexLive。**

*参考 https://yxnchen.github.io/technique/Docker部署ShareLaTeX并简单配置中文环境/#安装并配置ShareLaTeX*

```
# 进入容器的命令行（sharelatex容器本质上是一个Ubuntu）
$ docker exec -it sharelatex bash

# 进入texlive默认安装目录
$ cd /usr/local/texlive

# 复制2020文件夹为2021
$ cp -a 2020 2021

# 下载并运行升级脚本
$ wget http://mirror.ctan.org/systems/texlive/tlnet/update-tlmgr-latest.sh
$ sh update-tlmgr-latest.sh -- --upgrade

# 更换texlive的下载源
$ tlmgr option repository https://mirrors.sustech.edu.cn/CTAN/systems/texlive/tlnet/

# 升级tlmgr
$ tlmgr update --self --all

# 安装完整版texlive（漫长的等待，不要让shell断开）
$ tlmgr install scheme-full

# 推出sharelatex的命令行界面，并重启sharelatex容器
$ exit
$ docker restart sharelatex

# 安装Noto字体（可选）
$ apt install fonts-noto-cjk
```







# ref

https://sparktour.me/2021/04/02/self-host-overleaf/
