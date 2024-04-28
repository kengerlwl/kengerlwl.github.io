---
title: java基础
top: false
cover: false
draft: true
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





## 数据类型

### 基本数据类型

![image-20210712152020611](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/e8da9232c588c9b3f04ef0372addef93/d6d2baff4b0ba2647046bf6d69619806.png)









## 运算

### 参数传递

**Java 的参数是以值传递的形式传入方法中，而不是引用传递。(但是由于java默认用的就是指针来指向对象，所以在函数里面改变对象实际也会改变)**

以下代码中 Dog dog 的 dog 是一个指针，存储的是对象的地址。在将一个参数传入一个方法时，本质上是将对象的地址以值的方式传递到形参中。

```java
public class Dog {

    String name;

    Dog(String name) {
        this.name = name;
    }

    String getName() {
        return this.name;
    }

    void setName(String name) {
        this.name = name;
    }

    String getObjectAddress() {
        return super.toString();
    }
}
```

在方法中改变对象的字段值会改变原对象该字段值，因为引用的是同一个对象。

```java
class PassByValueExample {
    public static void main(String[] args) {
        Dog dog = new Dog("A");
        func(dog);
        System.out.println(dog.getName());          // B
    }

    private static void func(Dog dog) {
        dog.setName("B");
    }
}
```



### float 与 double

**Java 不能隐式执行向下转型，因为这会使得精度降低。（不能自动从高精度转变为低精度）**

1.1 字面量属于 double 类型，不能直接将 1.1 直接赋值给 float 变量，因为这是向下转型。

```java
// float f = 1.1;
```

1.1f 字面量才是 float 类型。

```java
float f = 1.1f;
```



### & 和 && 的区别

> &运算符有两种用法：
>
> - 按位与
> - 逻辑与
>
> **&&运算符是短路与运算**

### `==` 和 `equals` 的区别？

> **equals与 == 的最大区别：一个是方法，一个是运算符**
>
> **==**：
>
> - 如果比较的对象是基本类型，则比较数值是否相等
> - 如果比较的对象是封装类型，则比较对象的地址值是否相等
>
> **equals**：用来比较方法两个对象的内容是否相等
>
> **注**：equals 方法不能用于基本数据类型的变量，如果没有对 equals 方法进行重写，则比较的是引用类型的变量所指向的对象的地址。



### String s = "Hello";s = s + " world!"; 这两行代码执行后，原始的 String 对象中的内容到底变了没有？

> 没有。因为String类是不可变类，它的所有对象都是不可变对象。在这段代码中， s 原先指向一个 String 对象，内容是"Hello"，然后我们对 s 进行了“ 操作，那么 s 所指向的那个对象是否发生了改变呢？答案是没有。这时， s 不指向原来那个对象了，而指向了另一个 String 对象，内容为 "Hello world!"，原来那个对象还是存在内存中。只是s这个引用变量不再指向它了

------

著作权归小熊学Java所有 原文链接：https://javaxiaobear.cn/interview/javaBasics/javaSE.html



## 关键字

### final 语法

1. 对于基本类型，final 使数值不变；

2. 当一个**对象的引用**被声明为 `final`，意味着这个引用只能指向初始化时所指向的对象，不能再指向其他对象。这样做的目的是**确保在程序执行过程中，该引用始终指向同一个对象，而不会被重新赋值指向其他对象**。

3. **final声明方法不能被子类重写**。private 方法隐式地被指定为 final，

4. **final类：** 当一个类被声明为 `final` 时，意味着该类不能被继承。这通常是因为该类的设计者认为它已经完整并且不应该有子类来改变其行为。

   ```
   javaCopy codefinal class FinalClass {
       // 类定义
   }
   
   // 下面的代码是非法的，因为无法继承 final 类
   // class SubClass extends FinalClass {
   //     // 类定义
   // }
   ```

所以，`final` 对象代表一个引用只能指向初始化时所指向的对象，而 `final` 类代表不能被继承的类。

### static

**1. 静态变量**

- 静态变量：又称为类变量，也就是说这个变量属于类的，类所有的实例都共享静态变量，可以直接通过类名来访问它。静态变量在内存中只存在一份。

- 实例变量：每创建一个实例就会产生一个实例变量，它与该实例同生共死。

  

**2. 静态方法**

静态方法在类加载的时候就存在了，它不依赖于任何实例。所以静态方法必须有实现，也就是说它不能是抽象方法。

**3. 静态语句块**

静态语句块在类初始化时运行一次。

```java
public class A {
    static {
        System.out.println("123");
    }

    public static void main(String[] args) {
        A a1 = new A();
        A a2 = new A();
    }
}
```



