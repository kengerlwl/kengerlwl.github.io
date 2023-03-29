---
title: esxi使用istore作为旁路由
top: false
cover: false
toc: true
mathjax: true
date: 2023-03-21 15:27:31
password:
summary:
tags:
- istore
- 代理
- 旁路由
categories:
- 代理
---

# 为什么istore

- 因为istore提供直接的iso镜像文件，方便esxi直接安装。

- 并且也是基于openwrt该的，大部分的使用习惯是一致的



# how

## 首先esxi直接安装ISO

- cpu，内存都不需要很高
- cpu：2
- 内存：2g
- 存储：8g
- 网卡：建议直通





## 坑1-------记得将镜像写入存储

由于我这里**选择得我是ISO文件启动，所以只是相当于U盘启动了**，拔掉U盘就啥也没有了，想要实现正常效果，就需要写入。







### 1.先上传img镜像

可以直接将img文件通过Web界面上传到系统中

也可以通过scp的方式来上传



### 2.写入目标镜像

举例：

```

dd if=/dev/zero of=/dev/sda     #格式化磁盘

dd if=/cdrom/op.img of=/dev/sda   #将img文件写入到硬盘中

/cdrom/op.img是镜像的位置（如果你将镜像上传在了/opt/openwrt.img这里就改为/opt/openwrt.img）

```

确定完成以后，重启系统将U盘拔出即可



### 3.然后esxi控制拔出u盘

启动





## 更改路由器ip





### 更改旁路由lan为主路由的同一网段

`vi /etc/config/network`

[![最强软路由系统iStoreOS_X86安装体验，极简化设置、一键旁路由、小白强烈推荐](https://qnam.smzdm.com/202205/07/62761ff381ca43592.png_e1080.jpg)](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/5983908472625ebc769d6753cd4062a4/4e4db73fbc922244899f840ce1fcc74b.png)

更改ip和mask到主路由同一网段，方便在主路由网段进行访问。



### 配置istore

然后就可以根据更改后的旁路由ip进行访问了。

也可以安装一下其他的插件

1、不同于其他openwrt的复杂配置。 iStoreOS进行了深度定制，在某些基础功能上都有对小白极其友好的向导设置，点击网络向导。

[![最强软路由系统iStoreOS_X86安装体验，极简化设置、一键旁路由、小白强烈推荐](https://qnam.smzdm.com/202205/07/62761ff410d712913.png_e1080.jpg)](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/5983908472625ebc769d6753cd4062a4/cedc20c4e21949b386304e70c4ad0ec9.png)

2、根据自身需求选择配置，我这里选择配置为旁路由。

[![最强软路由系统iStoreOS_X86安装体验，极简化设置、一键旁路由、小白强烈推荐](https://qnam.smzdm.com/202205/07/62761ff4341e22968.png_e1080.jpg)](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/5983908472625ebc769d6753cd4062a4/bd50cb647804ee660a3e10a69502b3ba.png)

3、进入旁路由配置选项，只需要修改两个选项，将ip地址修改为旁路由登录ip，网管地址修改为主路由ip，根据自身需要选择是否关闭旁路由dhcp功能，我这里选择关闭，点击保存配置。

[![最强软路由系统iStoreOS_X86安装体验，极简化设置、一键旁路由、小白强烈推荐](https://qnam.smzdm.com/202205/07/62761ff431d787474.png_e1080.jpg)](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/5983908472625ebc769d6753cd4062a4/e09ffad009cb129455cfc0b25597495b.png)







# 坑2

istore暂停挂起后，好像会失效，建议重启解决。





# 坑3------DNS配置要注意

对于旁路由，如果不正确配置其DNS，可能会导致旁路由下的设备会使用不了不分域名解析。

**正确的思路：**

我的主路由ip：`10.10.10.10`

我的旁路由ip：`10.10.100.1`

配置文件为：**/etc/resolv.conf** 

```
search lan
nameserver 10.10.10.10
nameserver 8.8.8.8
```

解释：

```bash
cat /etc/resolv.conf
domain  51osos.com
search  www.51osos.com  51osos.com
nameserver 202.102.192.68
nameserver 202.102.192.69
```

1）nameserver：表示域名解析时，使用该地址指定的主机为域名服务器，其中域名服务器是按照文件中出现的顺序来查询的，且**只有当第一个nameserver没有反应时才查询下面的nameserver**。
2）domain：声明主机的域名，很多程序会用到，如邮件系统。当为没有域名的主机进行DNS查询时，也要用到。如果没有域名，主机名将被使用，删除所有在第一个点(.)前面的内容。
3）search：它的多个参数指明域名查询顺序，当要查询没有域名的主机，主机将在由search声明的域中分别查找。
**注意：search和domain不能共存，如果同时存在，后面出现的将会被使用。**



总之一句话，istore，做旁路由有较大风险干扰主路由，建议试试用openwrt



# ref

https://post.smzdm.com/p/a0qrvdgw/

