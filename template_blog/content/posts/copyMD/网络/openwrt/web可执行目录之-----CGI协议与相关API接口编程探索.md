---
title: web可执行目录之-----CGI协议与相关API接口编程探索
top: false
cover: false
toc: true
mathjax: true
date: 2023-04-22 15:27:31
password:
summary:
tags:
- web api
- cgi
categories:
- 综合
---



# 介绍

Web 服务器的可执行目录是指用于存放 CGI 脚本或其他可执行文件的目录。它的作用是**让 Web 服务器能够通过 CGI 或其他类似机制执行这些脚本或程序，并将结果返回给客户端**。

## 需求与优点



**CGI（通用网关接口）是一种将Web服务器和外部应用程序连接起来的标准接口**，它可以使得Web服务器调用外部可执行程序来处理网页请求。下面是CGI web服务器可执行的优点和缺点：

优点：

- 灵活性高：**可以使用任何编程语言创建可执行文件，并且在需要的时候修改或更新**。
- 可扩展性强：可以方便地添加新的功能或模块，而不需要修改Web服务器的核心代码。
- 高度定制化：不同的可执行文件可以处理不同的任务，因此可以针对不同的需求进行高度定制化的配置。

缺点：

- 安全风险：由于可执行文件会直接运行在Web服务器的进程中，因此如果没有正确的安全措施，就可能存在风险。
- **性能瓶颈：每个CGI脚本都需要启动一个单独的进程来处理请求，这可能导致服务器负载增加，影响性能。**
- 代码简洁性差：使用CGI需要编写额外的可执行文件，并且需要进行繁琐的配置，因此相比于其他技术，代码简洁性较差。



### 特点，支持多语言脚本

除了下面的demo使用shell，还可以添加其他类型的可执行的文件，例如python也可以访问执行。



## demo

1. 创建一个 Shell 脚本，并设置执行权限：

   注意解释语句`#!/bin/sh`。很多服务器没有bash

   ```
   #!/bin/sh
   
   echo "Content-type: application/json"
   echo ""
   
   case "$REQUEST_METHOD" in
       GET)
           echo '{"hello": "world"}'
           ;;
       *)
           echo "Unsupported request method."
           exit 1
           ;;
   esac
   ```

2. **将脚本保存到 web 服务器的可执行目录**中，例如我的openwrt的 `/www/cgi-bin`。

3. 在 web 服务器上配置 CGI。

4. 访问您的 API：

   ```
   复制代码GET http://ip/cgi-bin/test.sh
   ```

以上代码演示了如何使用 Shell 脚本创建简单的 RESTful API。在实际应用中，您可能需要编写更复杂的 Shell 脚本，并使用 curl 或类似的工具来测试和调试您的 API。



## cgi如何传递参数

```
#!/bin/sh

# 从 QUERY_STRING 环境变量中获取查询字符串
QUERY_STRING=$(echo $QUERY_STRING | tr '&' '\n')

# 循环遍历所有参数，并输出到标准输出
for param in $QUERY_STRING; do
    name=$(echo $param | cut -d '=' -f 1)  # 获取参数名
    value=$(echo $param | cut -d '=' -f 2) # 获取参数值
    echo "parameter name: $name, value: $value"
done

```

运行

```
http://ip/test.sh?name=John&age=20 
```

