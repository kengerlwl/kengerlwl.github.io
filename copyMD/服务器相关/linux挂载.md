```
title: linux挂载
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
- mount
categories:
- 服务器
```



# 安装必要库

```
sudo apt install nfs-common
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

