---
title: java反射
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



# 反射概念

Java的反射（reflection）机制是指在程序的运行状态中，可以构造任意一个类的对象，可以了解任意一个对象所属的类，可以了解任意一个类的成员变量和方法，可以调用任意一个对象的属性和方法。 这种动态获取程序信息以及动态调用对象的功能称为Java语言的反射机制。

- 实现对象的创建
- 实现了解对象的类的所有属性。



## 反射的实现方法？

> 1. Class.forName(“类的路径”)
> 2. 类名.class
> 3. 对象名.getClass()
> 4. 基本类型的包装类，可以调用包装类的Type属性来获得该包装类的Class对象





## 利用反射动态创建对象实例

> 1. Class 对象的 newInstance()
>
>    使用 Class 对象的 newInstance()方法来创建该 Class 对象对应类的实例，但是这种方法要求该 Class 对象对应的类有默认的空构造器。
>
> 2. 调用 Constructor 对象的 newInstance()
>
>    先使用 Class 对象获取指定的 Constructor 对象，再调用 Constructor 对象的 newInstance()方法来创建 Class 对象对应类的实例,通过这种方法可以选定构造方法创建实例。
>
>    
>
>    ```java
>    //获取 Person 类的 Class 对象
>    Class clazz=Class.forName("reflection.Person");
>    //使用.newInstane 方法创建对象
>    Person p=(Person) clazz.newInstance();
>    //获取构造方法并创建对象
>    Constructor c=clazz.getDeclaredConstructor(String.class,String.class,int.class);
>    //创建对象并设置属性13/04/2018
>    Person p1=(Person) c.newInstance("李四","男",20);
>    ```





## spring与反射



### 创建 Bean 实例时的反射

```
// 通过类加载器，根据 class 路径，得到其类对象
Class<?> clz = Thread.currentThread().getContextClassLoader().loadClass("org.deppwang.litespring.v1.service.PetStoreService");
// 根据类对象生成 Bean 实例
return clz.newInstance();
```

### 构造方法依赖注入时的反射

```
// 通过反射获取当前类所有的构造方法信息（Constructor 对象）
Constructor<?>[] candidates = beanClass.getDeclaredConstructors();
// 设置构造方法参数实例
Object[] argsToUse = new Object[parameterTypes.length];
argsToUse[i] = getBean(beanNames.get(i));
// 使用带有参数的 Constructor 对象实现实例化 Bean。此时使用反射跟上面一样（newInstance0），只是多了参数
return constructorToUse.newInstance(argsToUse);
```

## class 文件与类对象

class 文件由 java 文件编译而来，class 文件包含字段表、方法表、`<init>` 方法（构造方法）等。

当类加载器将 class 文件加载进虚拟机元数据区（方法区，jdk1.7）时，虚拟机创建一个与之对应的类对象（Class 实例）。并将 class 文件由存放在磁盘的静态结构转换为存放在内存的运行时结构。

我们可以认为一个类（class 文件）对应一个类对象，当前类的所有对象共用一个类对象。**类对象作为访问存放在 jvm 的 class 文件的入口。**













# ref

[Spring 中的反射与反射的原理 - 掘金](https://juejin.cn/post/6844904148316471310)







