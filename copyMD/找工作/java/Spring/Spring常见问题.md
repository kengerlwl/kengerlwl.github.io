---
title: Spring常见问题
top: false
cover: false
toc: true
mathjax: true
draft: true
date: 2024-04-05 15:27:31
password:
summary:
tags:
- java
- Spring
categories:
- find JOB
---

# 基础概念



## spring的底层

- 底层都依赖于它的两个核心特性，也就是**(IOC)依赖注入**（dependency injection，DI）和**面向切面编程**（aspectorientedprogramming，AOP）。
  - 实现机制：**工厂模式+反射机制**

- 依赖反射实现容器的创建管理





## Spring中用到了哪些设计模式？

> - **工厂模式**：BeanFactory就是简单工厂模式的体现，用来创建对象的实例
> - **单例模式**：**Bean默认为单例模式**
> - **代理模式**：Spring的**AOP功能用到了JDK的动态代理和CGLIB字节码生成技术**
> - **模板方法**：用来解决代码重复的问题。比如. RestTemplate, JmsTemplate, JpaTemplate
> - **观察者模式**：定义对象键一种一对多的依赖关系，当一个对象的状态发生改变时，所有依赖于它的对象都会得到通知被制动更新，如Spring中listener的实现–ApplicationListener

## Spring 如何设计容器的，BeanFactory和ApplicationContext的关系详解

> Spring 作者 Rod Johnson 设计了两个接口用以表示容器。
>
> - ```
>   BeanFactory
>   ```
>
>   - BeanFactory 简单粗暴，**可以理解为就是个 HashMap**，Key 是 BeanName，Value 是 Bean 实例。通常只提供注册（put），获取（get）这两个功能。我们可以称之为 “低级容器”。
>
> - ```
>   ApplicationContext 派生自BeanFactory， 继承MessageSource，
>   ```
>
>   - ApplicationContext 可以称之为 “高级容器”。因为他比 BeanFactory 多了更多的功能。他继承了多个接口。因此具备了更多的功能。例如资源的获取，支持多种消息（例如 JSP tag 的支持），对BeanFactory 多了工具级别的支持等待。所以你看他的名字，已经不是 BeanFactory 之类的工厂了，而是 “应用上下文”， 代表着整个大容器的所有功能。该接口定义了一个 refresh 方法，此方法是所有阅读 Spring 源码的人的最熟悉的方法，用于刷新整个容器，即重新加载/刷新所有的bean



## 依赖注入有几种实现方式？

> 依赖注入是时下最流行的IOC实现方式，依赖注入分为接口注入（Interface Injection），Setter方法注入（Setter Injection）和构造器注入（Constructor Injection）三种方式。其中接口注入由于在灵活性和易用性比较差，现在从Spring4开始已被废弃。
>
> - **构造器依赖注入**：构造器依赖注入通过容器触发一个类的构造器来实现的，该类有一系列参数，每个参数代表一个对其他类的依赖。
> - **Setter方法注入**：Setter方法注入是**容器通过调用无参构造器或无参static工厂 方法实例化bean之后，调用该bean的setter方法，即实现了基于setter的依赖注入。**





## Spring支持的几种bean的作用域

| 作用域         | 描述                                                         |
| -------------- | ------------------------------------------------------------ |
| **singleton**  | **（默认）将单个 bean 定义范围限定为每个 Spring IoC 容器的单个对象实例。** |
| **prototype**  | **一个bean的定义可以有多个实例**                             |
| request        | 每次http请求都会创建一个bean，该作用域仅在基于web的Spring ApplicationContext情形下有效 |
| session        | 在一个HTTP Session中，一个bean定义对应一个实例。该作用域仅在基于web的Spring ApplicationContext情形下有效 |
| global-session | 在一个全局的HTTP Session中，一个bean定义对应一个实例。该作用域仅在基于web的Spring ApplicationContext情形下有效 |
| application    | 将单个 bean 定义范围限定为`ServletContext`. 仅在 web-aware Spring 的上下文中有效`ApplicationContext` |
| webSocket      | 将单个 bean 定义范围限定为`WebSocket`. 仅在 web-aware Spring 的上下文中有效`ApplicationContext` |

 **缺省的Spring bean 的作用域是Singleton**。使用 prototype 作用域需要慎重的思考，因为频繁创建和销毁 bean 会带来很大的性能开销

## Spring框架中的单例bean是线程安全的吗？

> 不是。spring 中的 bean 默认是单例模式，spring 框架并没有对单例 bean 进行多线程的封装处理
>
> **说到底，对于单例模式还是要看有没有状态信息，如果实例有状态那就不安全了。**



