---
title: linux Ubuntu通过systemd 添加开机自动启动程序方法
top: false
cover: false
toc: true
mathjax: true
date: 2023-05-05 15:27:31
password:
summary:
tags:
- 服务器
- linux
- 开机启动脚本
categories:
- 服务器
---
# 机器

ubuntu 22



# 流程

## 建立Systemd 服务单元配置文件

建立一个新的Systemd 服务单元配置文件，储存于`/etc/systemd/system/echo_server.service`：

```

[Unit] 

Description= Echo Server

[Service] 

 Type= simple

 ExecStart= /opt/echo_server.py

 Restart= always

[Install] 

WantedBy= multi-user.target

```

权限要设定为`644`：

```bash
sudo chmod 644 /etc/systemd/system/echo_server.service
```

如果在开发过程中，有修改过Systemd 的服务单元配置文件，记得重新载入daemon 让新设置生效：

\# 重新载入Systemd 配置文件 

`sudo systemctl daemon-reload`

接着就可以使用 `systemctl` 命令启动自定义的echo 服务器：

\# 启动自定义的echo 服务器

`sudo systemctl start echo_server`

查看echo 服务器的状态：

\# 查看echo 服务器状态

`systemctl status echo_server`



## 常见systemctl的命令

允许开机自启：

```bash
systemctl enable scratch.service
```

其他命令

```bash
启动 sudo systemctl start scratch
重启 sudo systemctl restart scratch
停止 sudo systemctl stop scratch
日志 sudo systemctl status scratch
```



## 注意

要给足文件权限。



## 一个frp的demo

```
[Unit]
Description=frp service
After=network.target network-online.target syslog.target
Wants=network.target network-online.target

[Service]
Type=simple

#启动服务的命令（命令必须写绝对路径）
ExecStart=bash /home/m1ld/.test/frp_0.45.0_linux_amd64/run_frps.sh

# 停止服务后，执行的命令
ExecStop=ps -aux | grep frp | awk '{print $2}' | xargs kill -9

[Install]
WantedBy=multi-user.target
```





## Systemd 服务单元配置文件说明:

```
[Unit] 
# 服务名称
Description= Your Server

# 服务相关文件
# Documentation=https://example.com 
# Documentation=man:<a class="wpal-linked-keyword" href="https://nginx.p2hp.com/" target="_blank">nginx</a>(8)

# 设定服务启动的先后相关姓，例如在网络启动之后：
# After=network.target

[Service] 
# 进程类型
Type= simple

# 启动服务命令
ExecStart=bash/sh /opt/your_command

# 服务进程PID（通常配合forking 的服务使用）
# PIDFile=/run/your_server.pid

# 启动服务前，执行的命令
# ExecStartPre=/opt/your_command

# 启动服务后，执行的命令
# ExecStartPost=/opt/your_command

# 停止服务命令
# ExecStop=/opt/your_command

# 停止服务后，执行的命令
# ExecStopPost=/opt/your_command

# 重新载入服务命令
# ExecReload=/opt/your_command

# 服务终止时自动重新启动
# Restart= always

# 重新启动时间格时间（预设为100ms）
# RestartSec=3s

# 启动服务超时秒数
# TimeoutStartSec=3s

# 停止服务超时秒数
# TimeoutStopSec=3s

# 执行时的工作目录
# WorkingDirectory=/opt/your_folder

# 执行服务的用户（名称或ID 皆可）
# User=myuser

# 执行服务的群组（名称或ID 皆可）
# User=mygroup

# 环境变数设置
# Environment="VAR1=word1 word2" VAR2=word3 "VAR3=$word 5 6"

# 服务输出信息指向设定
# StandardOutput=syslog

# 服务错误信息息指向设定
# StandardError=syslog

# 设定服务在Syslog 中的名称
# SyslogIdentifier=your-server

[Install] 
WantedBy= multi-user.target
```





# ref

[https://blog.p2hp.com/archives/8690](https://blog.p2hp.com/archives/8690)









