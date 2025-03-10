---
title: java-JVM学习
top: false
cover: false
toc: true
mathjax: true
draft: false
date: 2024-03-25 15:27:31
password:
summary:
tags:
- java
categories:
- find JOB

---

## 什么是JVM？

> JVM（Java Virtual Machine）是用于运行Java字节码的虚拟机，**包括一套字节码指令集、一组程序寄存器、一个虚拟机栈、一个虚拟机堆、一个方法区和一个垃圾回收器**。JVM运行在操作系统之上，不与硬件设备直接交互。
>
> **java是一个解释型语言！！！**
>
> **Java源文件在通过编译器之后被编译成相应的.Class文件**（字节码文件），**.Class文件又被JVM中的解释器编译成机器码在不同的操作系统（Windows、Linux、Mac）上运行**。每种操作系统的解释器都是不同的，但基于解释器实现的虚拟机是相同的，这也是Java能够跨平台的原因。在一个Java进程开始运行后，虚拟机就开始实例化了，有多个进程启动就会实例化多个虚拟机实例。进程退出或者关闭，则虚拟机实例消亡，在多个虚拟机实例之间不能共享数据

## JVM虚拟机包含了哪些区域？



**一个更加清晰的结构图**

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/8c884d8796e5beac7799576e7fbbb968.png)





**java运行时数据区结构图**



![Java 运行时数据区域（JDK1.8 ）](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/ab3aa96730a25c95c8e9a6b6c184d643.png)

**线程私有的：**

- **程序计数器**：相当于判断当前线程执行到哪一行

- **虚拟机栈**：**拟机栈为虚拟机执行 Java 方法 （也就是字节码）服务，还有方法调用的各种（变量，操作数，方法返回地址）存储要要入栈帧。**

  ![三分恶面渣逆袭：Java虚拟机栈](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/2cf6bde8c17b55608dcb130c6688f912.png)

- **本地方法栈**：**为虚拟机使用到的 Native 方法服务**，与虚拟机栈不同：Navtive方法是Java通过JNI直接调用本地C/C++库，可以认为是Native方法相当于C/C++暴露给Java的一个接口，**Java通过调用这个接口从而调用到C/C++方法**。

**线程共享的：**

- **堆**： **几乎所有的对象实例以及数组都在这里分配内存。**
  - Java 堆是**垃圾收集器管理的主要区域（GC）**
  - 栈的话一般操作系统有指令可以自己做好回收
  - ![二哥的 Java 进阶之路：堆](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/f7a24aef5da03e76e6d8743c1c0bfbe1.png)
- **方法区：（实际上是一些字符串常量池，方法，类信息）**
- 直接内存 (非运行时数据区的一部分)

**常量池有**

- 运行时常量池
- 字符串常量池



### java内存分区

![refs/heads/master/image-20221026100332889](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/8d49402e9a8099495c09a33c227b839e.png)

### java堆

**Java堆(Java Heap)是线程共享的**，一般来说也是JVM管理最大的一块内存区域，**同时也是垃圾收集器GC的主要管理区域。**

Java堆在JVM启动时创建，作用是：**存放对象实例**

### 对象逃逸：并不是所有的java对象都放在堆！！！

**“逃逸分析” 的本质：**

**主要就是分析对象的动态作用域，分析一个对象的动态作用域是否会逃逸出方法范围、或者线程范围。**

**简单的说：**

如果一个对象在一个方法内定义，如果被方法外部的引用所指向，那认为它逃逸了。

否者，这个对象，没有发生逃逸。

**逃逸分析的类型有两种：**

- 方法逃逸
- 线程逃逸

什么是：方法逃逸(对象逃出当前方法)：

当一个对象在方法里面被定义后，它可能被外部方法所引用，例如作为调用参数传递到其它方法中。