## Spring如何处理线程并发问题？

> 1. 在一般情况下，只有无状态的Bean才可以在多线程环境下共享，在Spring中，绝大部分Bean都可以声明为singleton作用域，因为Spring对一些Bean中非线程安全状态采用**ThreadLocal**进行处理，解决线程安全问题
> 2. ThreadLocal和线程同步机制都是为了解决多线程中相同变量的访问冲突问题。**同步机制采用了“时间换空间”的方式，仅提供一份变量，不同的线程在访问前需要获取锁，没获得锁的线程则需要排队。而ThreadLocal采用了“空间换时间”的方式。**
> 3. **ThreadLocal会为每一个线程提供一个独立的变量副本，从而隔离了多个线程对数据的访问冲突**。因为每一个线程都拥有自己的变量副本，从而也就没有必要对该变量进行同步了。ThreadLocal提供了线程安全的共享对象，在编写多线程代码时，可以把不安全的变量封装进ThreadLocal。



# `ThreadLocal`详解

**它可以在一个线程中传递同一个对象。（方便同一个线程中的不同上下文的调用）**

也可以使一个实例，在不同的线程中拥有不同的变量。ThreadLocal 实际上是将变量绑定到当前线程上，并不会影响到其他线程。也就是说，同一个 ThreadLocal 变量在不同线程中是独立的，不会相互影响。

## Spring Bean的生命周期

![image-20210726145441431](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/c4045af266103bf0f40c3fa6989e6e59/9013ba7699bd049343060c879ecbc5e8.png)



1. Spring对Bean进行实例化
2. Spring将值和bean的引用注入到Bean对应的属性中
3. 实现各种spring的生命周期函数，直到bean准备就绪
4. 当bean已经准备就绪，可以被应用程序使用了，它们将一直驻留在应用上下文中，直到该应用上下文被销毁；
5. 如果bean实现了DisposableBean接口，Spring将调用它的destroy()接口方法。同样，如果bean使用destroy-method声明了销毁方法，该方法也会被调用。



## 自动装配

自动装配是 Spring 框架中一种便捷的机制，**用于将一个 Bean 的依赖自动注入到另一个 Bean 中。简单来说，自动装配就是让 Spring 容器在创建 Bean 时，自动识别并满足 Bean 所需的依赖关系。**

```
	构造函数注入
	@Autowired
    public MyService(MyRepository repository) {
        this.repository = repository;
    }
    属性注入
    @Autowired
    private MyRepository repository;
    
    Setter 方法注入
    @Autowired
    public void setRepository(MyRepository repository) {
        this.repository = repository;
    }
    
```

## 使用@Autowired注解自动装配的过程是怎样的？

> 使用@Autowired注解来自动装配指定的bean。在使用@Autowired注解之前需要在Spring配置文件进行配置
>
> 
>
> ```xml
> <context:annotation-config />
> ```
>
> 1. 在启动spring IOC时，容器自动装载了一个AutowiredAnnotationBeanPostProcessor后置处理器，当容器扫描到@Autowied、@Resource或@Inject时，就会在IOC容器自动查找需要的bean，并装配给该对象的属性
> 2. 在使用@Autowired时，首先在容器中查询对应类型的bean： 
>    - **如果查询结果刚好为一个，就将该bean装配给@Autowired指定的数据；**
>    - **如果查询的结果不止一个，那么@Autowired会根据名称来查找；**
>    - 如果上述查找的结果为空，那么会抛出异常。解决方法时，使用required=false。
>    - 当您创建多个相同类型的 bean 并希望仅使用属性装配其中一个 bean 时，您可以使用@Qualifier注解和 @Autowired 通过指定应该装配哪个确切的 bean 来消除歧义



## @Autowired和@Resource之间的区别

> @Autowired和@Resource可用于：构造函数、成员变量、Setter方法
>
> @Autowired和@Resource之间的区：
>
> - @Autowired默认是按照**类型**装配注入的，默认情况下它要求依赖对象必须存在（可以设置它required属性为false）。
> - @Resource默认是按照**名称**来装配注入的，只有当找不到与名称匹配的bean才会按照类型来装配注入







## @Bean 和@Component区别

`@Bean` 注解用于手动配置和管理 Bean，通常与 `@Configuration` 注解一起使用；

而 `@Component` 注解用于标识通用的 Spring 组件，并由 Spring 自动扫描和管理。

