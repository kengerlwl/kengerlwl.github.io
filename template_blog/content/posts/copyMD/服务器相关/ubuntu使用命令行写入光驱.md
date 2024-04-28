---
title: ubuntu使用命令行写入光驱
top: false
cover: false
toc: true
mathjax: true
date: 2023-11-20 15:27:31
password:
summary:
tags:
- 服务器
- linux
categories:
- 服务器
---
ubuntu使用命令行写入光驱



# 背景

有相关的需求



# 方法

## 制造ISO镜像

```
mkisofs -o output.iso -J -r ./Test
```



## 将镜像写入光盘

```
wodim -v dev=/dev/sr0 speed=4 -eject -dao -data output.iso
```

这里的 `-dao` 表示使用 Disc-At-Once 写入模式，适用于数据光盘。如果你在写入音频光盘，可能需要使用 `-tao` 模式。
