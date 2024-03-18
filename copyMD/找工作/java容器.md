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
- LinkedHashSet：**具有 HashSet 的查找效率，并且内部使用双向链表**维护元素的插入顺序。

#### 2. List

- ArrayList：基于动态数组实现，支持随机访问。
- Vector：和 ArrayList 类似，**但它是线程安全的**。
- LinkedList：基于双向链表实现，只能顺序访问，但是可以快速地在链表中间插入和删除元素。不仅如此，LinkedList 还可以用作栈、队列和双向队列。

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

