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

与 Runnable 接口不一样，Callable 接口提供了一个 call() 方法作为线程执行体，call() 方法比 run() 方法功能要强大，比如**：call() 方法可以有返回值、call() 方法可以声明抛出异常。**

为什么要用到这个：



- **提高并发性和响应性**：通过使用 Future，可以在等待某些操作完成时不阻塞程序的执行，从而提高程序的并发性和响应性。这对于处理大量IO密集型任务非常有用。
- **异步编程**：Future 是异步编程的基础之一。**在处理需要长时间等待的任务时，异步编程可以使得程序在等待结果的同时继续执行其他任务，而不是被阻塞。**
- **支持函数式编程**：Callable 对于函数式编程很重要，它允许将函数作为参数传递给其他函数，或者将函数作为返回值返回，这种机制可以极大地增加代码的灵活性和复用性。

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
    lock. unlock(); // 之所以用这个是为了防止锁不释放
}

```

#### ReentrantReadWriteLock 是什么？

`ReentrantReadWriteLock` 其实是两把锁，**一把是 `WriteLock` (写锁)，一把是 `ReadLock`（读锁） 。读锁是共享锁，写锁是独占锁**。读锁可以被同时读，可以同时被多个线程持有，而写锁最多只能同时被一个线程持有。（**兼容性和数据库那边是一致的**）







### synchronized 关键字的底层原理？

> Synchronized【对象锁】**采用互斥的方式让同一时刻至多只有一个线程能持有【对象锁】，其它线程再想获取这个【对象锁】时就会阻塞住**

> **Synchronized 底层其实就是一个 Monitor**，Monitor 被翻译为监视器，是由 jvm 提供，c++语言实现
>
> - **Monitor 实现的锁属于重量级锁，你了解过锁升级吗？**
>
>   - **Monitor 实现的锁属于重量级锁，里面涉及到了用户态和内核态的切换、进程的上下文切换，成本较高，性能比较低。**
> - **相当于用monitor实现了一个锁的计数器**
>

![执行 monitorexit 释放锁](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/bb65bdb9c9fd2ec81565504ae3c020cd/526b027d891fa58c2ee2203ed2484942.png)

**Java 中的 synchronized 有偏向锁、轻量级锁、重量级锁三种形式，分别对应了锁只被一个线程持有、不同线程交替持有锁、多线程竞争锁三种情况。**

|          | **描述**（越往下，越轻量级，开销越小）                       |
| -------- | ------------------------------------------------------------ |
| 重量级锁 | 底层使用的 Monitor 实现，里面涉及到了用户态和内核态的切换、进程的上下文切换，成本较高，性能比较低。 |
| 轻量级锁 | 线程加锁的时间是错开的（也就是没有竞争），可以使用轻量级锁来优化。轻量级修改了对象头的锁标志，相对重量级锁性能提升很多。每次修改都是 CAS 操作，保证原子性 |
| 偏向锁   | **一段很长的时间内都只被一个线程使用锁，可以使用了偏向锁**，在第一次获得锁时，会有一个 CAS 操作，**之后该线程再获取锁，只需要判断 mark word 中是否是自己的线程 id 即可，而不是开销相对较大的 CAS 命令** |

**一旦锁发生了竞争，都会升级为重量级锁**





###  ReentrantLock 和synchronized 区别

**相同点**

- **二者都是可重入锁**，
-  Java 中`synchronized`和`ReentrantLock`等独占锁就是悲**观锁思想的实现。**



**不同点**：

- **在性能上**，`ReentrantLock` 相对于 `synchronized` 更加灵活，性能也更好。因为 `ReentrantLock` 的实现采用了 CAS 操作，可以更好地支持高并发场景。
- **灵活性上**，`ReentrantLock` 提供了更灵活的锁获取方式，例如可以尝试非阻塞地获取锁、设定超时时间、以及支持可中断的锁获取等功能。
- **可中断性**：
  - `ReentrantLock` 支持可中断的锁获取，即在等待锁的过程中，可以响应中断，而不会一直等待下去。
  - `synchronized` 关键字在等待锁的过程中，是不可中断的，即线程一旦进入等待状态，只能等待锁的释放，无法响应中断。
- ReentrantLock 比 synchronized 增加了一些高级功能**（可中断，公平锁，）**



 synchronized 相比

|          | ReentrantLock                                                | Synchronized         |
| -------- | ------------------------------------------------------------ | -------------------- |
| 锁机制   | **依赖 AQS（AbstractQueuedSynchronizer）**                   | **监视器模式**       |
| 灵活性   | **支持响应中断（获取锁的过程可以中断）**，**超时（超时自动中断）**，尝试获取锁 | 不灵活，**不可中断** |
| 释放形式 | unlock()方法释放锁                                           | 自动释放监视器       |
| 锁类型   | 公平锁&非公平锁（**释放锁后是否按照FCFS的公平原则**）        | 非公平锁             |
| 条件队列 | 可关联多个队列                                               | 关联一个队列         |
| 可重入性 | **可重入**                                                   | **可重入**           |





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

**synchronized相比于ReentrantLock其实是隐式生成锁。**

**1、对象锁**

**普通同步方法，锁是当前实例对象。**比如：

```java
public synchronized void doLongTimeTaskC() {}
```

**2、类锁**

**静态同步方法，锁是当前类的Class对象**。比如：

```java
public synchronized static void doLongTimeTaskA() {}
```

**3、同步代码块上的对象锁或类锁**

**加在同步代码块上，锁是Synchonized括号里配置的对象（任何对象），可以是实例对象，也可以是Class对象；**



```java
public void doLongTimeTaskD() {
    // 对象锁，实际上可以直接锁住任何对象
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

// **对象锁，实际上可以直接锁住任何对象（Object）。不仅仅是this。**

### 类级锁

这就是结果按顺序输出的原因，这也是类锁的特性，多个线程持有一个类锁，排队执行，持有就是王者，





## java 线程相关结构





![Java 运行时数据区域（JDK1.8 之后）](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/bb65bdb9c9fd2ec81565504ae3c020cd/ab3aa96730a25c95c8e9a6b6c184d643.png)

- 程序计数器私有主要是为了**线程切换后能恢复到正确的执行位置**
- **虚拟机栈：** 每个 Java 方法在执行之前会创建一个栈帧用于存储局部变量表、操作数栈、常量池引用等信息。从方法调用直至执行完成的过程，就对应着一个栈帧在 Java 虚拟机栈中入栈和出栈的过程。
- **本地方法栈：** 和虚拟机栈所发挥的作用非常相似，区别是：**虚拟机栈为虚拟机执行 Java 方法 （也就是字节码）服务，而本地方法栈则为虚拟机使用到的 Native 方法服务。** 在 HotSpot 虚拟机中和 Java 虚拟机栈合二为一。





## 线程池



### **使用线程池的好处**：

- **降低资源消耗**。通过重复利用已创建的线程降低线程创建和销毁造成的消耗。
- **提高响应速度**。当任务到达时，任务可以不需要等到线程创建就能立即执行。
- **提高线程的可管理性**。线程是稀缺资源，如果无限制的创建，不仅会消耗系统资源，还会降低系统的稳定性，使用线程池可以进行统一的分配，调优和监控



### 线程池有几种实现方式？

> 线程池的创建方法总共有 7 种，但总体来说可分为 2 类：
>
> 1. 通过 ThreadPoolExecutor 创建的线程池；
>
> 2. 通过 Executors 创建的线程池。
>
>    1. `FixedThreadPool`：**固定线程数量的线程池**。该线程池中的线程数量始终不变。当有一个新的任务提交时，线程池中若有空闲线程，则立即执行。若没有，则新的任务会被暂存在一个任务队列中，待有线程空闲时，便处理在任务队列中的任务。
>
>    2. `SingleThreadExecutor`： **只有一个线程的线程池**。若多余一个任务被提交到该线程池，任务会被保存在一个任务队列中，待线程空闲，按先入先出的顺序执行队列中的任务。
>
>    3. `CachedThreadPool`： **可根据实际情况调整线程数量的线程池。线程池的线程数量不确定**，但若有空闲线程可以复用，则会优先使用可复用的线程。若所有线程均在工作，又有新的任务提交，则会创建新的线程处理任务。所有线程在当前任务执行完毕后，将返回线程池进行复用。
>
>    4. `ScheduledThreadPool`：给**定的延迟后运行任务或者定期执行任务的线程池。**
>
>    

![image-20231114150834495](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/bb65bdb9c9fd2ec81565504ae3c020cd/3671a9e49ffb7bce0d3f775cee82f939.png)



### 自定义线程池ThreadPoolExecutor的各个参数含义？

> **参数 1：corePoolSize**
>
> 核心线程数，线程池中**始终存活的线程数**。
>
> **参数 2：maximumPoolSize**
>
> **最大线程数，线程池中允许的最大线程数，当线程池的任务队列满了之后可以创建的最大线程数。**
>
> 当**队列中存放的任务达到队列容量的时候**，**当前可以同时运行的线程数量变为最大线程数。**
>
> **参数 3：keepAliveTime**
>
> **最大线程数可以存活的时间，当线程中没有任务执行时，最大线程就会销毁一部分，最终保持核心线程数量的线程。**
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
> - **PriorityBlockingQueue：一个支持优先级排序的无界阻塞队列；**
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

### 线程池数量确定

有一个简单并且适用面比较广的公式：

- **CPU 密集型任务(N+1)：** 这种任务消耗的主要是 CPU 资源，可以将线程数设置为 **N（CPU 核心数）+1**。比 CPU 核心数多出来的一个线程是为了防止线程偶发的缺页中断，或者其它原因导致的任务暂停而带来的影响。一旦任务暂停，CPU 就会处于空闲状态，而在这种情况下多出来的一个线程就可以充分利用 CPU 的空闲时间。
- **I/O 密集型任务(2N)：** 这种任务应用起来，系统会用大部分的时间来处理 I/O 交互，而线程在处理 I/O 的时间段内不会占用 CPU 来处理，这时就可以将 CPU 交出给其它线程使用。因此在 I/O 密集型任务的应用中，我们可以多配置一些线程，具体的计算方法是 2N。



## wait vs sleep 的区别

> 共同点：wait() ，wait(long) 和 sleep(long) 的效果都是**让当前线程暂时放弃 CPU 的使用权，进入阻塞状态**
>
> 不同点：
>
> | 不同点   | wait                                                         | sleep                                                        |
> | -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
> | 方法归属 | wait()，wait(long) 都是 Object 的成员方法，每个对象都有      | sleep(long) 是 Thread 的静态方法                             |
> | 醒来时机 | wait(long) 和 wait() 还可以被 notify 唤醒，**wait() 如果不唤醒就一直等下去, 它们都可以被打断唤醒** | **执行 sleep(long) 和 wait(long) 的线程都会在等待相应毫秒后醒来, 它们都可以被打断唤醒** |
> | 锁特性   | wait 方法的调用必须先获取 wait 对象的锁   **wait 方法执行后会释放对象锁，允许其它线程获得该对象锁**（我放弃 cpu，但你们还可以用） | 而 sleep 则无此限制   sleep 如果在 synchronized 代码块中执行，**并不会释放对象锁**（我放弃 cpu，你们也用不了） |

- sleep在睡眠结束后，进入就绪状态，等待时间片分配再执行。

### **join()**:函数

- **`join()`是Thread类的方法，用于让一个线程等待另一个线程完成执行。当一个线程调用另一个线程的`join()`方法时，它会被阻塞，直到目标线程执行完成。**
- 可以用于等待特定线程的结束。不会释放CPU资源，



## JMM（Java 内存模型）

所有的**共享变量都存储于主内存**(计算机的 RAM)这里所说的变量指的是实例变量和类变量。不包含局部变量，因为局部变量是线程私有的，因此不存在竞争问题。

每一个线程还存在自己的工作内存，**线程的工作内存，保留了被线程使用的变量的工作副本。**

**线程对变量的所有的操作(读，写)都必须在工作内存中完成**，而不能直接读写主内存中的变量，**不同线程之间也不能直接访问对方工作内存中的变量，线程间变量的值的传递需要通过主内存完成。**



![image-20231113221403439](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/bb65bdb9c9fd2ec81565504ae3c020cd/10481c2c23931c67e9c66056a2dc1a88.png)





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

### 但是volatile**不能保证对变量的操作是原子性的。**

public class VolatileAtomicityDemo {
    public volatile static int inc = 0;

    public void increase() {
        inc++;
    }
    
    public static void main(String[] args) throws InterruptedException {
        ExecutorService threadPool = Executors.newFixedThreadPool(5);
        VolatileAtomicityDemo volatileAtomicityDemo = new VolatileAtomicityDemo();
        for (int i = 0; i < 5; i++) {
            threadPool.execute(() -> {
                for (int j = 0; j < 500; j++) {
                    volatileAtomicityDemo.increase();
                }
            });
        }
        // 等待1.5秒，保证上面程序执行完成
        Thread.sleep(1500);
        System.out.println(inc);
        threadPool.shutdown();
    }
}
正常情况下，运行上面的代码理应输出 2500。但你真正运行了上面的代码之后，你会发现每次输出结果都小于 2500。

为什么会出现这种情况呢？不是说好了，volatile 可以保证变量的可见性嘛！

也就是说，如果 volatile 能保证 inc++ 操作的原子性的话。每个线程中对 inc 变量自增完之后，其他线程可以立即看到修改后的值。5 个线程分别进行了 500 次操作，那么最终 inc 的值应该是 5*500=2500。

很多人会误认为自增操作 inc++ 是原子性的，实际上，inc++ 其实是一个复合操作，包括三步：

- 读取 inc 的值。

- 对 inc 加 1。

- 将 inc 的值写回内存。

**volatile 是无法保证这三个操作是具有原子性的，有可能导致下面这种情况出现，解决办法：给increase函数加锁**



## `volatile` 关键字与单例模式

> - 在双重检查锁定的单例模式中，**使用 `volatile` 关键字修饰单例对象的引用，可以确保多线程环境下的正确性。**
> - **`volatile` 关键字可以防止指令重排序，从而避免在多线程环境下获取到未完全初始化的实例对象。**

**双重校验锁实现对象单例（线程安全）**：



```java
public class Singleton {

    private volatile static Singleton uniqueInstance;

    private Singleton() {
    }

    public  static Singleton getUniqueInstance() {
       //先判断对象是否已经实例过，没有实例化过才进入加锁代码
        if (uniqueInstance == null) {
            //类对象加锁
            synchronized (Singleton.class) {
                if (uniqueInstance == null) {
                    uniqueInstance = new Singleton();
                }
            }
        }
        return uniqueInstance;
    }
}
```



## 自旋锁是什么



在使用自旋锁时，如果线程尝试获取锁但锁已被其他线程占用，**该线程不会被挂起，而是会反复检测锁是否被释放。只有当获取锁成功后才会继续执行。**











# AQS

```java
AbstractQueuedSynchronizer 
```

AQS 核心思想是，**如果被请求的共享资源空闲，则将当前请求资源的线程设置为有效的工作线程，并且将共享资源设置为锁定状态**。

## 结构

![887fafe6f6b282d7443424fce2cadb9](C:\Users\kenger\Documents\WeChat Files\wxid_i60ep1lbq9cl22\FileStorage\Temp\887fafe6f6b282d7443424fce2cadb9.jpg)

相当于给目标资源加了一个state变量判断是否占用了该资源，然后有个队列用来存储当且需要这个资源的线程队列。

如果state >=1 ， 那么就会锁定这个资源。







**`ReentrantLock`，`Semaphore`，其他的诸如 `ReentrantReadWriteLock`，`SynchronousQueue`等等皆是基于 AQS 的**

## Semaphore信号量 有什么用？

synchronized 和 ReentrantLock 都是一次只允许一个线程访问某个资源，**而Semaphore(信号量)可以用来控制同时访问特定资源的线程数量。**





## CountDownLatch 有什么用？

**`CountDownLatch` 允许 `count` 个线程阻塞在一个地方，直至所有线程的任务都执行完毕。（适用于等待所有任务都执行解决后，统一获取结果再执行）** 

例如：我们要读取处理 6 个文件，这 6 个任务都是没有执行顺序依赖的任务，但是我们需要返回给用户的时候将这几个文件的处理的结果进行统计整理。



类似的还有更强大的**CyclicBarrier**





# 其他



## CAS机制



### CAS问题

- **循环时间长开销大**
  CAS 经常会用到自旋操作来进行重试，也就是不成功就一直循环执行直到成功
  - 优化：**暂停当前CPU核心**：`pause`指令会暂停当前逻辑核心的执行，在等待期间避免不必要的功耗浪费。





## 指令重排

**什么是指令重排序？** 简单来说就是系统在执行代码的时候并不一定是按照你写的代码的顺序依次执行。

**为什么会出现**：

- **编译器优化重排**：编译器（包括 JVM、JIT 编译器等）在不改变单线程程序语义的前提下，重新安排语句的执行顺序。

- **指令并行重排**：现代处理器采用了指令级并行技术(Instruction-Level Parallelism，ILP)来将多条指令重叠执行。如果不存在数据依赖性，处理器可以改变语句对应机器指令的执行顺序

Java 源代码会经历 **编译器优化重排 —> 指令并行重排 —> 内存系统重排** 的过程，最终才变成操作系统可执行的指令序列。

**java里面有volatile来实现禁止重排**。

将变量声明为 `volatile` ，这就指示 JVM，**这个变量是共享且不稳定的，每次使用它都到主存中进行读取**







## 线程安全容器



### ConcurrentHashMap

`HashMap` 的线程安全版本—— `ConcurrentHashMap` 的诞生。

**对数组的node上锁，最新1.8版本**

![Java8 ConcurrentHashMap 存储结构（图片来自 javadoop）](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/bb65bdb9c9fd2ec81565504ae3c020cd/f268edb660265d7a82b12875c3d27d81.png)

### BlockingQueue

`BlockingQueue` 是一个接口，继承自 `Queue`，所以其实现类也可以作为 `Queue` 的实现来使用，而 `Queue` 又继承自 `Collection` 接口

 3个常见的 `BlockingQueue` 的实现类：`ArrayBlockingQueue`、`LinkedBlockingQueue`、`PriorityBlockingQueue` 。

`ArrayBlockingQueue` 一旦创建，容量不能改变。**其并发控制采用可重入锁 `ReentrantLock` ，不管是插入操作还是读取操作，都需要获取到锁才能进行操作**。当队列容量满时，尝试将元素放入队列将导致操作阻塞;尝试从一个空队列中取一个元素也会同样阻塞。

### CopyOnWriteArrayList 

CopyOnWrite 是一个时髦的技术，不管是 Linux 还是 Redis 都会用到。**在 Java 中，CopyOnWriteArrayList 虽然是一个线程安全的 ArrayList，但因为其实现方式是，每次修改数据时都会复制一份数据出来，所以有明显的适用场景，即读多写少或者说希望无锁读的场景。**





## 常见原子类

**线程安全操作**

**基本类型**

使用原子的方式更新基本类型

- `AtomicInteger`：整型原子类
- `AtomicLong`：长整型原子类
- `AtomicBoolean`：布尔型原子类

**数组类型**

使用原子的方式更新数组里的某个元素

- `AtomicIntegerArray`：整型数组原子类
- `AtomicLongArray`：长整型数组原子类
- `AtomicReferenceArray`：引用类型数组原子类

**引用类型**

- `AtomicReference`：引用类型原子类



**一个经典问题：操作的原子性，并不等于事务的原子性，读取和写入都是原子性，但是先读后写这个过程不是原子性！！！！！！！！所以不是用了线程安全类就OK了**



## ThreadLocal 相关



### ThreadLocal 内存泄露问题

`ThreadLocalMap` 中使用的 key 为 `ThreadLocal` 的弱引用，**而 value 是强引用。所以，如果 `ThreadLocal` 没有被外部强引用的情况下，在垃圾回收的时候，key 会被清理掉，而 value 不会被清理掉。**

`ThreadLocalMap` 中就会出现 key 为 null 的 Entry。假如我们不做任何措施的话，value 永远无法被 GC 回收，这个时候就可能会产生内存泄露。`ThreadLocalMap` **实现中已经考虑了这种情况，在调用 `set()`、`get()`、`remove()` 方法的时候，会清理掉 key 为 null 的记录。使用完 `ThreadLocal`方法后最好手动调用`remove()`方法**







为了搞清楚这个问题，我们需要搞清楚`Java`的**四种引用类型**：

- **强引用**：我们常常 new 出来的对象就是强引用类型，只要强引用存在，垃圾回收器将永远不会回收被引用的对象，哪怕内存不足的时候
- **软引用**：使用 SoftReference 修饰的对象被称为软引用，软引用指向的对象在内存要溢出的时候被回收
- **弱引用**：使用 WeakReference 修饰的对象被称为弱引用，只要发生垃圾回收，若这个对象只被弱引用指向，那么就会被回收
- **虚引用**：虚引用是最弱的引用，在 Java 中使用 PhantomReference 进行定义。虚引用中唯一的作用就是用队列接收对象即将死亡的通知









## java虚拟线程

类似于协程

一个线程可以有多个虚拟线程。

适用于IO密集型任务。

