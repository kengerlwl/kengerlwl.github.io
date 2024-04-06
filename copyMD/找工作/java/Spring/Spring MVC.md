---
title: Spring MVC
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
