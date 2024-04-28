---
title: 关于R6300与小米AX3600刷openwrt教程
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- openwrt
categories:
- 综合
---
# 关于R6300与小米AX3600刷openwrt教程
## R6300教程
**需要用到的资源如下[百度云](https://pan.baidu.com/s/1pmyT5WHlxAezD48TDZvtPw) 提取码：s87z**

![image-20220427141644265](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/24569a3e4256b1d33ceeb759b36ba0f6.png)

刷机文件：

- R6300V2_back-to-ofw.trx 由梅林刷到原厂的固件

- factory-to-dd-wrt.chk 原厂刷到dd-wrt的跳板固件

- Openwrt-19.07.2。 需要刷入的openwrt固件

- netgear-r6300v2-webflash.bin dd-wrt 当前最新固件（20210211）



### 刷回原厂固定版本的系统

如果是其他诸如梅林等系统，首先将系统还原为原厂固件系统。

以下是梅林

![1-0bc2d58fee7642019cb30bd7a602e575](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/f4f5211bcaf6c34315d451406f90d153.png)

在梅林**系统管理里面的固件升级**直接使用文件进行刷机：
**使用固件**![2-1a198385c20a4bec9c37017afa96d234](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/4fdeac671c9241c1b8ab52c0593815e9.png)

然后进入升级界面

![image-20220427142108994](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/cbccea0255c45c6774c73682c05618ee.png)

然后有完成的提示

![4-3a4e3346f13b420fa44f3960022623d9](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/4582499bb92c73c4d77bb8854262b3e7.png)



### 原厂刷入dd-wrt

原厂Netgear的默认地址：192.168.1.1 用户名：admin 密码：password

![8-6c0d8a99b5b84078b5aab5dd6e86c2eb](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/a9f2aa61739567771accce7b1c820225.png)



**然后原版刷入dd-wrt跳板固件**

这里选择用dd-wrt作为跳板固件，选择factory-to-dd-wrt.chk 刷机成后可以选择继续刷到最新版的dd-wrt或者openwrt。

需要注意的是，如果是**美版6300v2需要选择dd-wrt.K3_R6300V2CH.chk**，美版特殊！文件包内有文件。

![9-24c5e4f975524dd4a3a8dde2289c3001](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/552f6d3eb325cd5ea6d5f82a06a28ab8.png)

在上传文件升级会有版本提示，否则就需要从新确认固件是否有问题。

![10-06403273426f4554bc3971db95745025](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/6d954d25910431c68fe1b71ba24551a7.png)



刷机成功后，就能进入dd-wrt系统了。ip没变，还是192.168.1.1。登陆进去后，选择刷入openwrt系统

![13-262c666e5c7b49ac8698c936f08e6161](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/b3da2f825192f07072af67836257edf9.png)



选择刷入固件：

我们这里选择刷入openwrt系统

![image-20220427142620127](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/6d30b47c71fd3d2386aac88c5daebaae.png)

![14-c936b7bf28ab4ccc89a700b20aec4d23](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/be4484cf66c54a31b42b5ee6722c74ff.png)

### 启动openwrt

这里有点小bug。**在dd-wrt刷入openwrt后，要重启路由器**。否则虽然有网关出现，但是管理界面会链接不上。







## AX3600刷入openwrt

整体上来说，和6300类似。

用到的文件[网盘](https://www.geet.cc/?dir=d/%E5%B0%8F%E7%B1%B3AX3600)

![image-20220427144226797](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/7cd010f397df07dba4905afa4f9423dd.png)

### 先刷入特定版本的老原厂固件

![image-20220427143040471](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/6a702bd406ef2136d24fcff73808714e.png)

**这个版本有漏洞可以破解，可以刷入ssh**

![image-20220427143128048](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/2e2b25cda337252e6084d7a7c784dc67.png)

### 然后进入ssh

先拿到token，stok后面这串就是我们的token。

![image-20220427143245513](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/c73ff25a47329f133382dad213340e85.png)

#### 获取 SSH：

```
http://192.168.31.1/cgi-bin/luci/;stok=（将token放入这里）/api/misystem/set_config_iotdev?bssid=Xiaomi&user_id=longdike&ssid=-h%3B%20nvram%20set%20ssh_en%3D1%3B%20nvram%20commit%3B%20sed%20-i%20's%2Fchannel%3D.*%2Fchannel%3D%5C%22debug%5C%22%2Fg'%20%2Fetc%2Finit.d%2Fdropbear%3B%20%2Fetc%2Finit.d%2Fdropbear%20start%3B
```

*补全**stok=**后面的数据，*

![image-20220427143427007](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/d5cca4e584580e525d73e00d68be7195.png)

*然后复制到浏览器打开*，显示`{"code":0}`就说明成功了。

![image-20220427143453925](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/4c3fa205e576a9a45fd7a365fc42fa08.png)

#### 修改默认 SSH 密码为 admin

具体办法同上，也是选择拿到token复制到如下链接并访问。

```
http://192.168.31.1/cgi-bin/luci/;stok=/api/misystem/set_config_iotdev?bssid=Xiaomi&user_id=longdike&ssid=-h%3B%20echo%20-e%20'admin%5Cnadmin'%20%7C%20passwd%20root%3B
```

*补全**stok=**后面的数据，然后复制到浏览器打开*,显示`{"code":0}`就说明成功了。

#### 进入ssh
这里用putty连上路由器

![image-20220427143659857](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/e5f8106ddc96f245be7846b0f6932191.png)

**密码是admin。**



然后将如下升级固件用scp传入路由器的/tmp目录下

![image-20220427143830787](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/61f32af36ec2532fe1aceb99afdc7c0f.png)



#### ssh执行以下命令

```
nvram set flag_last_success=0
nvram set flag_boot_rootfs=0
nvram set flag_boot_success=1
nvram set flag_try_sys1_failed=0
nvram set flag_try_sys2_failed=0
nvram set boot_wait=on
nvram set uart_en=1
nvram set telnet_en=1
nvram set ssh_en=1
nvram commit
```

然后逐一执行以下命令(注意替换包的名字)

```
ubiformat /dev/mtd12 -y -f /tmp/请替换固件包名.ubi
nvram set flag_last_success=0
nvram set flag_boot_rootfs=0
nvram commit
reboot
```





重启后进入openwrt

**openwrt默认用户名和密码为（root，password）**

![image-20220427144053505](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/eac86cb5b405690647db62f9da52eb90/7d7fc358a09b31772378f791e3aeff66.png)







## 参考

- [1] [Netgear R6300v2 刷机dd-wrt openwrt
](https://www.zabbx.cn/archives/netgearr6300v2%E5%88%B7%E6%9C%BAdd-wrtopenwrt)
- [2] [R6300 V2 路由器刷 OpenWrt 翻车记
](https://zhuanlan.zhihu.com/p/93230822)

- [3] [小米AX3600不扩容刷机OpenWrt教程](www.ceer.cc/122)










