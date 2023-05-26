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
docker run --name=sqlserver --rm -it \
-e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=8580555@Mf' -e 'MSSQL_PID=Enterprise' \
--net host \
-p 1433:1433  \
-v /data/DataLACP/mssql_data:/var/opt/mssql \
-d mcr.microsoft.com/mssql/server bash




# 将所有用户都加入某个用户组(注意，其中某些用户只有root才能执行，请在docker中先用root登录)

#!/bin/bash
groupadd -g 212000 csuoss
# 将所有用户添加到csuoss组
for user in $(getent passwd | cut -f1 -d:); do
  #echo $user
  usermod -a -G csuoss $user
done

```



查看某个组的用户

```
getent group csuoss
```

**注意：**

linux修改用户所属于的组后，不会立刻生效。

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
(/opt/mssql/bin/sqlservr --accept-eula & ) | grep -q "Service Broker manager has started" &&  /opt/mssql-tools/bin/sqlcmd -S127.0.0.1 -Usa -PabcDEF123# -i filldata.sql
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



### 获取该容器的用户属性

```
#!/bin/bash

# 输入待处理字符串
str=$(sudo docker inspect --format='{{range $k, $v := .Config.Env}}{{$v}} {{end}}' 8a33787a0ba9aa714dcfdbf1290d6e67971ce45de6d2b3ec949809def1a52730)

# 定义一个关联数组
declare -A my_dict

# 分割字符串并获取键值对
for pair in $str; do
    key=$(echo $pair | cut -d'=' -f1)
    value=$(echo $pair | cut -d'=' -f2)
    my_dict[$key]=$value
done

# 输出结果
for key in "${!my_dict[@]}"; do
    echo "$key: ${my_dict[$key]}"
done

# 查看指定属性的变量
echo ${my_dict["CONTAINER_CREATED_USER"]}
```



### 查找给定PID所属Docker容器的脚本：

```
#!/bin/bash

# 获取指定进程pid
pid=2111388

# 使用cgroup查找PID所属的容器ID,,,这里的NF-0。代表从后面数第一个。
container_ids=$(awk -F/ '$2 == "docker"{ print $(NF-0) }' /proc/$pid/cgroup | sort -u)
echo $container_ids
# 输出结果
if [ -z "$container_ids" ]; then
    echo "该进程没有在任何Docker容器中运行！"
else
    echo "该进程所属的Docker容器ID为：$container_ids"
fi

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

别名

```
echo "alias docker=\"docker_wrapper.sh\"" >> /etc/bash.bashrc
```





# ref

[Docker多用户资源监控解决方案](https://yuxinzhao.net/docker-multi-user-solution)
