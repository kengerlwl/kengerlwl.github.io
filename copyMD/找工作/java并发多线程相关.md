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

> Synchronized【对象锁】采用互斥的方式让同一时刻至多只有一个线程能持有【对象锁】，其它线程再想获取这个【对象锁】时就会阻塞住

> Synchronized 底层其实就是一个 Monitor，Monitor 被翻译为监视器，是由 jvm 提供，c++语言实现

## 多线程的常用方法？

|     方法名      |          描述          |
| :-------------: | :--------------------: |
|     sleep()     | 强迫一个线程睡眠Ｎ毫秒 |
|    isAlive()    |  判断一个线程是否存活  |
|     join()      |      等待线程终止      |
|  activeCount()  |   程序中活跃的线程数   |
|   enumerate()   |    枚举程序中的线程    |
| currentThread() |      得到当前线程      |
|   isDaemon()    |     是否为守护线程     |
|   setDaemon()   |     设置为守护线程     |
|    setName()    |   为线程设置一个名称   |
|     wait()      |    强迫一个线程等待    |
|    notify()     |  通知一个线程继续运行  |
|  setPriority()  |  设置一个线程的优先级  |