## Object 通用方法

```java
public native int hashCode() # 常用

public boolean equals(Object obj) # 常用

protected native Object clone() throws  # 常用CloneNotSupportedException

public String toString() # 常用

public final native Class<?> getClass()

protected void finalize() throws Throwable {}

public final native void notify()

public final native void notifyAll()

public final native void wait(long timeout) throws InterruptedException

public final void wait(long timeout, int nanos) throws InterruptedException

public final void wait() throws InterruptedException
```

### hashCode()

hashCode() 返回哈希值，而 equals() 是用来判断两个对象是否等价。等价的两个对象散列值一定相同，但是**散列值相同的两个对象不一定等价，这是因为计算哈希值具有随机性**，两个值不同的对象可能计算出相同的哈希值。

注意，对于hashmap的使用，如果**内容相等，但是它们的hashCode()不等；所以，HashSet在添加p1和p2的时候，认为它们不相等。**

**因此，应该两者统一。**

### toString()

默认返回 ToStringExample@4554617c 这种形式，其中 @ 后面的数值为散列码的无符号十六进制表示。



### clone()

默认情况下，`clone()` 方法执行的是浅拷贝。

**浅拷贝**

拷贝对象和原始对象的引用类型引用同一个对象。





 **深拷贝**

拷贝对象和原始对象的引用类型引用不同对象。

```java
public class DeepCloneExample implements Cloneable {

    private int[] arr;

    public DeepCloneExample() {
        arr = new int[10];
        for (int i = 0; i < arr.length; i++) {
            arr[i] = i;
        }
    }

    public void set(int index, int value) {
        arr[index] = value;
    }

    public int get(int index) {
        return arr[index];
    }

    @Override
    protected DeepCloneExample clone() throws CloneNotSupportedException {
        DeepCloneExample result = (DeepCloneExample) super.clone();
        result.arr = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            result.arr[i] = arr[i];
        }
        return result;
    }
}
```

## 继承

### 访问权限

Java 中有三个访问权限修饰符：private、protected 以及 public，如果不加访问修饰符，表示包级可见。

1. **private（私有）**：private修饰的成员（方法、变量等）只能在声明它们的类内部访问，其他任何类都无法直接访问。这提供了最高级别的封装。
2. **protected（受保护）**：protected修饰的成员对于同一个包中的类以及所有子类都是可见的。也就是说，protected成员可以被同一个包中的其他类以及继承了该类的类访问。
3. **public（公开）**：public修饰的成员对于所有类都是可见的，无论是同一个包中的类还是不同包中的类，都可以访问public成员。
4. **默认访问权限（包级可见）**：如果不使用任何修饰符，则成员具有默认的访问权限，也称为包级可见性。默认访问权限使得该成员对于同一个包中的其他类可见，但对于不同包中的类则是不可见的。

## public 、 private 、 protected， 以及不写（默认）时的区别

| 修饰符    | 当前类 | 同包 | 子类 | 其他包 |
| --------- | ------ | ---- | ---- | ------ |
| public    | √      | √    | √    | √      |
| protected | √      | √    | √    | ×      |
| default   | √      | √    | ×    | ×      |
| private   | √      | ×    | ×    | ×      |











### 抽象类与接口

抽象类和接口都是面向对象编程中用于实现多态性和封装的重要概念，它们有些相似但也有着一些区别。

**抽象类（Abstract Class）**：

1. 抽象类是一种不能实例化的类，即不能直接创建抽象类的对象。
2. **抽象类可以包含抽象方法和具体方法。抽象方法是没有实现的方法，而具体方法是有实现的方法。**
3. 子类继承抽象类时，必须实现抽象类中的所有抽象方法，除非子类也是抽象类。
4. **可以有构造方法，用于子类的初始化。**
5. 抽象类可以包含成员变量，方法和构造方法。
6. 使用 `abstract` 关键字定义抽象类。

**接口（Interface）**：

1. 接口是一种完全抽象的类，**它只定义了方法的签名而没有提供方法的实现。**
2. 类可以实现一个或多个接口，并实现接口中定义的所有方法。
3. 接口中的方法默认是 `public` 和 `abstract` 的，可以省略这些修饰符。
4. 接口中不能包含成员变量，除非是 `public static final` 类型的常量。
5. **接口中不能有构造方法。**
6. 使用 `interface` 关键字定义接口。

**区别**：

1. 抽象类可以包含成员变量和具体方法的实现，而接口不能包含成员变量和具体方法的实现。
2. **一个类可以继承一个抽象类，但可以实现多个接口。**
3. 抽象类的目的是为了提供一个公共的接口，同时提供一些默认的实现，而接口的目的是为了定义一个规范，不关心具体的实现。
4. 接口更加灵活，可以帮助避免类之间的紧耦合，而抽象类更适合用于在相似类之间共享代码。

