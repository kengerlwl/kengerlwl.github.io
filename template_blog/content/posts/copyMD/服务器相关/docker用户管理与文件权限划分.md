---
title: docker用户管理与文件权限划分
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
- docker
categories:
- 服务器
---
# 需求

实验室本来是给所有用户都开启了sudo使用`docker`的权限。

出现了一些问题：

- 存储问题：由于docker使用容器用的是root用户。导致一些root用户没有权限的文件夹挂载访问不了。
  - 例如我这里有个nas，nas挂载在宿主机的/data。但是这个nas只能让csuoss用户组里的用户访问，root不在这个用户组。而且docker里面并没有继承宿主机的group信息。所以不能docker挂载该目录。这对一些大型数据库很不友好。

- 用户容器进程区分问题： 部分用户通过docker运行了一些不合理的进程。导致了服务器有了一些问题。但是由于是sudo运行的，基本上都是root用户的进程，我根本找不到是谁的程序。所以决定把这个问题也解决一下。





# 实操

在gpu2上有个nas挂载目录，只有csuoss目录组才有权限。而root不是该用户组的。

默认root用户运行命令。（注意，待挂载的目录必须是个空目录`/data/DataLACP/mysql_b`）

```
sudo docker run --rm --name=mysql_lxy  -v /data/DataLACP/mysql_b:/var/lib/mysql/data -it -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql /bin/bash
```

新建脚本

```
#!/bin/bash

# 设置变量
NEW_USER="mysql"
NEW_UID="212047"
NEW_GROUP="csuoss"
NEW_GID="212000"

# 创建新组
groupadd -g $NEW_GID $NEW_GROUP

# 创建新用户
useradd -u $NEW_UID -g $NEW_GID -G $NEW_GROUP $NEW_USER

```

## sqlserver实操

- 还是用docker运行该容器
- 但是将该容器内所有用户都加入某个具备该权限的用户组，本文是csuoss。
- 然后就会发现可以读取了



```
# docker 启动命令
docker run --name=sqlserver -it \
-e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=8580555@Mf' -e 'MSSQL_PID=Enterprise' \
--net host \
-p 1433:1433  \
-v /data/DataLACP/mssql_data:/var/opt/mssql \
-d mcr.microsoft.com/mssql/server bash




# 将所有用户都加入某个用户组(注意，其中某些用户只有root才能执行，请在docker中先用root登录)

NEW_GROUP="csuoss"
NEW_GID="212000"

# 创建新组
groupadd -g $NEW_GID $NEW_GROUP
#!/bin/bash
groupadd -g 212000 csuoss
# 将所有用户添加到csuoss组
for user in $(getent passwd | cut -f1 -d:); do
  #echo $user
  usermod -a -G csuoss $user
done

```



查看某个组的用户（但是这个命令获取的所有用户并不全）

```
getent group csuoss
```











**注意：**

**修改用户分组前要保证**

1. **用户不能正在登录**：如果要修改的用户当前正在登录系统，则无法直接更改其用户组。在修改用户组之前，请确保用户已注销或关闭所有与其相关的会话。
2. **用户不能正在运行进程**：如果用户有正在运行的进程，则无法直接修改其用户组。这可能是由于用户正在运行某些服务或应用程序。首先结束用户的所有进程，然后再尝试修改其用户组。

**linux修改用户所属于的组后，不会立刻生效。**

- 要么退出当前会话重新登录
- docker的话可以直接重新运行容器
- su - $USER : 使用这个命令重新开始一个 session ， 并重新继承当前环境。

```
su - $USER
```





## 坑

对于挂载的特定用户组才能访问的nas目录，很奇怪。当即使我们刷新了用户权限后，如下：

```
root@gpu2-labot:/var/opt# id
uid=0(root) gid=0(root) groups=0(root),999(mssql),212000(csuoss)
```

**对于root用户而言仍然是不可以访问的。**

但是对于其他非root用户，mssql或者其他用户自建的用户则都可以访问。







### 启动server

```
/opt/mssql/bin/sqlserver
```



初始化

```
/opt/mssql/bin/mssql-conf setup 
```

程序启动命令

```
(/opt/mssql/bin/sqlservr --accept-eula & ) | grep -q "Service Broker manager has started" &&  /opt/mssql-tools/bin/sqlcmd -S127.0.0.1 -Usa -P8580555@Mf -i filldata.sql
```

进入cli工具

```
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "8580555@Mf"
```





## Tdengine:2.4.0.7

```
docker pull tdengine/tdengine:2.4.0.7
```



```
sudo docker run --rm -it --name tdengine_1  -v /data/DataLACP/td_data:/tmp1  \
-p 6030:6030 -p 6035:6035 -p 6041:6041 -p 6030-6040:6030-6040/udp tdengine/tdengine:2.4.0.7 bash
```





# 如何用docker进行用户管理

在网上查到了一个解决方案。能够有效进行docker用户的资源监控。

### 另一个作者原理

由于docker容器创建时并不会记录创建者的信息，所以没法锁定已经创建的容器的所有者，因此需要设法在容器创建时将容器创建者的信息记录下来。我的方法是在容器创建时给容器定义一个特殊的环境变量，并将创建者的宿主机用户名字符串设置到这个容器中的环境变量中。

```
docker run -itd -e CONTAINER_CREATED_USER=$(whoami) ubuntu /bin/bash
```

