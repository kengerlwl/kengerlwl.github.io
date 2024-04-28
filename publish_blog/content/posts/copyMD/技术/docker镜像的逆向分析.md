---
title: docker镜像的逆向分析
top: false
cover: false
toc: true
mathjax: true
date: 2023-05-17 15:27:31
password:
summary:
tags:
- web api
- cgi
categories:
- 综合
---



# 需求

目前我需要在一台神奇的服务器上部署一个数据库，但是由于权限问题，我不能让容器按照默认的守护进程直接启动，我需要进入容器更改完我需要做的一些修改后，再手动启动数据库。

那么问题来了，在修改完配置后，我如何才能知道该容器原有的启动命令是多少呢?





**如何用bash启动一个什么也不执行的容器**



注意，如果您尝试同时使用 `-it` 和 `-d`，**则Docker会忽略 `-it` 选项**，并将 `-d` 的行为应用于容器。例如，以下命令会在后台启动一个交互式终端并立即返回控制台：

```
docker run -it -d --name my-container ubuntu
```



# 方案

 ### 方法1

```
docker inspect <id>
```



### 方法2

- 先正常随便run一个能运行的指定容器出来
- 然后进入该容器查看其启动命令是那些

```
root@7fe2ac01f161:~/TDengine-server-2.4.0.7# ps -aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   4632  1744 ?        Ss   12:56   0:00 /bin/sh /usr/bin/entrypoint.sh taosd
root          36  0.0  0.0 2391080 52956 ?       Sl   12:56   0:00 taosadapter
root          62  0.5  0.0 3256468 20100 ?       Sl   12:56   0:05 taosd -c /tmp/taos
root         191  0.0  0.0  20184  3728 pts/0    Ss   12:56   0:00 bash
root         374  0.0  0.0  36080  3284 pts/0    R+   13:13   0:00 ps -aux
```

可以看到命令是`/bin/sh /usr/bin/entrypoint.sh taosd`

然后成功work