什么是：线程逃逸((对象逃出当前线程)：

这个对象甚至可能被其它线程访问到，例如赋值给类变量或可以在其它线程中访问的实例变量



通过逃逸分析，编译器会对代码进行优化。

**如果能够证明一个对象不会逃逸到方法外或者线程外，或者说逃逸程度比较低，则可以对这个对象采用不同程度的优化：**

- **栈上分配（就不分配到堆了）**
- **标量替换**
- **消除同步锁**



###  java本地方法栈

本地方法栈(Native Method Stack)也是线程私有的，与虚拟机栈的作用非常类似。 区别是虚拟机栈是为执行Java方法服务的，而本地方法栈是为执行Native方法服务的。







## 在JVM后台运行的线程有哪些？

> - 虚拟机线程（JVMThread）：虚拟机线程在JVM到达安全点（SafePoint）时出现。
> - 周期性任务线程：通过定时器调度线程来实现周期性操作的执行。
> - **GC（Garbage Collection）线程**：GC线程支持JVM中不同的垃圾回收活动。
> - 编译器线程：编译器线程在运行时将字节码动态编译成本地平台机器码，是JVM跨平台的具体实现。
> - 信号分发线程：接收发送到JVM的信号并调用JVM方法





## 关于垃圾回收全流程

1. **先判断什么是垃圾**，并标记，JVM一般用**可达性分析**算法
2. 交个垃圾收集器进行垃圾回收，（回收算法：四种）
   1. JVM 提供了多种垃圾回收器，包括 CMS GC、G1 GC、ZGC 等





## 如何确定垃圾可以回收？

> 方法：引用计数器和可达性分析
>
> **引用计数器**：在Java 中如果要操作对象，就必须先获取该对象的引用，因此可以通过引用计数法来判断一个对象是否可以被回收。在为对象添加一个引用时，引用计数加l ；在为对象删除一个引用时， 引进计数减l ；如果一个对象的引用计数为0 ，则表示此刻该对象没有被引用，可以被回收。
>
> **存在的问题：如果两个互相引用，则不会回收**![对象之间循环引用](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/33861af6e976624ec2f601443ee6fc7c.png)
>
> **可达性分析**：为了解决引用计数器方法的循环引用问题，首先定义一些GC Root s 对象，然后**以这些GC Roots 对象作为起点向下搜索，如果在GC roots 和一个对象之间没有可达路径， 则称该对象是不可达的**。不可达对象要经过至少两次标记才能判定其是否可以被回收，如果在两次标记后该对象仍然是不可达的，则将被垃圾收集器回收。
>
> ​	**哪些对象可以作为 GC Roots 呢？**
>
> - **虚拟机栈中的引用**（方法的参数、局部变量等）
> - **本地方法栈中 JNI 的引用**
> - **类静态变量**
> - 运行时常量池中的常量（String 或 Class 类型）





### java引用类型总结

![Java 引用类型总结](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/5cd2eb63ab7866a1bedaa5f6f31a4656.png)

1. **强引用（StrongReference）**

以前我们使用的大部分引用实际上都是强引用，这是使用最普遍的引用。**如果一个对象具有强引用，那就类似于必不可少的生活用品，垃圾回收器绝不会回收它**。当内存空间不足，Java 虚拟机宁愿抛出 OutOfMemoryError 错误，使程序异常终止，也不会靠随意回收具有强引用的对象来解决内存不足问题。

**2．软引用（SoftReference）**

如果一个对象只具有软引用，那就类似于可有可无的生活用品。**如果内存空间足够，垃圾回收器就不会回收它**，如果内存空间不足了，就会回收这些对象的内存。只要垃圾回收器没有回收它，该对象就可以被程序使用。软引用可用来实现内存敏感的高速缓存。

软引用可以和一个引用队列（ReferenceQueue）联合使用，如果软引用所引用的对象被垃圾回收，JAVA 虚拟机就会把这个软引用加入到与之关联的引用队列中。

**3．弱引用（WeakReference）**

如果一个对象只具有弱引用，那就类似于可有可无的生活用品。弱引用与软引用的区别在于：只具有弱引用的对象拥有更短暂的生命周期。在垃圾回收器线程扫描它所管辖的内存区域的过程中，**一旦发现了只具有弱引用的对象，不管当前内存空间足够与否，都会回收它的内存**。不过，由于垃圾回收器是一个优先级很低的线程， 因此不一定会很快发现那些只具有弱引用的对象。

弱引用可以和一个引用队列（ReferenceQueue）联合使用，如果弱引用所引用的对象被垃圾回收，Java 虚拟机就会把这个弱引用加入到与之关联的引用队列中。

**4．虚引用（PhantomReference）**

"虚引用"顾名思义，就是形同虚设，与其他几种引用都不同，**虚引用并不会决定对象的生命周期。如果一个对象仅持有虚引用，那么它就和没有任何引用一样，在任何时候都可能被垃圾回收。**





## 垃圾回收算法（主要针对堆的内存做回收）

标记清除（ Mark-Sweep ）

标记复制（ Copying ）

标记整理( Mark-Compact ）

分代收集（ Generational Collecting ）





### 一些常见的原则（分代不同区域用什么回收算法）

> 分代收集算法根据对象的不同类型将内存划分为不同的区域， JVM 将堆划分为新生代和老年代。
>
> **新生代主要存放新生成的对象，其特点是对象数量多但是生命周期短，在每次进行垃圾回收时都有大量的对象被回收；**
>
> **老年代主要存放大对象和生命周期长（相当于会晋升到老年代中）的对象，因此可回收的对象相对较少**。
>
> 因此， JVM 根据不同的区域对象的特点选择了不同的算法。**老年代的垃圾回收算法根据老年代的特性有两类，标记清除和标记整理。**
>
> **空间分配担保**
>
> 空间分配担保是为了**确保在 Minor GC 之前老年代本身还有容纳新生代所有对象的剩余空间。**

**新生代采用标记-复制算法，老年代采用标记-整理算法。**







### 标记清除算法？

> 标记清除，顾名思义，就是把标记的清除掉，分两个阶段，第一阶段，标记，第二阶段，清除；
>
> **首先标记出所有需要回收的对象，在标记完成后，统一回收掉所有被标记的对象，**也可以反过来，标记存活的对象，统一回收所有未被标记的对象。标记过程就是对象是否属于垃圾的判定过程，它是最早出现也是最基础的算法

**效率低下，内存碎片化**

### 标记复制（适用于存活率低）(AB分区，直接分区移动存活的)

为了解决碎片空间的问题，出现了“复制算法”。复制算法的原理是，**将内存分成两块，每次申请内存时都使用其中的一块，当内存不够时**，将**这一块内存中所有存活的复制到另一块上。然后将然后再把已使用的内存整个清理掉。**

**导致内存利用率不足**

### 标记-整理算法（适用于存活率高）（双端移动，也是移动存活的对象）

复制算法在 GC 之后存活对象较少的情况下效率比较高，但如果存活对象比较多时，会执行较多的复制操作，效率就会下降。而老年代的对象在 GC 之后的存活率就比较高，所以就有人提出了“标记-整理算法”。

**标记-整理算法的“标记”过程与“标记-清除算法”的标记过程一致，但标记之后不会直接清理。而是将所有存活对象都移动到内存的一端。移动结束后直接清理掉剩余部分。**

![标记-整理算法](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/9f54c5467aad11f9dd339ba0f2e05b8e.png)



### 不同算法对比

![refs/heads/master/image-20240915180830891](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/295e38a1d1b4fa2c58f238c3c8d4b707.png)





三个算法效率对比



### 重点：分代清除法



![三分恶面渣逆袭：Java堆内存划分](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/bae8c5a1cbef1379722b3989a11acc1c.png)

三分恶面渣逆袭：Java堆内存划分

新生代又被划分为 Eden 空间和两个 Survivor 空间（From 和 To）。

- **Eden 空间**：大多数新创建的对象会被分配到 Eden 空间中。当 Eden 区填满时，会触发一次轻量级的垃圾回收（Minor GC），清除不再使用的对象。
- **Survivor 空间**：每次 Minor GC 后，仍然存活的对象会从 Eden 区或 From 区复制到 To 区。From 和 To 区交替使用。

对象在新生代中经历多次 GC 后，如果仍然存活，会被移动到老年代。



### 对象什么时候会进入老年代？

对象通常会先在年轻代中分配，然后随着时间的推移和垃圾收集的处理，某些对象会进入到老年代中。

![二哥的 Java 进阶之路：对象进入老年代](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/7246d9600feb75db7fff0b0958af5722.png)









## 内存分配与回收

### Minor/Young GC 和 Full GC

- **Minor GC：回收新生代**，因为新生代对象存活时间很短，因此 Minor GC 会频繁执行，执行的速度一般也会比较快。
  - **触发条件**：新创建的对象优先在新生代 Eden 区进行分配，如果 Eden 区没有足够的空间时，就会触发 Young GC 来清理新生代。
- **Full GC(all 回收)：回收老年代和新生代**，老年代对象其存活时间长，因此 Full GC 很少执行，执行速度会比 Minor GC 慢很多



### Full GC 的触发条件

![Full GC触发条件](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/75882c327cc0ef4bc483c63c3ee2c6f0.png)



对于 Minor GC，其触发条件非常简单，当 Eden 空间满时，就将触发一次 Minor GC。而 Full GC 则相对复杂，有以下条件：

#### 1. 调用 System.gc()

只是建议虚拟机执行 Full GC，但是虚拟机不一定真正去执行。不建议使用这种方式，而是让虚拟机管理内存。

#### 2. 老年代空间不足

老年代空间不足的常见场景为前文所讲的大对象直接进入老年代、长期存活的对象进入老年代等。

为了避免以上原因引起的 Full GC，应当尽量不要创建过大的对象以及数组。除此之外，可以通过 -Xmn 虚拟机参数调大新生代的大小，让对象尽量在新生代被回收掉，不进入老年代。还可以通过 -XX:MaxTenuringThreshold 调大对象进入老年代的年龄，让对象在新生代多存活一段时间。

#### 3. 空间分配担保失败

使用复制算法的 Minor GC 需要老年代的内存空间作担保，如果担保失败会执行一次 Full GC。



## 垃圾收集器

VM 的垃圾收集器主要分为两大类：分代收集器和分区收集器

- **分代收集器的代表是 CMS**
- **分区收集器的代表是 G1 和 ZGC。**

![三分恶面渣逆袭：HotSpot虚拟机垃圾收集器](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/052c07ed8872fa58b8f28d2af4b9b462.png)



### CMS 收集器（并行标记清除）

（**有待深入理解**）

CMS收集器仅作用于**老年代**的收集，**是基于`标记-清除算法`的**

特点：

- 并发标记
- 并发清除

![小潘：CMS](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/987cac742efed23f002b9aa7469afd20.png)



### G1（Garbage-First Garbage Collector）收集器

**目前是java的默认垃圾收集器**

G1 把 Java 堆划分为多个大小相等的独立区域（Region），每个区域都可以扮演新生代（Eden 和 Survivor）或老年代的角色。

![gc-collector-20231228213824](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/cba989a5f31a0dd0e2dbaad8365c42a3.png)

G1 收集器的运行过程大致可划分为这几个步骤：

①、**并发标记**，G1 通过并发标记的方式找出堆中的垃圾对象。并发标记阶段与应用线程同时执行，不会导致应用线程暂停。

②、**混合收集**，在并发标记完成后，G1 会计算出哪些区域的回收价值最高（也就是包含最多垃圾的区域），然后优先回收这些区域。这种回收方式包括了部分新生代区域和老年代区域。

选择回收成本低而收益高的区域进行回收，可以提高回收效率和减少停顿时间。

③、**可预测的停顿**，G1 在垃圾回收期间仍然需要「Stop the World」。不过，G1 在停顿时间上添加了预测机制，用户可以 JVM 启动时指定期望停顿时间，G1 会尽可能地在这个时间内完成垃圾回收。



### 区别



| 特征         | CMS                          | G1（适用于多CPU，大内存服务器）      |
| ------------ | ---------------------------- | ------------------------------------ |
| 垃圾收集算法 | **标记-清除**                | **分代、复制、标记-清除、标记-整理** |
| 内存分配策略 | 可能产生较多内存碎片         | 尽量避免内存碎片                     |
| 并发性       | 标记和清除阶段并发           | 标记阶段并发，清理阶段暂停应用程序   |
| 回收停顿时间 | 注重减少停顿时间             | 注重整体性能表现                     |
| 适用场景     | **对停顿时间敏感的应用程序** | **大堆内存、高吞吐量的应用程序**     |

我们生产环境中采用了设计比较优秀的 G1 垃圾收集器，因为它不仅能满足低停顿的要求，而且解决了 CMS 的浮动垃圾问题、内存碎片问题。

G1 非常适合大内存、多核处理器的环境。

## JMM主内存和工作内存





![JMM(Java 内存模型)](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/afaf5bed55fe5835ca70005914a9db2c.png)

**什么是主内存？什么是本地内存？**

- **主内存**：**所有线程创建的实例对象都存放在主内存中，不管该实例对象是成员变量，还是局部变量，类信息、常量、静态变量都是放在主内存中**。为了获取更好的运行速度，虚拟机及硬件系统可能会让**工作内存优先存储于寄存器和高速缓存**中。
- **本地内存**：**每个线程都有一个私有的本地内存，本地内存存储了该线程以读 / 写共享变量的副本**。每个线程只能操作自己本地内存中的变量，无法直接访问其他线程的本地内存。**如果线程间需要通信，必须通过主内存来进行。本地内存是 JMM 抽象出来的一个概念，并不真实存在**，它涵盖了缓存、写缓冲区、寄存器以及其他的硬件和编译器优化。

线程 1 与线程 2 之间如果要进行通信的话，必须要经历下面 2 个步骤：

1. 线程 1 把本地内存中修改过的共享变量副本的值同步到主内存中去。
2. 线程 2 到主存中读取对应的共享变量的值。









## HotSpot 虚拟机对象探秘

### 对象的创建（建议背图）

**类加载判断》内存分配》内存初始化为0》对象头设置》init构造方法执行**

![二哥的 Java 进阶之路：对象的创建过程](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/b5b269e78f1e267b2e137ca91f5eeec7.png)



- **类加载检查**

​		虚拟机遇到一条 new 指令时，首**先将去检查这个指令的参数是否能在常量池中定位到这个类的符号引用**，并且检查这个符号引用代表的**类是否已被加载过、解析和初始化过**。**如果没有，那必须先执行相应的类加载过程**。

- **分配内存**

  在**类加载检查**通过后，接下来虚拟机将为新生对象**分配内存**。对象所需的内存大小在类加载完成后便可确定，为对象分配空间的任务等同于把一块确定大小的内存从 Java 堆中划分出来。**分配方式**有 **“指针碰撞”** 和 **“空闲列表”** 两种，**选择哪种分配方式由 Java 堆是否规整决定，而 Java 堆是否规整又由所采用的垃圾收集器是否带有压缩整理功能决定**。

- **初始化零值**

​		内存分配完成后，虚拟机需要将分配到的**内存空间都初始化为零值**（不包括对象头）

- **设置对象头**

  初始化零值完成之后，**虚拟机要对对象进行必要的设置**，例如这个对象是哪个类的实例、如何才能找到类的元数据信息、对象的哈希码、对象的 GC 分代年龄等信息。 **这些信息存放在对象头中。**

- **执行 init 方法**
	
	执行 new 指令之后会接着执行 `<init>` 方法，把对象按照程序员的意愿进行初始化





### 对象的访问定位

Java 程序通过栈上的 reference 数据来操作堆上的具体对象。对象的访问方式由虚拟机实现而定，目前主流的访问方式有：**使用句柄**、**直接指针**。

**使用句柄：需要使用句柄池转到指针， 但是方便移动对象**

**直接使用指针：定位更快**





## 类加载过程详解

简单回顾一下类加载过程。

- 类加载过程：**加载->连接->初始化**。
- 连接过程又可分为三步：**验证->准备->解析**。

![类加载过程](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/d5c27259d176f877f8a4947266957d28.png)



- 类加载器是一个负责加载类的对象，用于实现类加载过程中的加载这一步。

- 每个 Java 类都有一个引用指向加载它的 `ClassLoader`。

- 数组类不是通过 `ClassLoader` 创建的（数组类没有对应的二进制字节流），是由 JVM 直接生成的。

简单来说，**类加载器的主要作用就是加载 Java 类的字节码（ `.class` 文件）到 JVM 中（在内存中生成一个代表该类的 `Class` 对象）。**



### 类加载器加载规则

JVM 启动的时候，并不会一次性加载所有的类，而是根据需要去动态加载。也就是说，大部分类在具体用到的时候才会去加载，这样对内存更加友好。

对于已经加载的类会被放在 `ClassLoader` 中。在类加载的时候，系统会首先判断当前类是否被加载过。已经被加载的类会直接返回，否则才会尝试加载。也就是说，对于一个类加载器来说，相同二进制名称的类只会被加载一次。





**类加载器分类，以及加载流程**

![类加载器层次关系图](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/f2e69943a7177210b2e5fff570bf4e7b/cb10529e430edb743c6cdbc89aebc247.png)



### Java类加载器的层次结构：

1. **Bootstrap ClassLoader（启动类加载器）**：负责加载Java核心类库（如`rt.jar`，`java.lang.*`等），由C++实现，无法在Java代码中直接访问。
2. **Extension ClassLoader（扩展类加载器）**：负责加载Java的扩展库（通常位于`lib/ext`目录下的类库）。
3. **Application ClassLoader（应用类加载器）**：也称为系统类加载器，负责加载用户类路径（classpath）下的类，**通常是我们自定义的类和第三方类库。**

## 双亲委派模型

### 双亲委派模型介绍

类加载器有很多种，当我们想要加载一个类的时候，具体是哪个类加载器加载呢？这就需要提到双亲委派模型了。

`ClassLoader` 类使用委托模型来搜索类和资源。每个 `ClassLoader` 实例都有一个相关的父类加载器。需要查找类或资源时，`ClassLoader` 实例会在试图亲自查找类或资源之前，将搜索类或资源的任务委托给其父类加载器



结合上面的源码，简单总结一下双亲委派模型的执行流程：

- 在类加载的时候，**系统会首先判断当前类是否被加载过。已经被加载的类会直接返回，否则才会尝试加载（每个父类加载器都会走一遍这个流程**）。
- **类加载器在进行类加载的时候，它首先不会自己去尝试加载这个类，而是把这个请求委派给父类加载器去完成（调用父加载器 `loadClass()`方法来加载类）。这样的话，所有的请求最终都会传送到顶层的启动类加载器 `BootstrapClassLoader` 中。**
- **只有当父加载器反馈自己无法完成这个加载请求（它的搜索范围中没有找到所需的类）时，子加载器才**会尝试自己去加载（调用自己的 `findClass()` 方法来加载类）。



双亲委派模型保证了 Java 程序的稳定运行，可以避免类的重复加载（JVM 区分不同类的方式不仅仅根据类名，相同的类文件被不同的类加载器加载产生的是两个不同的类），也保证了 Java 的核心 API 不被篡改。



在面向对象编程中，有一条非常经典的设计原则：**组合优于继承，多用组合少用继承。**









# JVM参数调优

## 内存

- 指定堆内存
- 指定新生代内存

## GC

- 指定垃圾回收器



## 其他

- 









# ref

[JVM面试题，54道Java虚拟机八股文（1.5万字51张手绘图），面渣逆袭必看👍 | 二哥的Java进阶之路](https://javabetter.cn/sidebar/sanfene/jvm.html#_17-%E5%AF%B9%E8%B1%A1%E4%BB%80%E4%B9%88%E6%97%B6%E5%80%99%E4%BC%9A%E8%BF%9B%E5%85%A5%E8%80%81%E5%B9%B4%E4%BB%A3)