```java
// Product.java
public class Product {
    private String name;
    private double price;

    // 省略构造函数、getter 和 setter 方法
}

// ProductService.java
@Component
public class ProductService {

    @Bean // 将product也声明为了一个bean。注入IOC容器
    public Product createProduct() {
        // 创建一个商品对象
        Product product = new Product();
        product.setName("iPhone");
        product.setPrice(999.99);
        return product;
    }
}

```





## spring bean的循环依赖问题

当我们注入一个对象A时，需要注入对象A中标记了某些注解的属性，这些属性也就是对象A的依赖，把对象A中的依赖都初始化完成，对象A才算是创建成功。那么，如果对象A中有个属性是对象B，而且对象B中有个属性是对象A，那么对象A和对象B就算是循环依赖，**如果不加处理，就会出现：创建对象A-->处理A的依赖B-->创建对象B-->处理B的对象A-->创建对象A-->处理A的依赖B-->创建对象B......这样无限的循环下去。**

Spring处理循环依赖的基本思路是这样的：

虽说要初始化一个Bean，必须要注入Bean里的依赖，才算初始化成功，但并不要求此时依赖的依赖也都注入成功，只要依赖对象的构造方法执行完了，这个依赖对象就算存在了，注入就算成功了，至于依赖的依赖，以后再初始化也来得及（参考Java的内存模型）。

因此，我们初始化一个Bean时，**先调用Bean的构造方法，这个对象就在内存中存在了（对象里面的依赖还没有被注入），然后把这个对象保存下来，当循环依赖产生时，直接拿到之前保存的对象，于是循环依赖就被终止了，依赖注入也就顺利完成了。**

**解决办法**

- **使用 `@Lazy` 注解**：在 Spring 4.3 版本后，可以使用 `@Lazy` 注解来延迟初始化 Bean，从而避免循环依赖问题。

- Spring文档建议的一种方式是**使用setter注入。当依赖最终被使用时才进行注入。**

- 使用@PostConstruct






## Spring AOP实现日志

1. 创建一个切面类，用于定义日志记录的逻辑：

```
javaCopy codeimport org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class LoggingAspect {

    @Before("execution(* com.example.service.*.*(..))")
    public void logBefore(JoinPoint joinPoint) {
        System.out.println("Before method: " + joinPoint.getSignature().getName());
    }

    @After("execution(* com.example.service.*.*(..))")
    public void logAfter(JoinPoint joinPoint) {
        System.out.println("After method: " + joinPoint.getSignature().getName());
    }
}
```

在上述代码中，我们定义了一个切面类 `LoggingAspect`，并在其中定义了两个通知方法：

- `logBefore()` 方法用于在目标方法执行之前记录日志。
- `logAfter()` 方法用于在目标方法执行之后记录日志。

这里我们使用了 `@Before` 和 `@After` 注解来指定通知的类型，并使用 `execution()` 切入点表达式来匹配所有 `com.example.service` 包下的方法。



## Spring只支持方法级别的连接点？

> 因为Spring基于动态代理，所以Spring只支持方法连接点



## Spring AOP切面通知有哪些类型？

> 1. 前置通知（Before）：在目标方法被调用之前调用通知功能；
> 2. 后置通知（After）：在目标方法完成之后调用通知，此时不会关心方法的输出是什么；
> 3. 返回通知（After-returning ）：在目标方法成功执行之后调用通知；
> 4. 异常通知（After-throwing）：在目标方法抛出异常后调用通知；
> 5. 环绕通知（Around）：通知包裹了被通知的方法，在被通知的方法调用之前和调用之后执行自定义的行为。





## 动态代理代理和静态代理

1. **静态代理**：
   - 静态代理是在编译期间就已经确定代理类和被代理类的关系的代理方式。
   - 静态代理需要为每个被代理的类编写一个代理类，代理类通常在编译期间就已经确定。
   - 静态代理实现简单，但扩展性较差，如果需要代理的类很多，会导致代理类的数量增加。
2. **动态代理**：
   - 动态代理是在运行时动态生成代理类的代理方式。
   - 动态代理不需要为每个被代理的类编写单独的代理类，而是通过反射和代理对象的接口动态生成代理类。
   - 动态代理实现相对复杂，但具有较好的扩展性，能够在运行时动态生成代理类，适用于不确定代理类的情况。



# Spring事务的实现方式和实现原理

> **Spring事务的本质其实就是数据库对事务的支持**，没有数据库的事务支持，spring是无法提供事务功能的。真正的数据库层的事务提交和回滚是通过binlog或者redo log实现的。









