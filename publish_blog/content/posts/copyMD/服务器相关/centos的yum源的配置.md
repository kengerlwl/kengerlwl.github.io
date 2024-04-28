---
title: centos的yum源的配置
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- 服务器
- linux
categories:
- 服务器
---
### yum源配置

```bash
yum install nginx
```

没有配置yum源，好麻烦。找了教程

二十二、Centos安装yum,wegt(完全配置篇）链接如下

https://developer.aliyun.com/article/939699

1、先看是不是有yum

```bash
rpm -qa | grep yum
```

2、删除之前的yum包

```bash
rpm -aq | grep yum | xargs rpm -e --nodeps
```

3、查看
![在这里插入图片描述](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/27b7ca39ce6c419cd68af06fd49a272f/46cbd7160ed983002e180f9693d9f506.png)4、下载rpm,repo包

（1）在此网易镜像链接下载http://tel.mirrors.163.com/centos/7/os/x86_64/Packages/
（2）五个包
![在这里插入图片描述](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/27b7ca39ce6c419cd68af06fd49a272f/37642dfb8aeea230835b49100835f053.png)rz 命令上传到linux
![在这里插入图片描述](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/27b7ca39ce6c419cd68af06fd49a272f/2803df350ec1ff5df6a40be6e7756b4e.png)
(4)安装

```bash
rpm -ivh python-2.7.5-89.el7.x86_64.rpm python-iniparse-0.4-9.el7.noarch.rpm --nodeps --force
 rpm -ivh yum-metadata-parser-1.1.4-10.el7.x86_64.rpm --nodeps --force
rpm -ivh yum-3.4.3-168.el7.centos.noarch.rpm yum-plugin-fastestmirror-1.1.31-54.el7_8.noarch.rpm --nodeps --force
```

![在这里插入图片描述](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/27b7ca39ce6c419cd68af06fd49a272f/3be3fd8466481090b19664b534750969.png)5、更改yum源

（1）备份/etc/yum.repos.d/CentOS-Base.repo

```bash
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
```

(2)下载CentOS7 repo文件

http://mirrors.163.com/.help/centos.html根据此网站教程CenOS镜像使用帮助

将下载好的repo文件放入/etc/yum.repos.d/中

```bash
cp CentOS7-Base-163.repo /etc/yum.repos.d/

# 然后生成缓存
yum clean all
yum makecache
```

![在这里插入图片描述](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/27b7ca39ce6c419cd68af06fd49a272f/4030065ba0be8abd3be187e2f468258b.png)
6、检查

```bash
yum -v
yum list installed
```