通过 `docker inspect <container-name>` 指令可以获取容器内的环境变量，由此，通过docker容器名获得容器创建者的用户名。

`docker top aux` 指令可以通过容器名获取容器内的进程信息，由此可以判断出进程的创建者。

结合以上指令，只需要让写一个类似top的资源管理器，将其中的user信息显示为进程所属容器的创建者名。为了方便开发，我直接使用在[ctop](https://github.com/bcicen/ctop)的基础上修改。





## 个人思路

## 1 将所有csuoss组的用户都加入docker用户组

另一种方式

```
csuoss_gid=212000
for user in $(getent passwd | grep $csuoss_gid |  cut -f1 -d:); do
  echo $user
  usermod -a -G docker $user
done
```

因为用户执行docker的方式不能通过sudo。否则会读取不到当前用户的环境变量。因此，只能将所有用户都加入到docker用户组





### 获取该容器的用户属性

```
#!/bin/bash

get_container_env_vars() {
    container_id="$1"

    # 输入待处理字符串
    str=$(sudo docker inspect --format='{{range $k, $v := .Config.Env}}{{$v}} {{end}}' "$container_id")

    # 定义一个关联数组
    declare -A my_dict

    # 分割字符串并获取键值对
    for pair in $str; do
        key=$(echo "$pair" | cut -d'=' -f1)
        value=$(echo "$pair" | cut -d'=' -f2)
        my_dict[$key]=$value
    done

    # 输出结果
    echo "目标容器的env："
    for key in "${!my_dict[@]}"; do
        echo "$key: ${my_dict[$key]}"
    done

    # 查看指定属性的变量
    echo ""
    echo "目标容器的运行用户为："
    echo ${my_dict["CONTAINER_CREATED_USER"]}
}

# 使用示例：find_container_user.sh -c container_id
if [ "$1" == "-c" ]; then
    container_id="$2"
    get_container_env_vars "$container_id"
fi

```

**使用**

```
find_container_user.sh -c 容器id

alias find_container_user=\"/home/labot/lib/find_container_user.sh\"
```





### 查找给定PID所属Docker容器的脚本：

```
#!/bin/bash

get_container_id() {
    while getopts "p:" opt; do
        case $opt in
            p) pid=$OPTARG ;;
            \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
        esac
    done

    if [ -z "$pid" ]; then
        echo "请使用 -p 参数指定进程的 PID"
        exit 1
    fi

    # 使用 cgroup 查找 PID 所属的容器 ID
    container_ids=$(awk -F/ '$2 == "docker"{ print $(NF-0) }' /proc/"$pid"/cgroup | sort -u)

    # 输出结果
    if [ -z "$container_ids" ]; then
        echo "该进程没有在任何 Docker 容器中运行！"
    else
        echo "该进程所属的 Docker 容器 ID 为：$container_ids"
    fi
}

# 使用示例：find_container_id.sh -p pid
get_container_id "$@"

```

**使用**

```
$ ./find_container.sh -p 12345
```







### 覆盖原有的docker命令

新的docker命令脚本

```
#!/bin/bash
docker_command=docker
ctop_command=ctop

if [ $1 == "run" ]
then
    $docker_command run -e CONTAINER_CREATED_USER=$(whoami) ${@:2}
else
    $docker_command $@
fi
```

别名，要对所有用户生效，加入`/etc/profile`

```
echo "alias docker=\"docker_wrapper.sh\"" >> /etc/bash.bashrc
```

然后每隔几秒检查一下，更新所有csuoss用户组的用户到docker用户组。

最后使用方式是，普通1用户登录后可以直接使用docker命令，无需root。





# docker cuda

 Ubuntu 22.10 安装：

```bash
distribution=ubuntu22.04 && \
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && \
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

命令执行完毕之后，我们的系统中就添加好了 Lib Nvidia Container 工具的软件源啦，然后更新系统软件列表，使用命令安装 `nvidia-container-toolkit` 即可：

```bash
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
```

完成 `nvidia-container-toolkit` 的安装之后，我们继续执行 `nvidia-ctk runtime configure` 命令，为 Docker 添加 `nvidia` 这个运行时。完成后，我们的应用就能在容器中使用显卡资源了：

```bash
sudo nvidia-ctk runtime configure --runtime=docker
```

命令执行成功，我们将看到类似下面的日志输出：

```bash
# sudo nvidia-ctk runtime configure --runtime=docker

INFO[0000] Loading docker config from /etc/docker/daemon.json 
INFO[0000] Successfully loaded config                   
INFO[0000] Flushing docker config to /etc/docker/daemon.json 
INFO[0000] Successfully flushed config                  
INFO[0000] Wrote updated config to /etc/docker/daemon.json 
INFO[0000] It is recommended that the docker daemon be restarted. 
```

在完成配置之后，别忘记重启 docker 服务，让配置生效：

```bash
sudo systemctl restart docker
```

服务重启完毕，我们查看 Docker 运行时列表，能够看到 `nvidia` 已经生效啦。

```bash
# docker info | grep Runtimes

 Runtimes: nvidia runc io.containerd.runc.v2
```



## 测试

```
git clone https://github.com/wilicc/gpu-burn
cd gpu-burn
docker build -t gpu_burn .
docker run --rm --gpus all gpu_burn
```





# ref

[Docker多用户资源监控解决方案](https://yuxinzhao.net/docker-multi-user-solution)
