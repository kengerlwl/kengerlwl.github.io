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



**如何用bash启动一个什么也不执行的容器**





注意，如果您尝试同时使用 `-it` 和 `-d`，**则Docker会忽略 `-it` 选项**，并将 `-d` 的行为应用于容器。例如，以下命令会在后台启动一个交互式终端并立即返回控制台：

```
docker run -it -d --name my-container ubuntu
```



# 说明

以下实验，我以一个数据库**tdengine**为例：

### 正常后台启动

```
sudo docker run -d  --name tdengine_d   tdengine/tdengine:2.4.0.7 

```

进入容器查看其进程

```
root@7fe2ac01f161:~/TDengine-server-2.4.0.7# ps -aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   4632  1744 ?        Ss   12:56   0:00 /bin/sh /usr/bin/entrypoint.sh taosd
```

可以看到官方的启动命令`/bin/sh /usr/bin/entrypoint.sh taosd`

### 交互界面执行启动(然后放入后台)

```
sudo docker run -it  --name tdengine_it   tdengine/tdengine:2.4.0.7 bash

```

然后此时我们使用**Ctrl+P**或**Ctrl+Q**的方式退出容器的控制台，此时容器就会在后台运行。

进入容器查看其进程

```
root@019c7bcd3a90:~/TDengine-server-2.4.0.7# ps -aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.1  0.0   4632  1588 pts/0    Ss   13:33   0:00 /bin/sh /usr/bin/entrypoint.sh bash
```



### itd一次性搞定性的命令

```
sudo docker run -it -d  --name tdengine_itd   tdengine/tdengine:2.4.0.7 bash
```

进入容器查看其进程

```
root@9f920168e499:~/TDengine-server-2.4.0.7# ps -aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.4  0.0   4632  1624 pts/0    Ss   13:36   0:00 /bin/sh /usr/bin/entrypoint.sh bash
```





# ref

https://blog.csdn.net/acmman/article/details/83927649
