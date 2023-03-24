---
title: linux挂载
top: false
cover: false
toc: true
mathjax: true
date: 2023-03-12 15:27:31
password:
summary:
tags:
- 服务器
- linux
- mount
categories:
- 服务器
---



# 安装必要库

```
sudo apt install nfs-common
```



# 启动就挂载



### 说明

要挂载某个盘到某个目录下面。要保证该目录已经存在

### 配置

`/etc/fstab`文件

```
Last login: Mon Mar 20 22:14:35 2023 from 127.0.0.1
[root@core-labot ~]# cat /etc/fstab 

#
# /etc/fstab
# Created by anaconda on Sun Oct 10 04:29:36 2021
#
# Accessible filesystems, by reference, are maintained under '/dev/disk'
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
#
/dev/mapper/centos-root                         /                                       xfs     defaults                0 0
UUID=18255ddd-b54f-450a-a75c-b7d475858905       /boot                                   xfs     defaults                0 0
/dev/mapper/centos-swap                         swap                                    swap    defaults                0 0
zvol.csubot.cn:/mnt/matrix/Data-Core            /mnt/DataCore                           nfs4    defaults,_netdev        0 0
/mnt/DataCore                                   /www/wwwroot/file.csuoss.cn/DataCore    none    defaults,bind           0 0
```





# 挂载nas



## 检查盘

检查目标nas的盘

```
showmount -e zvol.csubot.cn


robot@gpu2-labot:~$ showmount -e zvol.csubot.cn
Export list for zvol.csubot.cn:
```





## 挂载

挂载-t nfs 指的是目标盘的类型，不是自己linux的文件系统。

```
sudo mount -t nfs zvol.csubot.cn:/mnt/matrix/Data-Core  /www/wwwroot/file.csuoss.cn/Data-Core
```

