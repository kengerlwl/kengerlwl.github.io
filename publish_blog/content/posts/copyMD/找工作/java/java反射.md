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







# 反射与注解

注解：`@Override`这样的就是注解，注解本身并不会给类或者方法加入什么新的功能。**注解仅仅只是一个标识，真正逻辑work的是反射。**

**真正给注解实现新的功能的，是反射。通过反射，可以动态获取到目标对象的类的，方法的变量的属性。进而可以判断这个类，方法，变量有没有用到某个注解。进而实现代理调用，执行。**



[不懂注解？那就自己写一个，安排的明明白白_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1Py4y1Y77P/?spm_id_from=..top_right_bar_window_history.content.click)

## 注解实现

```
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME) // 用于指定注解的保留策略，即注解在何时有效，比如编译后可以被反射获取到
@Target(ElementType.METHOD)  // 作用域，作用于函数还是变量还是类
public @interface MyAnnotation {
    String value();
}

```







## spring的反射与注解



### IOC



Spring框架中的反射通常在应用程序启动时工作**。当Spring容器启动时，它会扫描应用程序中的类和配置，然后根据配置信息实例化和管理相应的对象。**在这个过程中，Spring可能会使用Java的反射机制来动态地创建对象、调用方法以及设置属性。这种动态性使得Spring框架能够在不直接依赖于类的具体实现的情况下，根据配置信息创建和管理对象，从而实现了松耦合和灵活性。



假设我们有一个名为`UserService`的服务类，我们希望Spring能够管理它，并在需要时注入到其他类中。首先，我们需要**将该类标记为Spring管理的组件，通常使用`@Component`注解来实现：**

注意：

**因此，无论是 `@Component` 还是 `@Service` 注解，它们在实际的反射执行过程中没有任何区别，都可以被Spring框架扫描到并注册为Bean。区别仅在于语义上的意图和约定，以及在编码规范和可读性上的区别。！！！**

```
javaCopy codeimport org.springframework.stereotype.Component;

@Component
public class UserService {
    // 类的具体实现...
}
```

在应用程序启动时，Spring框架会扫描类路径以及包名**，寻找标记有`@Component`注解的类，并将它们实例化为bean并加入到Spring容器中**。在这个过程中，Spring可能会使用反射机制来创建类的实例。

另外，假设我们有一个名为`UserController`的控制器类，它需要依赖于`UserService`。我们可以使用构造函数注入的方式告诉Spring容器，**当创建`UserController`实例时，需要注入`UserService`实例**：

```
javaCopy codeimport org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;

@Controller
public class UserController {
    private final UserService userService;

    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // 控制器的其他方法...
}
```



### AOP

假设我们有一个需求，希望在执行某个方法之前和之后记录日志。我们可以通过定义一个切面来实现这个需求：

```
javaCopy codeimport org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class LoggingAspect {

    @Pointcut("execution(* com.example.service.*.*(..))")
    private void serviceMethods() {}

    @Before("serviceMethods()")
    public void logBefore() {
        System.out.println("Before executing service method");
    }

    @AfterReturning("serviceMethods()")
    public void logAfter() {
        System.out.println("After executing service method");
    }
}
```

下面是Spring AOP使用反射的基本原理：

1. **创建代理对象**：当Spring容器启动时，它会扫描定义的切面，并为匹配切点的bean创建代理对象。Spring AOP通常使用Java动态代理实现代理对象。通过`java.lang.reflect.Proxy`类的`newProxyInstance()`方法创建代理对象。这个代理对象实现了目标类所实现的所有接口，并且可以拦截接口方法的调用。
2. **拦截方法调用**：代理对象拦截匹配切点的方法调用。当某个被代理的方法被调用时，代理对象会触发`InvocationHandler`接口中的`invoke()`方法。
3. **调用通知方法**：在`invoke()`方法中，Spring使用反射API来定位并调用与切面匹配的通知方法。这涉及到解析切面中定义的切点表达式，并定位匹配的通知方法。
4. **执行目标方法**：在通知方法调用之前或之后，代理对象会调用目标方法。它使用反射API定位目标方法，并调用它。







# ref

[Spring 中的反射与反射的原理 - 掘金](https://juejin.cn/post/6844904148316471310)







