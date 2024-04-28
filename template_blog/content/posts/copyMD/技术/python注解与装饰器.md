---
title: python注解与装饰器
top: false
cover: false
toc: true
mathjax: true
date: 2023-08-22 15:27:31
password:
summary:
tags:
- 线程安全
- 消息队列
categories:
- 技术
---



# 背景

python想要使用注解，来实现一些方便解耦合的功能。

**例如对某个flask的路由函数加入token验证功能。但是又不是针对所有的函数都加入。**





# demo

装饰器是 Python 中一种强大的语法特性，用于修改或扩展函数或类的行为。它们是一种函数，可以接受另一个函数（或类）作为参数，并返回一个新的函数（或类）。装饰器在代码中以 `@decorator_name` 的形式应用于目标函数或方法，以实现在目标函数执行前后添加额外的逻辑。

以下是装饰器的基本使用示例：

```
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        result = func(*args, **kwargs)  # 调用原始函数并传递参数
        print("Something is happening after the function is called.")
        return result
    return wrapper

@my_decorator
def greet(name):
    print("somthing is happening in greet function")
    return f"Hello, {name}!"

greeting = greet("Alice")
print(greeting)

```

在这个示例中，`my_decorator` 是一个装饰器函数，它接受一个函数 `func` 作为参数。它定义了一个内部函数 `wrapper`，在调用目标函数 `func` 前后添加了额外的逻辑。然后，我们将 `@my_decorator` 应用于 `say_hello` 函数，这等效于执行 `say_hello = my_decorator(say_hello)`，从而将 `say_hello` 函数传递给 `my_decorator` 并重新赋值为装饰后的函数。

装饰器的原理：

1. 定义装饰器函数：**装饰器函数接受一个函数（或类）作为参数，并返回一个新的函数（或类）。这个新函数通常包含了在原始函数执行前后添加的逻辑。**
2. 应用装饰器：通过在目标函数（或类）之前加上 `@decorator_name`，将装饰器应用于目标函数。这等效于调用装饰器函数并将目标函数作为参数传递给它，然后用装饰器返回的新函数替代原始函数。
3. 调用装饰后的函数：当调用经过装饰的函数时，实际上是调用了装饰器返回的新函数。这个新函数在调用目标函数前后执行了额外的逻辑。

装饰器的应用场景包括：日志记录、权限验证、性能分析、输入校验等。它们能够在不修改原始函数代码的情况下，实现对函数行为的定制和扩展。





# verify token flask

```
# 用于验证请求的token的装饰器
def verify_request_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        if request.method == 'GET':
            # 获取请求参数中的token
            token = request.args.get('token')
        elif request.method == 'POST':
            # 获取请求参数中的token
            token = request.data.get('token')


        if token:
            conf = get_config()
            conf_token = conf["secrets"]['token']
            if token != conf_token:
                return Kit.common_rsp(data="token error", status="Forbidden")
        else:
            return Kit.common_rsp(data="token error", status="Forbidden")
        
        return func(*args, **kwargs)
    return wrapper

```





# ref

[浅谈java中注解和python中装饰器的区别](https://blog.csdn.net/a__int__/article/details/108279340)

