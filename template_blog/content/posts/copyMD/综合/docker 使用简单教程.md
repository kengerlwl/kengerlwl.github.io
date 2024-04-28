---
title: docker 使用简单教程
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- docker
categories:
- 综合
---
# docker 学习与使用

## docker介绍
Docker：容器，可以理解成一个“黑盒”。在项目变得庞大以后，往往我们会疲于管理整个项目的部署和维护。如果我们将整个项目用一个“容器”装起来，那么我们仅仅只用维护一个配置文件告诉计算机每次部署要把什么东西装进“容器”，甚至借用一些工具把这个过程自动化，部署就会变得很方便。

### docker 结构
Docker 包含三个基本概念，分别是镜像（Image）、容器（Container）和仓库（Repository）。镜像是 Docker 运行容器的前提，仓库是存放镜像的场所，可见镜像更是Docker的核心。

## docker安装

- windows直接去官网下载应用程序
- linux可以直接用包管理工具下载安装包


## docker的配置

先在项目下创建一个文件`Dockerfile`。
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/04de0721475502582d05243cb2a52876.png)

编辑`Dockerfile`文件：
`Dockerfile`文件的详解[link](https://blog.csdn.net/qq_39626154/article/details/82787528)
我这里以一个flask项目为例。运行hello程序在`./app/test.py`
```
#基于的基础镜像
FROM python:3.7.9
#代码添加到flaskhello文件夹
ADD . /flaskhello
# 设置flaskhello文件夹是工作目录
WORKDIR /flaskhello


# 安装支持,安装依赖文件，执行前置，可以执行很多命令。
RUN pip install -r requirements.txt
CMD ["python", "./app/test.py"]  #最后运行的启动命令
```

**Dockerfile详解**
```
dockerfile常用命令
FROM：基础镜像，FROM命令必须是dockfile的首个命令
LABEL：为镜像生成元数据标签信息。
USER：指定运行容器时的用户名或UID，后续RUN也会使用指定用户
RUN：RUN命令是Dockfile执行命令的核心部分。它接受命令作为参数并用于创建镜像。每条RUN命令在当前镜像基础上执行，并且会提交一个新镜像层。
WORKDIR：设置CMD指明的命令的运行目录。为后续的RUN、CMD、ENTRYPOINT、ADD指令配置工作目录。
ENV：容器启动的环境变量
ARG：构建环境的环境变量
COPY：复制文件到镜像中,格式： COPY 源路径 目标路径 ：COPY指令和ADD指令功能和使用方式类似。只是COPY指令不会做自动解压工作。
ADD： 拷复制文件到镜像中,格式： ADD 源路径 目标路径
CMD：容器运行时执行的默认命令
ENTRYPOINT：指定容器的“入口”
HEALTHCHECK：容器健康状态检查
```

**关于CMD命令**：
一定要使得该命令运行后保持前台，否则容器就会自动关闭。这是docker容器本质上是进程的概念

## 构建镜像与运行

构建：
```

# 先跳转到项目根文件目录下（也就是含有Dockerfile的文件目录下）
docker build -t dockerdemo:v1 . # 最后一个.实际指定当前的构建目录，dockerdemo(注意只能用小写)是该docker的名字,v1是tag
```
结果
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/400a9154b13f51973f2af1c7b5c8b734.png)



运行
```
# 3000是你要映射到服务器上的端口，5000是容器里面需要被映射出来的端口，demo:v1 是需要运行的容器
docker run -p 3000:5000 demo:v1

```

![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/716b6dc2421ffa1448152017202cd5e4.png)

访问
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/b24c63c55a126b2741a895c42bcdd652.png)


## 容器的管理





## build指定运行中的环境变量

如果直接将一些参数写到Dockerfile是非常不安全的，所以一般是指定运行时环境变量。

`docker build --build-arg`用于传递构建参数给Docker构建过程中的Dockerfile文件。这些构建参数可在Dockerfile内使用，通过`${变量名}`格式访问。示例如下：

```
复制代码docker build --build-arg MY_VARIABLE=value .
```



## 删除不需要的镜像，和容器

