---
title: java容器
top: false
cover: false
toc: true
mathjax: true
date: 2023-08-22 15:27:31
password:
summary:
tags:
- java
categories:
- find JOB

---

## 概览

容器主要包括 Collection 和 Map 两种，Collection 存储着对象的集合，而 Map 存储着键值对（两个对象）的映射表。



### Collection

#### 1. Set

- TreeSet：**基于红黑树实现，支持有序性操作，**例如根据一个范围查找元素的操作。但是查找效率不如 HashSet，HashSet 查找的时间复杂度为 O(1)，TreeSet 则为 O(logN)。
- HashSet：**基于哈希表实现，支持快速查找，但不支持有序性操作**。并且失去了元素的插入顺序信息，也就是说使用 Iterator 遍历 HashSet 得到的结果是不确定的。
- LinkedHashSet：**具有 HashSet 的查找效率，并且内部使用双向链表**维护元素的插入顺序（**用于保证元素的插入和取出顺序满足 FIFO 的场景**）。

#### 2. List

- ArrayList：基于动态数组实现，支持随机访问**（线程不安全）**。
  - **扩容：ArrayList 每次扩容之后容量都会变为原来的 1.5 倍左右（oldCapacity 为偶数就是 1.5 倍，否则是 1.5 倍左右）**

- Vector：和 ArrayList 类似，**但它是线程安全的**。
- LinkedList：**基于双向链表实现**，只能顺序访问，但是可以快速地在链表中间插入和删除元素。不仅如此，LinkedList 还可以用作栈、队列和双向队列。**（线程不安全）**

#### 3. Queue

- LinkedList：可以用它来实现双向队列。
- PriorityQueue：基于堆结构实现，可以用它来实现优先队列。

### Map

- TreeMap：基于**红黑树**实现。
- HashMap：基于**哈希表**实现。
- HashTable：**和 HashMap 类似，但它是线程安全的**，这意味着同一时刻多个线程同时写入 HashTable 不会导致数据不一致。**它是遗留类，不应该去使用它，而是使用 ConcurrentHashMap 来支持线程安全**，ConcurrentHashMap 的效率会更高，因为 ConcurrentHashMap 引入了分段锁。
- LinkedHashMap：使用双向链表来维护元素的顺序，顺序为插入顺序或者最近最少使用（LRU）顺序。

## 容器中的设计模式

### 迭代器模式

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/6bb5bcfd83ad6f211856a971bad5f5fc/e52efe39290bdfbf8a743cd4aecc4f7e.png)



Collection 继承了 Iterable 接口，其中的 iterator() 方法能够产生一个 Iterator 对象，**通过这个对象就可以迭代遍历 Collection 中的元素**。

### 适配器模式

**适配器模式常被用于实现不同容器类型之间的转换或兼容**

java.util.Arrays#asList() 可以把数组类型转换为 List 类型。





## 各种常见数据结构





### HashMap 和 Hashtable 的区别

- **线程是否安全：** `HashMap` 是非线程安全的，**`Hashtable` 是线程安全的**,因为 `Hashtable` 内部的方法基本都**经过`synchronized` 修饰**。（如果你要保证线程安全的话就使用 `ConcurrentHashMap` 吧！）；
- **效率：** 因为线程安全的问题，`HashMap` 要比 `Hashtable` 效率高一点。另外，`Hashtable` 基本被淘汰，不要在代码中使用它；
- **对 Null key 和 Null value 的支持：** `HashMap` 可以存储 null 的 key 和 value，但 null 作为键只能有一个，null 作为值可以有多个；Hashtable 不允许有 null 键和 null 值，否则会抛出 `NullPointerException`。
- **初始容量大小和每次扩充容量大小的不同：** ① 创建时如果不指定容量初始值，`Hashtable` 默认的初始大小为 11，之后每次扩充，容量变为原来的 2n+1。`HashMap` 默认的初始化大小为 16。之后每次扩充，容量变为原来的 2 倍。② 创建时如果给定了容量初始值，那么 `Hashtable` 会直接使用你给定的大小，而 `HashMap` 会将其扩充为 2 的幂次方大小（`HashMap` 中的`tableSizeFor()`方法保证，下面给出了源代码）。也就是说 `HashMap` 总是使用 2 的幂作为哈希表的大小,后面会介绍到为什么是 2 的幂次方。
- **底层数据结构：** JDK1.8 以后的 `HashMap` 在解决哈希冲突时有了较大的变化，当链表长度大于阈值（默认为 8）时，将链表转化为红黑树（将链表转换成红黑树前会判断，如果当前数组的长度小于 64，那么会选择先进行数组扩容，而不是转换为红黑树），以减少搜索时间（后文中我会结合源码对这一过程进行分析）。`Hashtable` 没有这样的机制。



### HashMap 和 HashSet 区别

如果你看过 `HashSet` 源码的话就应该知道：`HashSet` 底层就是基于 `HashMap` 实现的



### HashSet 如何检查重复?

简而言之：就是先判断hashcode，如果没有一样的，那么必不重复，如果有，再判断equal函数判断是不是真相等。

以下内容摘自我的 Java 启蒙书《Head first java》第二版：

> 当你把对象加入`HashSet`时，`HashSet` 会先计算对象的`hashcode`值来判断对象加入的位置，同时也会与其他加入的对象的 `hashcode` 值作比较，如果没有相符的 `hashcode`，`HashSet` 会假设对象没有重复出现。但是如果发现有相同 `hashcode` 值的对象，这时会调用`equals()`方法来检查 `hashcode` 相等的对象是否真的相同。如果两者相同，`HashSet` 就不会让加入操作成功。







# 算法中的容器使用





## List<>使用

需要创建一个可变的，随机访问的队列。

```
        // 创建一个ArrayList作为队列
        List<Integer> queue = new ArrayList<>();
        
        // 添加元素到队列
        queue.add(10);
        // 修改队列中的元素
        queue.set(1, 25);
        
        // 删除队列中的元素
        queue.remove(2); // 删除索引为2的元素
        
        // 转换为int[]
        queue.toArray(new int[ans.size()][])
```







