---
title: openwrt 添加开机自动启动脚本
top: false
cover: false
toc: true
mathjax: true
date: 2023-04-22 15:27:31
password:
summary:
tags:
- openwrt
- 开机启动脚本
categories:
- 网络
---

# 背景

需要再openwrt上实现一个开机后一段时间再执行某个脚本

于是决定使用开机自动启动脚本机制。

为什么 不考虑`/etc/rc.local`

1. **执行时机**：
   - `/etc/rc.local`：在系**统引导过程的最后阶段执行**，通常是在其他系统初始化脚本执行完毕后执行。这意味着它是在系统启动的相对较晚阶段执行的。
   - `/etc/init.d`：这是一个目录，其中包含了各种系统服务的启动脚本。这些脚本在系统引导时按照其配置的优先级顺序执行，因此它们在系统启动的不同阶段可能会有不同的执行时机。
2. **用途**：
   - `/etc/rc.local`：通常用于执行一些简单的自定义任务、脚本或命令，例如启动特定的应用程序、设置环境变量或执行一些初始化操作。它适用于一些不需要复杂服务管理的情况。
   - `/etc/init.d`：这个目录包含了系统服务的启动和停止脚本。这些脚本用于管理系统中的服务，如网络、打印机、防火墙等。它提供了更丰富的功能，包括服务的启动、停止、重新启动、状态查询等。
3. **管理**：
   - `/etc/rc.local`：通常只包含一个文件 `/etc/rc.local`，你可以编辑此文件并在其中添加自定义命令。它不涉及特定的服务管理。
   - `/etc/init.d`：包含了多个服务脚本，每个脚本都与一个特定的服务相关联。你可以使用 `service <servicename> start/stop/restart/status` 命令来管理这些服务。



# 方法



首先，在 /etc/init.d 目录中新建一个文件，文件名为自己定义，例如`/etc/init.d/myscript` 然后在文件中加入如下内容：

```bash
#!/bin/sh /etc/rc.common

START=199
STOP=200
start() {
    #sleep 120  # 延迟两分钟执行
    /root/start_server.sh  # 您的脚本路径和名称
}

reload() {
    echo "Reloading myscript"
}

stop() {
    echo "Stopping myscript"
}

restart() {
        echo "myscript  is restart"
}

```

最后设置权限，使其可执行

```bash
chmod +x /etc/init.d/myscript
```

# 增加开机启动脚本操作：

我们需要把增加的脚本放入`/etc/init.d`:

- 例如增加一个脚本保存为 `/etc/init.d/myscript`
- 将脚本设置为可执行文件，使用以下命令,`chmod +x /etc/init.d/myscript`
- 将脚本添加到系统启动脚本中，使用以下命令,`/etc/init.d/myscript enable`
- 如果想要在开机时立即启动脚本，可以使用以下命令,`/etc/init.d/myscript start`
- 如果想要停止脚本，可以使用以下命令`/etc/init.d/myscript stop`
- 如果想要重新启动脚本，可以使用以下命令`/etc/init.d/myscript restart`
- 如果想要查看脚本的状态，可以使用以下命令,`/etc/init.d/myscript status`

# ref

[https://blog.csdn.net/qq_41453285/article/details/102545624](https://blog.csdn.net/qq_41453285/article/details/102545624)
