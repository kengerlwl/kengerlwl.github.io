---
title: java并发多线程相关
top: false
cover: false
toc: true
mathjax: true
hidden: true
date: 2024-03-25 15:27:31
password:
summary:
tags:
- java
categories:
- find JOB

---







## 守护线程与用户线程有什么区别？

> - **守护线程**：运行在后台，为其他前台线程服务。也可以说守护线程是 JVM 中非守护线程的 “佣人”。一旦所有用户线程都结束运行，守护线程会随 JVM 一起结束工作。
> - **用户线程**：运行在前台，执行具体的任务，如程序的主线程、连接网络的子线程等都是用户线程。



## 创建线程的四种方式？

> 1. **继承Thread类**
> 2. **实现 Runnable 接口**
> 3. **使用 Callable 和 Future 创建线程**
> 4. **使用线程池创建线程**

### 继承Thread类

**执行start后，创建子线程，现成进入就绪状态。然后自动执行run函数内容**

```java
public class CreateThread extends Thread{
    @Override
    public void run() {
        //获取线程名
        System.out.println(Thread.currentThread().getName());
    }

    public static void main(String[] args) {
        CreateThread createThread = new CreateThread();
        //线程启动
        createThread.start();
    }
}
```





### 实现Runnable接口

**也要实现run函数**

```java
public class RunnableCreateThread implements Runnable{
    @Override
    public void run() {
        System.out.println("实现Runnable接口创建线程");
    }

    public static void main(String[] args) {
        new Thread(new RunnableCreateThread()).start();
    }
}

```

### 使用Callable和Future创建线程

与 Runnable 接口不一样，Callable 接口提供了一个 call() 方法作为线程执行体，call() 方法比 run() 方法功能要强大，比如：call() 方法可以有返回值、call() 方法可以声明抛出异常。

```java
public class MyCallable implements Callable {
    @Override
    public Object call() throws Exception {
        System.out.println(Thread.currentThread().getName());
        return "huahua";
    }

    public static void main(String[] args) {
        //创建 FutureTask 对象
        FutureTask futureTask = new FutureTask<>(new MyCallable());
        //创建线程并启动
        Thread thread = new Thread(futureTask);
        thread.start();
        try {
            Thread.sleep(1000);
            //获取返回值
            System.out.println("返回的结果是：" + futureTask.get());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

```

### 基于线程池创建线程

```java
public class CreateThreadByExecutors implements Runnable {
    
    public static void main(String[] args) {
        ExecutorService service = Executors.newSingleThreadExecutor();
        CreateThreadByExecutors thread = new CreateThreadByExecutors();
        for (int i = 0; i < 10; i++) {
            service.execute(thread);
            System.out.println("=======任务开始=========");
            service.shutdown();
        }
    }

    @Override
    public void run() {
        System.out.println("hello Thread");
    }
}
```







## 线程的 run()和 start()有什么区别？

> - 每个线程都是通过某个特定Thread对象所对应的方法run()来完成其操作的，run()方法称为线程体。通过调用Thread类的start()方法来启动一个线程。
> - **start() 方法用于启动线程，run() 方法用于执行线程的运行时代码**。run() 可以重复调用，而 start()只能调用一次。
> - **start()方法来启动一个线程，真正实现了多线程运行**。调用start()方法无需等待run方法体代码执行完毕，可以直接继续执行其他的代码； 此时线程是处于就绪状态，并没有运行。 然后通过此Thread类调用方法run()来完成其运行状态， run()方法运行结束， 此线程终止。然后CPU再调度其它线程。
> - **run()方法是在本线程里的，只是线程里的一个函数，而不是多线程的**。 如果直接调用run()，其实就相当于是调用了一个普通函数而已，直接待用run()方法必须等待run()方法执行完毕才能执行下面的代码，所以执行路径还是只有一条，根本就没有线程的特征，所以在多线程执行时要使用start()方法而不是run()方法





## java线程调度

**分时调度模型**和抢占式调度模型。

