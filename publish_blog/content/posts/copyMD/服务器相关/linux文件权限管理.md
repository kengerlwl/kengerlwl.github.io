---
title: linux文件权限管理
top: false
cover: false
toc: true
mathjax: true
date: 2023-03-20 15:27:31
password:
summary:
tags:
- 文件权限管理
- linux
- mount
categories:
- 服务器
---



# 说明

使用的工具

- setacl、getacl命令
- 安装`sudo apt-get install acl`
- 对挂载的盘进行支持

1、手动挂载

```
mount -o acl /dev/mapper/vg_server1-logs /home
[root@excbjdcpapp05 usr]# mount -l
/dev/mapper/VolGroup-lv_root on / type ext4 (rw)
proc on /proc type proc (rw)
sysfs on /sys type sysfs (rw)
devpts on /dev/pts type devpts (rw,gid=,mode=)
tmpfs on /dev/shm type tmpfs (rw)
/dev/sda1 on /boot type ext4 (rw)
none on /proc/sys/fs/binfmt_misc type binfmt_misc (rw)
/dev/mapper/vg_server1-logs on /home type ext4 (rw,acl)
```

2、编写fstab文件

```
vi /etc/fstab
/dev/mapper/vg_server1-logs       /home         ext4    defaults,acl       0 
```

然后重新挂载

```
mount -o remount /home
```