查看所有的容器
```
docker ps -a
```
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/9b74ab04b47259728f163126d74802d5.png)


停止和删除容器
```
#如何停止容器
docker stop + 容器id
# 删除容器id
docker rm + 容器id

```

![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/4707628ce451d57e301f537b34d02107.png)


要先把镜像的容器都关了，才能删除相关镜像

查看当前有哪些镜像
```
docker images # 查看所有镜像及其信息

docker images -q  # 输出所有镜像的id
```
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/a26457f5d68c5ec899dfb58129f51712.png)

删除镜像
删除images（镜像），通过image的id来指定删除谁
```
docker rmi <image id>
```
要删除全部image（镜像）的话
```
docker rmi $(docker images -q)
```
只删除未被使用的资源
- Docker 提供了方便的 docker system prune 命令来删除那些已停止的容器、dangling 镜像、未被容器引用的 network 和构建过程中的 cache：
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/c4374d159824ee90df3e24e958427892.png)


在本地的镜像更新之后，就会出现类似图中红框内的 <none> 镜像。这表示旧的镜像已经不再被引用了，此时它们就变成了 dangling images。如果使用 -a 参数，你还会发现另外一种类型的 <none> 镜像，它们的 repository 和 tag 列都表现为 <none>：
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/893e772a3551604979a621e81834f2df.png)
    这些镜像被称为 intermediate 镜像(就是其它镜像依赖的层)。

**我们还可在不同在子命令下执行 prune，这样删除的就是某类资源：**
```
docker container prune # 删除所有退出状态的容器
docker volume prune # 删除未被使用的数据卷
docker image prune # 删除 dangling 或所有未被使用的镜像
```





## 容器的网络模式
[参考文](https://www.cnblogs.com/feng0815/p/14192177.html)

## port映射

不解释，不是最优解，但是有时候挺有用

## host模式

**Docker的host模式可以让容器直接使用宿主机的网络命名空间，即容器和宿主机使用相同的网络接口。**这种模式可以使得容器能够直接访问宿主机上的网络服务，并且不需要为容器暴露端口，因此可以获得更好的性能。**由于容器和宿主机共享网络命名空间，所以它们具有相同的IP地址、端口和网络配置，因此与主机在同一个网络上。**    

**如何主机有多个ip，docker容器也能够看到**

### 关于docker的端口映射增改问题。

一般来说，在镜像运行成容器后就不能再更改端口映射了，并且下次启动原来的映射配置也在。
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/48f85923d1c58a63157bf99adde19876.png)

想要改变两个办法。
**法一：**
    更改配置docker文件，具体上网查询
**法二：**
    把现在的容器commit成镜像，然后再把镜像运行成容器，并且在运行的时候声明端口映射。

## 进入容器内部
好文的连接[link](https://cloud.tencent.com/developer/article/1691352)
    
    
### 1,新建centos的镜像和容器。
```
docker pull centos
```
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/7732d980c9dba0fc5e0c2a40c5f09766.png)

### 2,对这个镜像创建容器（也就是说运行它）

    docker container run -it -p 8888:8080 -v /opt/app:/opt/app --name=python-server 470671670cac bash

命令文档查看：docker container run --help

-it : 交互式终端（interactive terminal） ，也就是创建容器后进入容器。

-p 8888:8080 :  端口映射（port），将容器端口映射到宿主机端口（8888：宿主机端口，8080：容器端口），宿主机端口 8888 确认能被外网访问。

-v /opt/app:/opt/app：数据卷（volumn），将宿主机的数据（应用程序代码，配置文件等等）挂载到容器指定路径下，实现数据存储的持久化（如果没有数据挂载的话，容器销毁，容器中的数据会自动消失）。

--name=python-server: 新的容器的名称

 470671670cac：镜像ID（imageID），当然也可以是 imageName + tag（docker.io/centos:latest）

bash：跟 -it 命令结合在一起操作，使容器创建后处于前端，一般是 /bin/bash，我这是bash。
    
结果：
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/f7fd50b701e2dad74e2c70e4c28dddaa.png)

查看所有容器
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/a4641ced6f18e89d2bb9e2a7924789a5.png)

