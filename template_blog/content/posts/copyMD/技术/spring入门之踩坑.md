---
title: spring入门之踩坑
top: false
cover: false
toc: true
mathjax: true
date: 2023-05-2 15:27:31
password:
summary:
tags:
- web api
- cgi
categories:
- 综合
---



# 前置相关知识

## 语言特性相关
### 泛型
你可以写一个泛型方法，**该方法在调用时可以接收不同类型的参数**。根据传递给泛型方法的参数类型，编译器适当地处理每一个方法调用。

下面是定义泛型方法的规则：

所有泛型方法声明都有一个类型参数声明部分（由尖括号分隔），该类型参数声明部分在方法返回类型之前（在下面例子中的 <E>）。

```
public class GenericMethodTest
{
   // 泛型方法 printArray                         
   public static < E > void printArray( E[] inputArray )
   {
      // 输出数组元素            
         for ( E element : inputArray ){        
            System.out.printf( "%s ", element );
         }
         System.out.println();
    }
 
    public static void main( String args[] )
    {
        // 创建不同类型数组： Integer, Double 和 Character
        Integer[] intArray = { 1, 2, 3, 4, 5 };
        Double[] doubleArray = { 1.1, 2.2, 3.3, 4.4 };
        Character[] charArray = { 'H', 'E', 'L', 'L', 'O' };
 
        System.out.println( "整型数组元素为:" );
        printArray( intArray  ); // 传递一个整型数组
 
        System.out.println( "\n双精度型数组元素为:" );
        printArray( doubleArray ); // 传递一个双精度型数组
 
        System.out.println( "\n字符型数组元素为:" );
        printArray( charArray ); // 传递一个字符型数组
    } 
}

```





## 框架结构相关

### [SSM框架中Dao层，Mapper层，controller层，service层，model层，entity层都有什么作用](https://www.cnblogs.com/SH-xuliang/p/10775630.html)

SSM是**sping+springMVC+mybatis**集成的框架。

MVC即model view controller。

**model层=entity层**。存放我们的**实体类**，与数据库中的属性值基本保持一致。

**service层。存放业务逻辑处理**，也是一些关于数据库处理的操作，但不是直接和数据库打交道，他有接口还有接口的实现方法，在接口的实现方法中需要导入mapper层，mapper层是直接跟数据库打交道的，他也是个接口，只有方法名字，具体实现在mapper.xml文件里，service是供我们使用的方法。

**mapper层=dao层**，现在用mybatis逆向工程生成的mapper层，其实就是dao层。**对数据库进行数据持久化操作**，他的方法语句是直接针对数据库操作的，而service层是针对我们controller，也就是针对我们使用者。service的impl是把mapper和service进行整合的文件。

（多说一句，数据持久化操作就是指，把数据放到持久化的介质中，同时提供增删改查操作，比如数据通过hibernate插入到数据库中。）

**controller层。控制器**，导入service层，因为service中的方法是我们使用到的，controller通过接收前端传过来的参数进行业务操作，在返回一个指定的路径或者数据表





### 关于DTO(Data Transfer Object)
目标是在不同层之间“传输”数据。（例如前后端）
对于需要传输的数据，最好是将其封装到对象中，以便于发送和接收。
DTO类型的对象, 不应该掺杂任何业务逻辑; 只包含获取和设置属性的方法, 以及用于序列化或反序列化的解析器。

**本质上来说，就是一个前后端之间用来传递的json对象。和entity里面的对象比较像，但是并不完全一样。可以部分的替代entity，用来减少一下非必须得传递字段或者增加一些特殊的效验字段。**


### 关于ORM

**简单说，ORM 就是通过实例对象的语法，完成关系型数据库的操作的技术，是"对象-关系映射"（Object/Relational Mapping） 的缩写。**

ORM 把数据库映射成对象。

- 数据库的表（table） --> 类（class）
- 记录（record，行数据）--> 对象（object）
- 字段（field）--> 对象的属性（attribute）

ORM 使用对象，封装了数据库操作，因此可以不碰 SQL 语言。开发者只使用面向对象编程，与数据对象直接交互，不用关心底层数据库。

### 关于依赖注入
依赖注入（Dependency Injection，简称DI）是一种设计模式，用于管理对象之间的依赖关系。**在软件开发中，一个对象（被称为依赖）需要访问另一个对象（被称为依赖项）时，依赖注入通过外部的方式将依赖项传递给依赖，而不是由依赖自己创建或查找依赖项。**

在Spring框架中，Bean是Spring容器中的对象实例。它们**由Spring容器负责创建、组装和管理**。依赖注入是Spring框架的核心机制之一，它使得在创建Bean对象时，可以自动地将其所需的依赖项注入到对象中，而不需要手动创建或查找依赖项。

通过依赖注入，Bean对象可以通过声明它所需的依赖关系，而无需关心如何获取这些依赖项。**Spring容器负责在需要时查找并注入这些依赖项，从而实现对象之间的解耦和灵活性。**











# 坑



## dependency的更新问题

修改dependency后修改是需要时间的，idea需要时间去重新配置。



### 不要乱加依赖

有时候不是代码不行，而是依赖有问题

- 依赖版本错误，导致运行不了
- 依赖不是越多越好，有时候因为加了一些冲突的依赖，反而会导致运行不了。





# 工程上的考量

## 安全性

密码要尽量用md5等不可逆算法进行加密。不要暴露

## 通用性

不要重复造轮子。对于常见的，大量的操作，有规律可以总结的模块，要尽量写成一个通用的接口模块进行封装。

例如：DTO与Entity的转化。

## 规范性

- 返回的json要规范常用的字段
- 要尽量使用常量的变量名作为替代一些无意义的数值
- 错误要统一进行拦截
- 接口规范要统一
- 语法编码要规范



# ref

[good demo](https://gitee.com/liuge1988/spring-boot-demo#https://gitee.com/link?target=https%3A%2F%2Fwww.cnblogs.com%2Fxifengxiaoma%2Fp%2F11019240.html)

