---
title: openwrt系统镜像打包
top: false
cover: false
toc: true
mathjax: true
date: 2023-09-09 15:27:31
password:
summary:
tags:
- linux
- openwrt
categories:
- 网络
---

# 背景

我已经有了一台`openwrt`的系统，我想将目前的配置打包为img镜像。

下次刷入即用。为什么不考虑esxi虚拟机直接迁移呢，因为想打包成精简的img包。

# 方法

先看看目前占用的内存，这将决定后面导出的img包的大小

![image-20230909224156157](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/00ae1fc546ca2c05ae298424b8e9632b/8e9413f7058186ee23805e9e4f82286e.png)

从图中我们不难看出。目前系统是在/dev/sda上面的。

我们需要将该盘上的数据打包为镜像img。

我们插入另一个U盘`/dev/sdb1`

然后将数据打包到该盘。

# DD命令

挂载目标盘，然后导出到目标盘

```
root@OpenWrt:~# mount /dev/sdb1 /mnt/
root@OpenWrt:~# dd if=/dev/sda of=/mnt/backup.img count=4048 bs=1024k  conv=sync
```

等待dd命令运行完成后，就得到了RAW格式的backup.img镜像

dd命令参数的含义：

- if=文件名：输入文件名，缺省为标准输入。即指定源文件。< if=/dev/sdb >
- of=文件名：输出文件名，缺省为标准输出。即指定目的文件。< of=./backup/backup.img, 这里的.img是镜像的格式，转成.img格式的文件后方便后续使用etcher烧录镜像 >
- bs = bytes：同时设置读入/输出的块大小为bytes个字节，此处填的是1024k，表示1M大小。
- count = blocks：仅拷贝blocks个块，块大小等于ibs指定的字节数，此处设置的是2048， 表示2048个bs，也就是2g。
- conv= sync：将每个输入块填充到ibs个字节，不足部分用空（NUL）字符补齐。



# 注意

要仔细算好需要的空间，千万不能不足。





# ref

[系统镜像备份并重新烧录](https://doc.embedfire.com/linux/rk356x/build_and_deploy/zh/latest/building_image/image_backup/image_backup.html)