- **分时调度模型**是指让所有的线程轮流获得 cpu 的使用权，并且平均分配每个线程占用的 CPU的时间片这个也比较好理解。
- **Java虚拟机采用抢占式调度模型**，是指优先让可运行池中优先级高的线程占用CPU，如果可运行池中的线程优先级相同，那么就随机选择一个线程，使其占用CPU。处于运行状态的线程会一直运行，直至它不得不放弃



## 如何在两个线程间共享数据？

> **在两个线程间共享变量即可实现共享。**
>
> 一般来说，共享变量要求变量本身是线程安全的，然后在线程内使用的时候，如果有对共享变量的复合操作，那么也得保证复合操作的线程安全性

例如，ConcurrentHashMap



## 线程安全

**线程安全指的是当多个线程同时访问一个共享资源时，系统仍然能够正确地工作，且不会导致数据的损坏或不一致。**在具有线程安全性的程序中，对共享数据结构或对象的并发访问**不会导致竞态条件、数据竞争**或其他类似问题。线程安全的实现应该保证在并发环境下不会出现意外或不确定的行为。

确保线程安全的方法通常包括使用同步机制（**如 synchronized 关键字、Locks**）、使用线程安全的数据结构、避免共享可变状态等。编写线程安全的代码对于多线程环境下的应用程序至关重要，可以避免数据错乱、死锁等问题，确保程序的正确性和稳定性。





## 什么是线程同步和线程互斥，有哪几种实现方式？



> **线程同步**：**当一个线程对共享的数据进行操作时，应使之成为一个”原子操作“**，即在没有完成相关操作之前，不允许其他线程打断它，否则，就会破坏数据的完整性，必然会得到错误的处理结果。
>
> **线程互斥**：是指对于共享的进程系统资源，在各单个线程访问时的排它性。当有若干个线程都要使用某一共享资源时，任何时刻最多只允许一个线程去使用，其它要使用该资源的线程必须等待，直到占用资源者释放该资源。线程互斥可以看成是一种特殊的线程同步。
>
> 线程间同步的方法分为两类：**用户模式**和**内核模式**
>
> - 内核模式：就是指利用系统内核对象的单一性来进行同步，使用时需要切换内核态与用户态。
>
>   方法：
>
>   - 事件
>   - 信号量
>   - 互斥量
>
> - 用户模式：不需要切换到内核态，只在用户态完成操作。
>
>   方法：
>
>   - 原子操作
>   - 临界区

**线程同步的方法**：

1. 同步代码方法：**sychronized关键字修饰的方法**
2. 同步代码块：**sychronized关键字修饰的代码块**
3. 使用特殊变量域Volatile实现线程同步：volatile关键字为域变量的访问提供了一种免锁机制
4. 使用重入锁实现线程同步：reentrantlock类是可冲入、互斥、实现了lock接口的锁他与sychronized方法具有相同的基本行为和语

## 在 Java 程序中怎么保证多线程的运行安全？

> - 使用安全类，比如 java.util.concurrent 下的类，使用原子类AtomicInteger。（这些类本身就线程安全了）
> - 使用自动锁sychronized
> - 使用手动锁Lock

### ReentrantLock手动锁

- `ReentrantLock` 是基于可重入原理设计的锁，**一个线程可以多次获取同一个 `ReentrantLock`，而不会导致死锁**。即线程在持有锁的情况下，可以再次获取该锁而不被阻塞。（**`synchronized` 也是可重入的**）

```
Lock lock = new ReentrantLock();
lock. lock();
try {
    System. out. println("获得锁");
} catch (Exception e) {
// TODO: handle exception
} finally {
    System. out. println("释放锁");
    lock. unlock();
}

```

### synchronized 关键字的底层原理？

> Synchronized【对象锁】**采用互斥的方式让同一时刻至多只有一个线程能持有【对象锁】，其它线程再想获取这个【对象锁】时就会阻塞住**