**不中断退出容器**
可以通过 Ctrl+p，Ctrl+q 退出容器，但容器还是处于运行状态（Up）。
或者输入命令`exit`可以直接退出，但是容器也关闭了


#### 查看容器的信息（例如ip等）
`docker inspect container_id`

然后有结果


![image-20220821221517801](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/6d07b1501c4b634d8718374b41b828e7.png)    
### 进入容器

**方法一**
`docker container exec -it 5de4e81a2e20(containerID或者容器的名字) bash（这个bash可以换成其他命令）`

执行命令的方式：
- 先启动容器
- 然后使用exec命令去执行命令
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/ddfd8f4be65c4ef913eedff5cbe88412.png)


其他容器命令
```
容器其他相关操作命令：

查看容器 ip（退出容器，在宿主机上，最好另起一个客户端）: docker container inspect  1427087a62a7（containerID）


容器启动（交互式）：docker container start  -i containerID

关闭容器：docker container stop containerID

容器重启动：docker container restart containerID

删除容器（-f : force 强制删除，能删除处于运行状态的容器）：docker container rm -f  containerID

查看所有容器的容器ID：docker container ls -a -q

删除所有容器：docker contianer rm $(docker container ls -a -q)

在交互式容器中退出，退出启动容器： Ctrl + d

在交互式容器中退出，但是不退出启动容器：先按 Ctrl + p 后 Ctrl + q

使用 -d 启动容器并一直在后台运行 SSH作为第一进程启动：docker container run -d -p 50001:22 imageID /usr/sbin/sshd -D 
```


​    
### 容器内的使用

我这里用的centos最新版也就是centos8.
执行yum有个bug:`Failed to download metadata for repo 'appstream......`
办法是进入容器执行
```
cd /etc/yum.repos.d/
sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-* 
```

然后就可以使用yum安装各种库和程序了
    

**改变系统的密码**
```
    安装 passwd（设置密码）： yum install -y passwd
    设置密码：passwd root

```

**安装ssh并启动**

```
作为 python 服务的守护程序，防止容器闪退（一直夯在容器中）；

安装命令： yum install -y openssh-server

ssh 配置文件 sshd_config 路径： /etc/ssh/sshd_config

ssh 启动文件路径：/usr/sbin/
启动 SSH: /usr/sbin/sshd


```
启动前修改
修改/etc/ssh/sshd_config这个ssh配置文件
    
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/315c39e1cfc901608d72456af0a85ce1.png)

退出后访问


### 将容器打包成镜像

在运行容器时指定映射端口运行后，如果想要添加新的端口映射，可以使用以下两种方式：

**方式一：将现有的容器打包成镜像，然后在使用新的镜像运行容器时重新指定要映射的端口**

大概过程如下：

先停止现有容器

`docker stop container-name`
将容器commit成为一个镜像

`docker commit container-name  new-image-name`
用新镜像运行容器
    
结果
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/84b4c22dcec687cb8738be54bdf5b6d1.png)

然后运行新的镜像
`docker run -it -d --name container-name（or id） -p p1:p1 -p p2:p2 new-image-name`

两个 -p 指定多个端口映射

**宿主机ssh连接入容器  **  

我这里将外部的2020端口映射到容器里面的22端口。
用特定的连接工具**MobaXterm**
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/33f1657022f4724b85c3b89bff23f464.png)

然后输入用户名和密码：成功
![](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/91e15ed4a577cd55d7e4a4843d293fe7/9fbb228cc98997fb48f0fcfddad37492.png)

## docker Hub的使用

先在hub中建立一个名叫centos_demo的仓库，我的用户名是`${username}`

在本地登录docker
```
#docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: ${username}
Password:
Login Succeeded
```

准备在本地提交，先给images打标签

```
docker tag 镜像名 账号名/仓库名：版本号
账号名是登陆的账号名，仓库是远端配置的仓库名，版本号自己定义一个就好。到时候pull下来也是pull这个账号名/仓库名：版本号就好
```

然后提交镜像push
```
docker push 账号名/仓库名：版本号
```