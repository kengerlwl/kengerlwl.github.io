---
title: java-IO
top: false
cover: false
toc: true
mathjax: true
draft: true
date: 2024-04-10 15:27:31
password:
summary:
tags:
- java
- IO
categories:
- find JOB
---



# 计算机IO结构

运算器、控制器、存储器、输入设备、输出设备。

![冯诺依曼体系结构](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/dc65631729c1fc11888079d4e0f4c5a7/102cfebfc7a79a3d4a45d44f29af6581.png)冯诺依曼体系结构

**输入设备（比如键盘）和输出设备（比如显示器）**都属于外部设备。网卡、硬盘这种既可以属于输入设备，也可以属于输出设备。



操作系统：一个进程的地址空间划分为 **用户空间（User space）** 和 **内核空间（Kernel space ）** 。内核空间用来进行一些更加高危，更加关键的操作。比如：文件管理、进程通信、内存管理等等



所以，想要IO，需要通过 **系统调用** 来间接访问内核空间

当应用程序发起 I/O 调用后，会经历两个步骤：

1. **内核等待 I/O 设备准备好数据**
2. **内核将数据从内核空间拷贝到用户空间。**





# 常见IO模型

### [BIO (Blocking I/O)](https://javaguide.cn/java/io/io-model.html#bio-blocking-i-o)

**BIO 属于同步阻塞 IO 模型** 。

同步阻塞 IO 模型中，应用程序发起 read 调用后，**会一直阻塞，直到内核把数据拷贝到用户空间。**

但是，当面对十万甚至百万级连接的时候，传统的 BIO 模型是无能为力的。因此，我们需要一种更高效的 I/O 处理模型来应对更高的并发量。

![图源：《深入拆解Tomcat & Jetty》](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/dc65631729c1fc11888079d4e0f4c5a7/04fb15e7c9736207b513137d6c45b084.png)



### [NIO (Non-blocking/New I/O)](#nio-non-blocking-new-i-o)

Java 中的 NIO 于 Java 1.4 中引入，对应 `java.nio` 包，提供了 `Channel` , `Selector`，`Buffer` 等抽象。NIO 中的 N 可以理解为 Non-blocking，不单纯是 New。**它是支持面向缓冲的，基于通道的 I/O 操作方法。 对于高负载、高并发的（网络）应用，应使用 NIO 。**

**相当于这个线程一直搁这疯狂的问IO数据好了吗？它并不阻塞在某一个IO上，它可以是一个线程不阻塞的，疯狂的询问多个IO好了吗。不想BIO，一个IO需要一个线程！！！！！！**

**可以使用少量的线程来处理多个连接，大大提高了 I/O 效率和并发。**

所以单独的线程可以管理多个输入和输出通道。因此NIO可以让服务器端使用一个或有限几个线程来同时处理连接到服务器端的所有客户端。

Java 中的 NIO 可以看作是 **I/O 多路复用模型**。也有很多人认为，Java 中的 NIO 属于同步非阻塞 IO 模型。

跟着我的思路往下看看，相信你会得到答案！

我们先来看看 **同步非阻塞 IO 模型**。

![图源：《深入拆解Tomcat & Jetty》](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/dc65631729c1fc11888079d4e0f4c5a7/4719c0e343b9b0a5b97fadd95e298908.png)图源：《深入拆解Tomcat & Jetty》

同步非阻塞 IO 模型中，应用程序会一直发起 read 调用，等待数据从内核空间拷贝到用户空间的这段时间里，线程依然是阻塞的，直到在内核把数据拷贝到用户空间。

**应用程序不断进行 I/O 系统调用轮询数据是否已经准备好的过程是十分消耗 CPU 资源的。**



### IO多路复用（多了个select过程）

IO 多路复用模型中，**线程首先发起 select 调用，询问内核数据是否准备就绪，等内核把数据准备好了，用户线程再发起 read 调用。read 调用的过程（数据从内核空间 -> 用户空间）还是阻塞的**。

**IO 多路复用模型，通过减少无效的系统调用，减少了对 CPU 资源的消耗。**



![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/dc65631729c1fc11888079d4e0f4c5a7/b7c5aa1b3d6f937b8daf2e184c728226.png)

目前支持 IO 多路复用的系统调用，有 select，epoll 等等。select 系统调用，目前几乎在所有的操作系统上都有支持。

- **select 调用**：内核提供的系统调用，它支持一次查询多个系统调用的可用状态。几乎所有的操作系统都支持。
- **epoll 调用**：linux 2.6 内核，属于 select 调用的增强版本，优化了 IO 的执行效率



### [AIO (Asynchronous I/O)](https://javaguide.cn/java/io/io-model.html#aio-asynchronous-i-o)

AIO 也就是 NIO 2。Java 7 中引入了 NIO 的改进版 NIO 2,它是异步 IO 模型。

优点，不用一直阻塞。

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/dc65631729c1fc11888079d4e0f4c5a7/ed560a676ca2432f45e79a0d2c5f43e1.png)
