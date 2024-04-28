---
title: Spring MVC and Boot
top: false
cover: false
toc: true
mathjax: true
hidden: true
date: 2024-04-06 15:27:31
password:
summary:
tags:
- java
- spring
categories:
- find JOB

---

# Spring MVC



## 什么是Spring MVC?

> Spring MVC是一个基于Java的实现了MVC设计模式的请求驱动类型的轻量级Web框架，通过把模型-视图-控制器分离，将web层进行职责解耦，把复杂的web应用分成逻辑清晰的几部分，简化开发，减少出错，方便组内开发人员之间的配合。









## Spring MVC 中常用的注解：

1. **控制器相关注解**：
   - `@Controller`: 用于标识一个类作为 Spring MVC 的控制器组件。
   - `@RequestMapping`: 用于映射请求 URL 到处理方法，并可以指定请求方法、请求参数等条件。
   - `@GetMapping`、`@PostMapping`、`@PutMapping`、`@DeleteMapping`: 用于分别标识处理 GET、POST、PUT、DELETE 请求的方法。
2. **参数绑定相关注解**：
   - `@RequestParam`: 用于从请求中获取参数值，并绑定到方法的参数上。
   - `@PathVariable`: 用于将 URL 中的模板变量绑定到方法的参数上。
   - `@ModelAttribute`: 用于将请求参数绑定到一个模型对象上，通常用于表单提交时的数据绑定。
3. **视图相关注解**：
   - `@ResponseBody`: 用于将方法返回的对象作为 HTTP 响应体返回给客户端，通常用于返回 JSON 或者 XML 格式的数据。
   - `@RestController`: 是 `@Controller` 和 `@ResponseBody` 的组合注解，用于标识 RESTful 风格的控制器。
   - `@RequestMapping`（类级别）: 用于指定该控制器下所有请求的公共 URL 前缀。
4. **数据校验相关注解**：
   - `@Valid`: 用于在方法参数上标注需要校验的对象，触发数据校验。
   - `@Validated`: 与 `@Valid` 类似，用于触发数据校验，但支持分组校验等功能。

## MVC是什么？MVC设计模式的好处有哪些？

> - mvc是一种设计模式（设计模式就是日常开发中编写代码的一种好的方法和经验的总结）。**模型（model）-视图（view）-控制器（controller），三层架构的设计模式。用于实现前端页面的展现与后端业务数据处理的分离。**
> - 好处： 
>   - 分层设计，实现了业务系统各个组件之间的解耦，有利于业务系统的可扩展性，可维护性。
>   - 有利于系统的并行开发，提升开发效率。

## 注解的原理是什么（反射）

> **注解本质是一个继承了Annotation的特殊接口**，其具体实现类是Java运行时生成的动态代理类。我们通过反射获取注解时，**返回的是Java运行时生成的动态代理对象**。通过代理对象调用自定义注解的方法，**会最终调用AnnotationInvocationHandler的invoke方法**。该方法会从memberValues这个Map中索引出对应的值。而memberValues的来源是Java常量池。





# Spring Boot

## 什么是Spring Boot？

> - 它使用**“习惯优于配置”**（项目中存在大量的配置，此外还内置了一个习惯性的配置，让你无需手动配置）的理念让你的项目快速运行起来。
> - Spring Boot整合了所有框架
> - **简化Spring应用开发的一个框架**

## Spring Boot核心注解是哪个，由哪几个组成呢？

> **启动类注解`@SpringBootApplication = @Configuration + @EnableAutoConfiguration（自动配置） + @ComponentScan（自动扫描注册组件）`**
>
> - **@Configuration：标明该类使用Spring基于Java的配置**
> - **@EnableAutoConfiguration：启动自动配置功能。**简单概括一下就是，借助@Import的支持，**将所有符合自动配置条件的bean定义加载到IoC容器**
> - **@ComponentScan：启用组件扫描，这样你写的Web控制器类和其他组件才能被自动发现并注册为Spring应用程序上下文里的Bean。**



## SpringBoot事务的使用

> SpringBoot的事务很简单，首先使用注解**EnableTransactionManagement开启事务之后，然后在Service方法上添加注解Transactional便可。**

## Spring Boot 中如何解决跨域问题



```java
@Configuration
public class ResourcesConfig implements WebMvcConfigurer
{
    /**
     * 跨域配置
     */
    @Bean
    public CorsFilter corsFilter()
    {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowCredentials(true);
        // 设置访问源地址
        config.addAllowedOrigin("*");
        // 设置访问源请求头
        config.addAllowedHeader("*");
        // 设置访问源请求方法
        config.addAllowedMethod("*");
        // 对接口配置跨域设置
        source.registerCorsConfiguration("/**", config);
        return new CorsFilter(source);
    }
}
```

说到底，本质是先对Options的请求进行预处理实现跨域请求。



## spring boot启动流程

1. **加载启动类**：Spring Boot 应用程序的入口是一个主启动类，通常带有 `@SpringBootApplication` 注解。在启动过程中，首先会加载这个主启动类。
2. **创建 Spring 应用程序上下文**：Spring Boot 使用 Spring 应用程序上下文（ApplicationContext）来管理应用程序中的对象和组件。在启动过程中，Spring Boot 会创建一个根应用程序上下文。
3. **自动配置**：Spring Boot 会根据应用程序的类路径和配置文件自动配置各种功能，例如数据源、Web 容器、安全等。这个过程是通过自动配置机制来实现的，Spring Boot 会根据一定的规则自动配置应用程序的各种组件。
4. **加载外部配置**：Spring Boot 允许您在外部配置文件（如 application.properties 或 application.yml）中指定应用程序的配置信息。在启动过程中，Spring Boot 会加载这些外部配置文件，并将配置信息加载到应用程序上下文中。
5. **启动内嵌的 Web 服务器**：如果应用程序是一个 Web 应用程序，Spring Boot 会在启动过程中启动一个内嵌的 Web 服务器（如 Tomcat、Jetty 或 Undertow），并将应用程序部署到 Web 服务器中。
6. **扫描并加载 Bean**：Spring Boot 会扫描应用程序中的所有类，识别标有特定注解（如 `@Component`、`@Controller`、`@Service` 等）的类，并将这些类注册为 Spring Bean。
7. **运行应用程序**：一旦所有的配置都加载完成，并且应用程序上下文已经准备好，Spring Boot 就会开始运行应用程序。这包括处理 HTTP 请求（如果是 Web 应用程序）、执行业务逻辑等。
8. **关闭应用程序上下文**：在应用程序关闭时，Spring Boot 会关闭应用程序上下文，释放资源，并执行一些清理操作。