> **Synchronized 底层其实就是一个 Monitor**，Monitor 被翻译为监视器，是由 jvm 提供，c++语言实现
>
> - **Monitor 实现的锁属于重量级锁，你了解过锁升级吗？**
>
>   - **Monitor 实现的锁属于重量级锁，里面涉及到了用户态和内核态的切换、进程的上下文切换，成本较高，性能比较低。**
>
>     

**Java 中的 synchronized 有偏向锁、轻量级锁、重量级锁三种形式，分别对应了锁只被一个线程持有、不同线程交替持有锁、多线程竞争锁三种情况。**

|          | **描述**                                                     |
| -------- | ------------------------------------------------------------ |
| 重量级锁 | 底层使用的 Monitor 实现，里面涉及到了用户态和内核态的切换、进程的上下文切换，成本较高，性能比较低。 |
| 轻量级锁 | 线程加锁的时间是错开的（也就是没有竞争），可以使用轻量级锁来优化。轻量级修改了对象头的锁标志，相对重量级锁性能提升很多。每次修改都是 CAS 操作，保证原子性 |
| 偏向锁   | **一段很长的时间内都只被一个线程使用锁，可以使用了偏向锁**，在第一次获得锁时，会有一个 CAS 操作，之后该线程再获取锁，只需要判断 mark word 中是否是自己的线程 id 即可，而不是开销相对较大的 CAS 命令 |

**一旦锁发生了竞争，都会升级为重量级锁**





###  ReentrantLock 和synchronized 区别

- **在性能上**，`ReentrantLock` 相对于 `synchronized` 更加灵活，性能也更好。因为 `ReentrantLock` 的实现采用了 CAS 操作，可以更好地支持高并发场景。
- **灵活性上**，`ReentrantLock` 提供了更灵活的锁获取方式，例如可以尝试非阻塞地获取锁、设定超时时间、以及支持可中断的锁获取等功能。
- **可中断性**：
  - `ReentrantLock` 支持可中断的锁获取，即在等待锁的过程中，可以响应中断，而不会一直等待下去。
  - `synchronized` 关键字在等待锁的过程中，是不可中断的，即线程一旦进入等待状态，只能等待锁的释放，无法响应中断。



 synchronized 相比

|          | ReentrantLock                  | Synchronized   |
| -------- | ------------------------------ | -------------- |
| 锁机制   | 依赖 AQS                       | 监视器模式     |
| 灵活性   | 支持响应中断，超时，尝试获取锁 | 不灵活         |
| 释放形式 | unlock()方法释放锁             | 自动释放监视器 |
| 锁类型   | 公平锁&非公平锁                | 非公平锁       |
| 条件队列 | 可关联多个队列                 | 关联一个队列   |
| 可重入性 | 可重入                         | 可重入         |





## 多线程的常用方法？

|     方法名      |            描述            |
| :-------------: | :------------------------: |
|     sleep()     | **强迫一个线程睡眠Ｎ毫秒** |
|    isAlive()    |    判断一个线程是否存活    |
|     join()      |      **等待线程终止**      |
|  activeCount()  |     程序中活跃的线程数     |
|   enumerate()   |      枚举程序中的线程      |
| currentThread() |      **得到当前线程**      |
|   isDaemon()    |       是否为守护线程       |
|   setDaemon()   |       设置为守护线程       |
|    setName()    |     为线程设置一个名称     |
|     wait()      |    **强迫一个线程等待**    |
|    notify()     |  **通知一个线程继续运行**  |
|  setPriority()  |    设置一个线程的优先级    |









## synchronized对象锁和类锁简介

我们可以从synchronized加锁位置区分对象锁和类锁。

**1、对象锁**

普通同步方法，锁是当前实例对象。比如：

```java
public synchronized void doLongTimeTaskC() {}
```

**2、类锁**

静态同步方法，锁是当前类的Class对象。比如：

```java
public synchronized static void doLongTimeTaskA() {}
```

**3、同步代码块上的对象锁或类锁**

加在同步代码块上，锁是Synchonized括号里配置的对象，可以是实例对象，也可以是Class对象；

```java
public void doLongTimeTaskD() {
    // 对象锁
    synchronized (this) {
    }
}
```

或

