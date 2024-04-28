---
title: VMWare ESXi 如何备份迁移系统
top: false
cover: false
toc: true
mathjax: true
date: 2023-03-23 15:27:31
password:
summary:
tags:
- 虚拟机
- linux
- esxi迁移
categories:
- 实验室

---



# 1. 找到目标vdmk文件夹

这是我需要备份的系统的文件夹

![image-20230324173509106](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/f71dd29847394edbcef934a3ed7bb42e/cc4b2ce0d51e2d30051e1a73e771b9c1.png)







# 2.拷贝到另一个目录下

我拷贝到了该目录下面

![image-20230324173614713](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/f71dd29847394edbcef934a3ed7bb42e/ed48bcdeff94784c429e6a4e308e9ef4.png)





# 3.新建虚拟机

选择添加现有硬盘

![image-20230324173657020](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/f71dd29847394edbcef934a3ed7bb42e/f4d1b197762a0e792f7ca4c0e03254d3.png)

找到目标所在地

![image-20230324173723578](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/f71dd29847394edbcef934a3ed7bb42e/887b889731d194f85afff4b4ca43851e.png)





完成



# 注意：

要关机或者挂起后才能拷贝







# ref