总的来说，如果你需要定义一组方法的规范而不关心具体实现，使用接口；如果你需要提供一些默认的实现，或者需要定义一些共有的成员变量，使用抽象类。



### super

- **访问父类的构造函数：可以使用 super() 函数访问父类的构造函数**，从而委托父类完成一些初始化的工作。应该注意到，子类一定会调用父类的构造函数来完成初始化工作，一般是调用父类的默认构造函数，如果子类需要调用父类其它构造函数，那么就可以使用 super() 函数。
- **访问父类的成员：如果子类重写了父类的某个方法，可以通过使用 super 关键字来引用父类的方法实现。**



### 重写与重载

在Java中，重写（Override）和重载（Overload）是两种不同的概念，它们都涉及到方法的使用和定义。

1. **重写（Override）**：
   - 重写是指**子类定义了一个与父类中具有相同名称、参数列表和返回类型的方法，并且在子类中提供了新的实现**。重写通常用于**实现多态性**，即子类对象可以以自己特有的方式来执行继承自父类的方法。
   - **重写的方法必须具有与被重写的方法相同的方法签名（即方法名、参数列表和返回类型），而且访问修饰符不能更严格，可以更宽松**。
   - 重写是运行时多态的一种表现，也就是说，当调用一个对象的方法时，实际执行的是其所属类中的方法，而不是声明时的类型。

示例：
```java
class Animal {
    public void makeSound() {
        System.out.println("Animal makes a sound");
    }
}

class Dog extends Animal {
    @Override
    public void makeSound() {
        System.out.println("Dog barks");
    }
}
```

2. **重载（Overload）**：
   - 重载是指**在同一个类中，可以定义多个方法，它们具有相同的名称但是参数列表不同（参数类型、参数个数或者参数顺序不同）**。
   - **重载方法之间的区别是它们的参数列表，返回类型可以不同，但不能仅仅依靠返回类型的不同来进行重载。**
   - 在调用重载方法时，编译器会根据提供的参数类型和数量来确定调用哪个重载方法。

示例：
```java
class Calculator {
    public int add(int a, int b) {
        return a + b;
    }

    public double add(double a, double b) {
        return a + b;
    }
}
```

总的来说，重写是针对继承关系中的父类和子类的方法，而重载是在同一个类中针对方法的参数列表的多态性。



## 反射

反射这一部分挺难1的，建议后面单开一文详细说明。

**Java反射机制是指在运行时检查类、方法、字段等信息，并且可以在运行时动态地创建对象、调用方法、获取和设置字段值等的能力。简单来说，反射机制允许程序在运行时获取和操作类的信息，而不需要事先知道类的具体类型。**



每个类都有一个 **Class** 对象，包含了与类有关的信息。当编译一个新类时，会产生一个同名的 .class 文件，该文件内容保存着 Class 对象。原理如图
![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/e8da9232c588c9b3f04ef0372addef93/c2b064c181acc94720b7cd57611d0388.png)

**Class类对象的获取**

在类加载的时候，jvm会创建一个class对象

class对象是可以说是反射中最常用的，获取class对象的方式的主要有三种

- 根据类名：类名.class
- 根据对象：对象.getClass()
- 根据全限定类名：Class.forName(全限定类名)

------

**Java 反射主要提供以下功能：**

- 在运行时判断任意一个对象所属的类；
- 在运行时构造任意一个类的对象；
- 在运行时判断任意一个类所具有的成员变量和方法（通过反射甚至可以调用private方法）；
- 在运行时调用任意一个对象的方法
- **反射最重要的用途就是开发各种通用框架。**很多框架（比如 Spring）都是**配置化的（比如通过 XML 文件配置 Bean），为了保证框架的通用性，它们可能需要根据配置文件加载不同的对象或类**，调用不同的方法，这个时候就必须用到反射，运行时动态加载需要加载的对象。

**反射的优点：**

- **可扩展性** ：应用程序可以利用全限定名创建可扩展对象的实例，来使用来自外部的用户自定义类。
- **类浏览器和可视化开发环境** ：一个类浏览器需要可以枚举类的成员。可视化开发环境（如 IDE）可以从利用反射中可用的类型信息中受益，以帮助程序员编写正确的代码。
- **调试器和测试工具** ： 调试器需要能够检查一个类里的私有成员。测试工具可以利用反射来自动地调用类里定义的可被发现的 API 定义，以确保一组测试中有较高的代码覆盖率。