```java
public static void doLongTimeTaskE() {

    // 类锁
    synchronized (Task.class) {
    }

}
```

对象锁和类锁是两个完全不一样的锁，下面通过实例看看他们的区别





### 对象锁

**总结：**

**多线程分别持有多个对象，每个线程异步执行对象的同步方法，因为JVM为每个对象创建了锁。**

**如果想让线程排队执行，让多个线程持有同一个对象，线程就会排队执行。**



### 类级锁

这就是结果按顺序输出的原因，这也是类锁的特性，多个线程持有一个类锁，排队执行，持有就是王者，





## java 线程相关结构





![Java 运行时数据区域（JDK1.8 之后）](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/bb65bdb9c9fd2ec81565504ae3c020cd/ab3aa96730a25c95c8e9a6b6c184d643.png)

- 程序计数器私有主要是为了**线程切换后能恢复到正确的执行位置**
- **虚拟机栈：** 每个 Java 方法在执行之前会创建一个栈帧用于存储局部变量表、操作数栈、常量池引用等信息。从方法调用直至执行完成的过程，就对应着一个栈帧在 Java 虚拟机栈中入栈和出栈的过程。
- **本地方法栈：** 和虚拟机栈所发挥的作用非常相似，区别是：**虚拟机栈为虚拟机执行 Java 方法 （也就是字节码）服务，而本地方法栈则为虚拟机使用到的 Native 方法服务。** 在 HotSpot 虚拟机中和 Java 虚拟机栈合二为一。





## 线程池

### 线程池有几种实现方式？

> 线程池的创建方法总共有 7 种，但总体来说可分为 2 类：
>
> 1. 通过 ThreadPoolExecutor 创建的线程池；
> 2. 通过 Executors 创建的线程池。

