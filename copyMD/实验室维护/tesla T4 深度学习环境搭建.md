---
title: tesla T4 深度学习环境搭建
top: false
cover: false
toc: true
mathjax: true
date: 2023-03-06 15:27:31
password:
summary:
tags:
- 实验室
- cuda
categories:
- dl
---



# Tesla T4安装





### NVIDIA的驱动

```
 wget https://cn.download.nvidia.com/tesla/460.106.00/NVIDIA-Linux-x86_64-460.106.00.run
```

下载deb文件后，先别着急安装，需先禁用nuoveau

```text
sudo vi /etc/modprobe.d/blacklist.conf 
```

下面两行加到末尾

```text
blacklist nouveau
options nouveau modeset=0
```

更新initramfs，需要稍微等一会

```text
sudo update-initramfs -u
```

重启系统。

验证屏蔽是否成功，执行下面语句，结果为空，即为成功。

```text
lsmod | grep nouveau
```

执行安装

先安装依赖软件，gcc make。若已安装则建立cc make软链接

```text
sudo apt install gcc
```

gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)

```text
sudo apt install make
```

GNU Make 4.2.1

```text
chmod +x NVIDIA-Linux-x86_64-460.106.00.run 
sudo bash ./NVIDIA-Linux-x86_64-460.106.00.run
```

安装过程中，

Install 32 bit compatibility libraries ？ 选择No

安装完毕后，输入

```text
nvidia-smi
```

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/fd10750a9216e7e8481fa986baad00c8/e5eef861ebafd1e5104dac0a107afa79.png)

### 安装CUDA和cuDNN

下载run文件

```text
wget https://developer.download.nvidia.com/compute/cuda/11.1.0/local_installers/cuda_11.1.0_455.23.05_linux.run
sudo sh cuda_11.1.0_455.23.05_linux.run
```

accept 同意 取消Driver，因为我们前面已经安装过显示驱动了，不能重复安装，否则会报错。

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/fd10750a9216e7e8481fa986baad00c8/80e31a36d5f762ad8c5c23c146db4f38.png)

等待执行完毕

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/fd10750a9216e7e8481fa986baad00c8/1aa9c7f087059a817bb0debaffa0acfa.png)

添加环境变量

```text
sudo vi ~/.bashrc
```

最后增加如下：(这里的路径根据上面的输出自动修改)

```text
export  PATH=/usr/local/cuda-11.1/bin:$PATH
export  LD_LIBRARY_PATH=/usr/local/cuda-11.1/lib64:$LD_LIBRARY_PATH
```

使生效。

```text
source ~/.bashrc 
或者使用 /etc/profile 全局生效，方便实验室用
```



测试查看cuda版本

```
labot@gui-gpu:~$ nvcc -V
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2020 NVIDIA Corporation
Built on Tue_Sep_15_19:10:02_PDT_2020
Cuda compilation tools, release 11.1, V11.1.74
Build cuda_11.1.TC455_06.29069683_0
```





**然后是cuDNN**



```
wget https://developer.nvidia.com/downloads/c118-cudnn-linux-8664-880121cuda11-archivetarz
```



安装cuDNN v8.2.1(请根据自己的需要进行下载。)**这个要翻到下面以前发行的就会有这种cudnn的库文件下载。**

[https://developer.nvidia.com/rdp/cudnn-archivedeveloper.nvidia.com/rdp/cudnn-archive](https://link.zhihu.com/?target=https%3A//developer.nvidia.com/rdp/cudnn-archive)

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/fd10750a9216e7e8481fa986baad00c8/bdf466115f08a53ab2b6a05ebafb9a36.png)

解压。

```text
tar zxvf cudnn-11.3-linux-x64-v8.2.1.32.tgz
```

本目录会多出一个cuda目录，将cudnn.h复制到cuda安装目录下的include下。

```text
sudo cp cuda/include/cudnn.h /usr/local/cuda-11.1/include/
```

再将lib64下所有的so文件，复制到lib64下。

```text
sudo cp cuda/lib64/lib* /usr/local/cuda-11.1/lib64/
```

将/usr/local/cuda-11.1/lib64下的所有so文件，复制到/usr/lib下，防止调用时找不到(非必要)

```text
sudo cp /usr/local/cuda-11.1/lib64/* /usr/lib/
```

添加可执行权限

```
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
```