## 泛型

Java中的泛型不支持基本数据类型，只能使用对象类型。因此，你不能将 int 作为 HashSet 的泛型参数。正确的做法是使用 Integer 类型作为泛型参数。例如：

```
        HashSet<int> set = new HashSet<>();错了
        HashSet<Integer> set = new HashSet<>();只能
```

```java
public class Box<T> {
    // T stands for "Type"
    private T t;
    public void set(T t) { this.t = t; }
    public T get() { return t; }
}
```

## 注解

Java 注解是附加在代码中的一些元信息，用于一些工具在编译、运行时进行解析和使用，**起到说明、配置的功能**。注解不会也不能影响代码的实际逻辑，仅仅起到辅助性的作用。

**Java的注解原理基于语法定义和反射机制实现**，通过编译器和运行时环境对注解进行解析和处理，为程序提供了更灵活、更方便的元数据管理方式。





# 安装



## jdk和jre



Java 中的 JDK 和 JRE的区别是**：JDK是 Java 语言的软件开发工具包**，主要用于移动设备、嵌入式设备上的java应用程序。JDK是整个java开发的核心，**它包含了JAVA的运行环境和JAVA工具**。**JRE（Java Runtime Environment，简称JRE）是一个软件**，由太阳微系统所研发，JRE可以让计算机系统运行**Java应用程序**。





## 文件名与类名

在Java中，**如果一个类是`public`的，并且它位于一个名为`ClassName.java`的文件中，那么这个类的名称必须与文件名完全相同。这是Java编译器的要求，以确保代码的结构清晰和易于理解。**

- 3.一个Java文件中只能有一个public类；
- 4.如果文件中不止一个类，文件名必须与public类名一致；

- 5.如果文件中不止一个类，而且没有public类，文件名可随意。





## 运行 javac&&java

```
class hello {
    public static void main(String[] args) {
        System.out.println("hello");
    }
    
}
```

**如果一个Java文件中没有`public`类，但包含了`main`方法，你仍然可以通过命令行来执行这个`main`方法，前提是该类的`main`方法是`public`的。但是，你不能直接使用`java`命令后跟类名来执行，而是需要使用`java`命令后跟着完整的类路径名。**

假设你有一个名为 `MyClass.java` 的文件，其中包含了一个非 `public` 的类 `MyClass`，并且该类包含了一个 `public static void main(String[] args)` 方法。你可以使用以下步骤来执行该 `main` 方法：

1. 首先，编译 `MyClass.java` 文件，使用以下命令：

   ```
   javac MyClass.java
   ```

   这将生成一个名为 `MyClass.class` 的字节码文件。

2. 接着，在命令行中，使用以下命令来执行 `main` 方法：

   ```
   java -cp . MyClass   # 注意，千万不能加上.class作为完整文件名
   ```

   这个命令中的 `-cp .` 选项表示将当前目录添加到类路径中，而 `MyClass` 是你要执行的类的名称。

这样就可以执行 `MyClass` 类中的 `main` 方法了。









# 其他



## 为什么浮点数运算的时候会有精度丢失的风险？

这个和计算机保存浮点数的机制有很大关系。我们知道计算机是二进制的，而且**计算机在表示一个数字时，宽度是有限的，无限循环的小数存储在计算机时，只能被截断，所以就会导致小数精度发生损失的情况**。这也就是解释了为什么浮点数没有办法用二进制精确表示。

`BigDecimal` 可以实现对浮点数的运算，不会造成精度丢失

`BigInteger` 内部使用 `int[]` 数组来存储任意大小的整形数据。

**原因是BigDecimal采用了long intCompact和int scale来表示数值，而不是浮点型的科学计数法。BigDecimal的原理很简单，就是将小数扩大N倍，转成整数后再进行计算，同时结合指数，得出没有精度损失的结果。**





## java unsafe类

**`Unsafe` 是位于 `sun.misc` 包下的一个类，主要提供一些用于执行低级别、不安全操作的方法，如直接访问系统内存资源、自主管理内存资源等，这些方法在提升 Java 运行效率、增强 Java 语言底层资源操作能力方面起到了很大的作用。**

**如若想使用 `Unsafe` 这个类的话，应该如何获取其实例呢？**

这里介绍两个可行的方案。

1、利用**反射**获得 Unsafe 类中已经实例化完成的单例对象 `theUnsafe` 。

`Unsafe` 类实现功能可以被分为下面 8 类：

1. 内存操作
2. 内存屏障
3. 对象操作
4. 数据操作
5. CAS 操作
6. 线程调度
7. Class 操作
8. 系统信息
