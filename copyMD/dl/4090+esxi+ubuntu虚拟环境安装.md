---
title: 4090+esxi+ubuntu虚拟环境安装
top: false
cover: false
toc: true
mathjax: true
date: 2023-05-29 15:27:31
password:
summary:
tags:
- pytorch
categories:
- 学术
---


# 添加PCIE设备

直接all in

![image-20230529224127732](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/469505aeb3a2f52330266433c225d6f2/5fb3a451989202d0dddb2d877933e9a6.png)



# NVIDIA驱动

参考相关博客，要注意一些虚拟机的参数添加问题。



[官网链接](https://www.nvidia.cn/Download/index.aspx?lang=cn)

去官网下载驱动

![image-20230601000105656](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/469505aeb3a2f52330266433c225d6f2/e525db42ac109a6dffaaf2658360ffaf.png)



`wget https://us.download.nvidia.com/XFree86/Linux-x86_64/525.116.04/NVIDIA-Linux-x86_64-525.116.04.run`

下载run文件后，先别着急安装，需先禁用nuoveau



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

### 问题1

在完成上述步骤后，可能仍然不work。

这时候，可以尝试去esxi里面，把pcie设备删除，然后再在虚拟机添加回来，重启。就ok了。



# Cuda环境

直接取官网，根据特定版本，选择runfile脚本文件安装。

## 2.2 进入CUDA官网

CUDA官网:https://developer.nvidia.com/cuda-toolkit-archive

选择相应版本型号



![image-20230601002603316](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/469505aeb3a2f52330266433c225d6f2/e4fb240f5670dd45caceaac8db614d5f.png)





下载run文件



```text
wget https://developer.download.nvidia.com/compute/cuda/12.0.1/local_installers/cuda_12.0.1_525.85.12_linux.run
sudo sh cuda_12.0.1_525.85.12_linux.run

```

accept 同意 取消Driver，因为我们前面已经安装过显示驱动了，不能重复安装，否则会报错。



![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/fd10750a9216e7e8481fa986baad00c8/80e31a36d5f762ad8c5c23c146db4f38.png)





等待执行完毕



![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/fd10750a9216e7e8481fa986baad00c8/1aa9c7f087059a817bb0debaffa0acfa.png)

****



添加环境变量



```text
sudo vi ~/.bashrc
```

如果要使所有用户生效，编辑`/etc/profile`



最后增加如下：这里的路径根据上面的输出自动修改这里的路径根据上面的输出自动修改

cuda版本可能有变，看你自己的配置

```text
export  PATH=/usr/local/cuda/bin:$PATH
export  LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```



使生效。



```text
source ~/.bashrc 
或者使用 /etc/profile 全局生效，方便实验室用
```







# cudnn环境

## 方法一

官方的tar解压

```
cudnn-linux-x86_64-8.8.1.3_cuda12-archive.tar.xz
sudo cp ./include/* /usr/local/cuda-12.1/include
sudo cp ./lib/libcudnn* /usr/local/cuda-12.1/lib64
 
sudo chmod a+r /usr/local/cuda-12.1/include/cudnn* 
sudo chmod a+r /usr/local/cuda-12.1/lib64/libcudnn*
```



## 方法二-ubuntu

官网：https://developer.nvidia.com/rdp/cudnn-archive

```
labot@gpu6-labot:~$ sudo dpkg -i cudnn-local-repo-ubuntu2204-8.9.4.25_1.0-1_amd64.deb   # 从官网下载
[sudo] password for labot: 
Selecting previously unselected package cudnn-local-repo-ubuntu2204-8.9.4.25.
(Reading database ... 165519 files and directories currently installed.)
Preparing to unpack cudnn-local-repo-ubuntu2204-8.9.4.25_1.0-1_amd64.deb ...
Unpacking cudnn-local-repo-ubuntu2204-8.9.4.25 (1.0-1) ...
Setting up cudnn-local-repo-ubuntu2204-8.9.4.25 (1.0-1) ...

The public cudnn-local-repo-ubuntu2204-8.9.4.25 GPG key does not appear to be installed.
To install the key, run this command:
sudo cp /var/cudnn-local-repo-ubuntu2204-8.9.4.25/cudnn-local-3C3A81D3-keyring.gpg /usr/share/keyrings/ # 运行这行输出的命令

labot@gpu6-labot:~$ sudo cp /var/cudnn-local-repo-ubuntu2204-8.9.4.25/cudnn-local-3C3A81D3-keyring.gpg /usr/share/keyrings/
labot@gpu6-labot:~$ sudo apt-get update 
labot@gpu6-labot:~$ sudo apt-get install libcudnn8

```





# anaconda

```
 wget https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
 bash Axxxxxx
```





# 坑1 已启用 / 需要重新引导 4090 问题

https://www.ypojie.com/11956.html







# 坑2 系统KCS无故重启问题

[KCS说明](https://www.cnblogs.com/wudibuzaijia/p/8526848.html)

思路：

1. 固态掉盘的问题：换个固态试试
2. 系统软件硬件不适配问题，直接物理机安装ubuntu。再做进一步测试。



# esxi手动缩小linux的存储

这个需要主机还有一个原存储大小的空间

https://www.imwxz.com/posts/ce878cfd.html



# 双烤

双烤意思是CPU+GPU一起



GPU：gpu-burn

```
git clone https://github.com/wilicc/gpu-burn
cd gpu-burn
docker build -t gpu_burn .
docker run --rm --gpus all gpu_burn
```



CPU：https://superpi.ilbello.com/

或者CPU：

```
sudo apt-get install stress
stress -c 2 -t 1800
-c是cpu线程数量
-t是时间
```





# GPU持久状态开启

厂商建议开启[GPU](https://so.csdn.net/so/search?q=GPU&spm=1001.2101.3001.7020)的持久模式。gpu默认持久模式关闭的时候，GPU如果负载低，会休眠。之后唤起的时候，有一定几率失败，nvidia-smi -pm 1 这个命令可以使GPU一直保持准备工作的状态

```
sudo nvidia-smi -pm 1
```



# ref

[虚拟机参数添加](http://php.js.cn/index.php)

[gpu持久状态开启](https://blog.csdn.net/owlcity123/article/details/108338293)

