---
title: esxi 虚拟交换机
top: false
cover: false
toc: true
mathjax: true
date: 2023-03-06 15:27:31
password:
summary:
tags:
- 虚拟交换机
- esxi
categories:
- 运维

---







# 虚拟交换机



### 添加管理标准虚拟交换机

**一般虚拟交换机示意图**

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/39867dfe28a5c1f5410ca5adb6389560/b465da262814a9dfac29e83fbee9483b.png)



在vSphere的网络配置里，虚拟交换机分为

- 标准交换机（Virtual Standard Switch)（**更常用**）
- 分布式交换机(Virtual Distributed Switch)，

进入vcsa集中管理界面

![image-20230316154503385](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/39867dfe28a5c1f5410ca5adb6389560/4a6d90a62dc0af6d89c1bb544c9f3566.png)



### 在一个标准虚拟交换机里，我们可以设置三类连接类型

![img](https:////upload-images.jianshu.io/upload_images/9635611-366f1f1952a12f25.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200/format/webp)

虚拟交换机连接类型

1. **VMkernel网络适配器，这种连接类型是ESXi用来主机管理（通常所说的ESXi管理口**（**一般是进入到esxi的那个ip分配））**，vMotion，iSCSI，NFS等服务的流量使用的连接类型，我们可以把不同的服务分到不同的VMkernel适配器上，也可以分配到同一个VMkernel适配器上，一般简写成vmk0,vmk1......VMkernel适配器需要分配IP地址，**以vmk0作为主机管理端口为例，如它设置了IP地址192.168.1.50，我们就可以在局域网内通过192.168.1.50来管理这台ESXi主机。**

2. **虚拟机端口组/PortGroup，端口组可以理解成虚拟机和虚拟交换机之间连接的一种模板。或者说，是用来连接我们创建的虚拟机的接口**，一般说来，虚拟机是将虚拟网卡连接到虚拟交换机上的端口组/PortGroup的一个端口上(想像成一台电脑的网线从物理网卡连接到了物理交换机上）来做网络交换（虚拟机使用直通的网络设备除外）。在创建端口组时还可以设置VLAN ID，这样同一个虚拟交换机下面还可以通过不同端口组来做VLAN隔离。

![image-20230316160845429](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/39867dfe28a5c1f5410ca5adb6389560/6c6a92927024f65a88cca8d4fad7f22f.png)端口组VLAN ID**可以选择配置vlan**

![image-20230316160910122](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/39867dfe28a5c1f5410ca5adb6389560/483a5482a72bfe818bd9713cae7944b4.png)

3.**物理网络适配器，这是虚拟交换机和物理交换机连接的物理载体**，桥梁。从示意图中，我们看到虚拟交换机中有一个端口（可以有多个）叫做上行链路/Uplink port，上行链路和物理网卡连接在一起，这个物理网卡在vSphere里可以标记为VMNIC, PNIC,UPLink，物理网卡作为连通虚拟网络和物理网络的桥梁，通常来说它本身不和IP地址绑定，所以当我们给ESXi主机分配IP时，并不是直接分配给了它的物理网卡，而是分配给了VMkernel适配器。





### 典型交换组拓补图demo

这就是一个很典型拓补图。这个图里面只有我们创建的虚拟机，

![image-20230316160647651](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/39867dfe28a5c1f5410ca5adb6389560/081b0e47cc682273bdbc4683d6e59043.png)





### 分布式交换机

为什么需要分布式交换机？：标准交换机不能集中管理

**标准交换机是通过ESXi主机来创建和管理的，这就意味着当你有多台ESXi主机时，你就要分别去每一台ESXi上创建标准交换机里的端口组等设置**，可能这个工作量还不算什么，但是当一年之后你要去修改端口组，或者扩展端口组呢？

说明：

- 分布式交换机不是在ESXi主机上创建的，而是vCenter。



**里面的链路数目要根据自己这边有几个活跃的物理网卡进行选择**

![image-20230316154911509](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/39867dfe28a5c1f5410ca5adb6389560/b4bef61fe608766a8e15219a48b14ce7.png)

如果重新安装了VCSA导致原来的分布式交换机不能更改配置了。**那么可以从这里选择新建然后导入原有的配置**



### 新建虚拟机时选择端口组

**一般的虚拟机都是通过端口组连接到虚拟交换机的。这也是新建虚拟机时网络适配器需要选择的项**

![image-20230316161310257](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/39867dfe28a5c1f5410ca5adb6389560/3e35190c5875333184f560446d9e7eb6.png)





最后，来看一个多台ESXi所连接的分布式交换机的拓扑图吧。

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/39867dfe28a5c1f5410ca5adb6389560/4cc9c0ce047e4a7f0297631efeda56a4.png)

**左侧为端口组，我把vCenter（vcsa）自己单独放了一个端口组，把VMkernel（esxi）放在一个端口组，剩余VM（虚拟机）放在一个端口组。因为没有设置VLAN，实际上这几个端口组是可以互通的。**







# ref

https://blog.51cto.com/wangchunhai/2506718

[某系列](https://www.jianshu.com/u/1a53fa3b0b2f)