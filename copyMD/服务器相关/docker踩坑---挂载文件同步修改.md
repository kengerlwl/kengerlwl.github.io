---
title: docker踩坑---挂载文件同步修改
top: false
cover: false
toc: true
mathjax: true
date: 2023-06-10 15:27:31
password:
summary:
tags:
- 服务器
- docker
categories:
- 服务器
---


# 需求

最近想要实现这样一个功能，由于目标机器过于陈旧，不能良好的安装运行环境。所以决定用docker封装好。

该程序需要再运行的时候即使修改宿主机部分文件，并且修改后，要在宿主机上执行部分命令。





## 坑1------我是直接挂载文件，但是挂载后，我在容器内修改了文件，容器外无反应



原因：

docker挂载文件时，并不是挂载了某个文件的路径，而是挂载了对应的文件，即挂载了linux指定的`inode`文件。

当使用vim之类的编辑器进行保存时，它不是直接保存文件，而是采用了`备份、替换`的策略，就是编辑时，是创建一个新的文件，在保存的时候，把备份文件替换源文件，这个时候文件的 `inode` 就发生了变化，而原来 `inode` 对应的文件其实并没有修改，也就是容器内的文件没有变化。当重启容器的时候，会挂载新的 `inode`





## solution

直接挂载目录