![image-20231114150834495](https://javaxiaobear-1301481032.cos.ap-guangzhou.myqcloud.com/picture-bed/image-20231114150834495.png)



### 自定义线程池的各个参数含义？

> **参数 1：corePoolSize**
>
> 核心线程数，线程池中**始终存活的线程数**。
>
> **参数 2：maximumPoolSize**
>
> **最大线程数，线程池中允许的最大线程数，当线程池的任务队列满了之后可以创建的最大线程数。**
>
> **参数 3：keepAliveTime**
>
> 最大线程数可以存活的时间，当线程中没有任务执行时，最大线程就会销毁一部分，最终保持核心线程数量的线程。
>
> **参数 4：unit**
>
> 单位是和参数 3 存活时间配合使用的，合在一起用于设定线程的存活时间 
>
> **参数 5：workQueue**
>
> 一个阻塞队列，用来存储线程池等待执行的任务，均为线程安全，它包含以下 7 种类型：
>
> - ArrayBlockingQueue：一个由数组结构组成的有界阻塞队列；
> - LinkedBlockingQueue：一个由链表结构组成的有界阻塞队列；
> - SynchronousQueue：一个不存储元素的阻塞队列，即直接提交给线程不保持它们；
> - PriorityBlockingQueue：一个支持优先级排序的无界阻塞队列；
> - DelayQueue：一个使用优先级队列实现的无界阻塞队列，只有在延迟期满时才能从中提取元素；
> - LinkedTransferQueue：一个由链表结构组成的无界阻塞队列。与 SynchronousQueue 类似，还含有非阻塞方法；
> - LinkedBlockingDeque：一个由链表结构组成的双向阻塞队列。
>
> 较常用的是 LinkedBlockingQueue 和 Synchronous，线程池的排队策略与 BlockingQueue 有关。
>
> **参数 6：threadFactory**
>
> 线程工厂，主要用来创建线程，默认为正常优先级、非守护线程。
>
> **参数 7：handler**
>
> 拒绝策略，拒绝处理任务时的策略，系统提供了 4 种可选：

### 线程池运行逻辑

这个线程池的特点是：

- **当有新任务提交时**，如果核心线程数小于 `corePoolSize`，则会创建新的核心线程来执行任务。
- **如果核心线程数已达到 `corePoolSize`**，但是等待队列未满，则任务会被添加到等待队列中。
- **如果等待队列已满，**但是当前线程数小于 `maximumPoolSize`，**则会创建新的非核心线程来执行任务。**
- **如果当前线程数已达到 `maximumPoolSize`，并且等待队列也已满，则根据线程池的拒绝策略来处理新任务。**



## wait vs sleep 的区别

> 共同点：wait() ，wait(long) 和 sleep(long) 的效果都是**让当前线程暂时放弃 CPU 的使用权，进入阻塞状态**
>
> 不同点：
>
> | 不同点   | wait                                                         | sleep                                                        |
> | -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
> | 方法归属 | wait()，wait(long) 都是 Object 的成员方法，每个对象都有      | sleep(long) 是 Thread 的静态方法                             |
> | 醒来时机 | wait(long) 和 wait() 还可以被 notify 唤醒，wait() 如果不唤醒就一直等下去, 它们都可以被打断唤醒 | 执行 sleep(long) 和 wait(long) 的线程都会在等待相应毫秒后醒来, 它们都可以被打断唤醒 |
> | 锁特性   | wait 方法的调用必须先获取 wait 对象的锁   **wait 方法执行后会释放对象锁，允许其它线程获得该对象锁**（我放弃 cpu，但你们还可以用） | 而 sleep 则无此限制   sleep 如果在 synchronized 代码块中执行，**并不会释放对象锁**（我放弃 cpu，你们也用不了） |





## JMM（Java 内存模型）

所有的**共享变量都存储于主内存**(计算机的 RAM)这里所说的变量指的是实例变量和类变量。不包含局部变量，因为局部变量是线程私有的，因此不存在竞争问题。

每一个线程还存在自己的工作内存，**线程的工作内存，保留了被线程使用的变量的工作副本。**

**线程对变量的所有的操作(读，写)都必须在工作内存中完成**，而不能直接读写主内存中的变量，**不同线程之间也不能直接访问对方工作内存中的变量，线程间变量的值的传递需要通过主内存完成。**



![image-20231113221403439](https://javaxiaobear-1301481032.cos.ap-guangzhou.myqcloud.com/picture-bed/image-20231113221403439.png)





## 你了解 ThreadLocal 吗？

> **作用**
>
> - ThreadLocal 可以实现【资源对象】的线程隔离，让每个线程各用各的【资源对象】，避免争用引发的线程安全问题
>
> - ThreadLocal 同时实现了线程内的资源共享
>
> - **每个线程内有一个 ThreadLocalMap 类型的成员变量，用来存储资源对象**
>
>   - 调用 set 方法，就是**以 ThreadLocal（对象） 自己作为 key，资源对象作为 value**，放入当前线程的 ThreadLocalMap 集合中（**一个线程可以有多个ThreadLocal实例，用于存储不同类型的值，例如int，string**）
>   - 调用 get 方法，就是以 ThreadLocal 自己作为 key，到当前线程中查找关联的资源值
>   - 调用 remove 方法，就是以 ThreadLocal 自己作为 key，移除当前线程关联的资源值
>
>   





## 什么是 volatile 关键字？它的作用是什么？

> `volatile` 是 Java 中的关键字，用于修饰变量。它的主要作用是确保多个线程之间对变量的可见性和有序性。当一个变量被声明为
>
> `volatile` 时，它将具备以下特性：
>
> - **可见性：对一个 `volatile` 变量的写操作会立即被其他线程可见，读操作也会读取最新的值。（volatile 关键字会强制将修改的值立即写入主存。）**
> - **有序性：`volatile` 变量的读写操作具备一定的顺序性，不会被重排序。**
>   - **禁止进行指令重排序**实现有序性

## `volatile` 关键字与单例模式

> - 在双重检查锁定的单例模式中，**使用 `volatile` 关键字修饰单例对象的引用，可以确保多线程环境下的正确性。**
> - **`volatile` 关键字可以防止指令重排序，从而避免在多线程环境下获取到未完全初始化的实例对象。**
