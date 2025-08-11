---
title: 阅读12-factor-agents
top: false
cover: false
toc: true
mathjax: true
date: 2025-07-16 15:27:31
password:
summary:
tags:
- llm
categories:
- 技术
---


# 第一章，认识软件
要认识到：软件是一个有向图。我们过去用流程图来表示程序是有原因的。
![alt text](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/f29ab4a01aec82190cd33b77e62a1648/5ad52a722027d407b20757a1a72139e6.png)
其流程，边界，是完全严谨可控的。
![alt text](../../asset/image-4.png)
让大模型自己去找这么编排处理逻辑
![alt text](../../asset/image-5.png)

## 目前简单agent存在的问题
基本agent的逻辑：
1. 需求
2. 计划
3. 执行
4. 反馈
5. 循环

问题
1. 当上下文窗口过长时，代理就会迷失方向——他们会一遍又一遍地尝试同样不成功的方法
一个目前的现象是：即使模型支持越来越长的上下文窗口，你也总是可以通过小而集中的提示和上下文获得更好的结果

一个目前普遍的共识是：
一个agent并不难处理完所有的事情，LLM的智能也不难处理所有的任务。
让大模型仅仅处理指定职能业务范围内的事情，可以更好的处理任务。


# 2. 提示词应该自己来编写，不要纯交给框架拼接生成
点评批评langchain和metagpt等的通过role和goal以及description的拼接生成提示词。
拥有自己的提示的主要好处：
```
完全控制：准确编写代理所需的指令，无需黑盒抽象
测试和评估：为你的提示构建测试和评估，就像对任何其他代码一样
迭代：根据实际表现快速修改提示
透明度：准确了解您的代理人正在执行的指令
角色黑客：利用支持非标准用户/助手角色使用的 API，
```
值得注意：prompt是程序和LLM交互的核心接口，这部分一定要严格控制。


# 3. 上下文管理是重中之重
这部分本质上是prompt的延伸。
LLM是无状态的，因此，输入给大模型的内容将直接决定LLM的输出判断质量。
- 注意，我不知道将背景传递给 LLM 的最佳方式是什么，但我知道你想要能够灵活地尝试一切。

## 标准的上下文
```
[
  {
    "role": "system",
    "content": "You are a helpful assistant..."
  },
  {
    "role": "user",
    "content": "Can you deploy the backend?"
  },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "1",
        "name": "list_git_tags",
        "arguments": "{}"
      }
    ]
  },
  {
    "role": "tool",
    "name": "list_git_tags",
    "content": "{\"tags\": [{\"name\": \"v1.2.3\", \"commit\": \"abc123\", \"date\": \"2024-03-15T10:00:00Z\"}, {\"name\": \"v1.2.2\", \"commit\": \"def456\", \"date\": \"2024-03-14T15:30:00Z\"}, {\"name\": \"v1.2.1\", \"commit\": \"abe033d\", \"date\": \"2024-03-13T09:15:00Z\"}]}",
    "tool_call_id": "1"
  }
]
```
## 有效的上下文管理

除了基于标准消息的格式之外，您还可以构建针对您的用例优化的上下文格式。例如，您可以使用自定义对象，并根据需要将其打包/展开到一个或多个用户、系统、助手或工具消息中。
以下是将整个上下文放入单个User Message中给LLM的示例：
```

[
  {
    "role": "system",
    "content": "You are a helpful assistant..."
  },
  {
    "role": "user",
    "content": |
            Here's everything that happened so far:
        
        <slack_message>
            From: @alex
            Channel: #deployments
            Text: Can you deploy the backend?
        </slack_message>
        
        <list_git_tags>
            intent: "list_git_tags"
        </list_git_tags>
        
        <list_git_tags_result>
            tags:
              - name: "v1.2.3"
                commit: "abc123"
                date: "2024-03-15T10:00:00Z"
              - name: "v1.2.2"
                commit: "def456"
                date: "2024-03-14T15:30:00Z"
              - name: "v1.2.1"
                commit: "ghi789"
                date: "2024-03-13T09:15:00Z"
        </list_git_tags_result>
        
        what's the next step?
    }
]
```

## 拥有上下文窗口的主要好处：

信息密度：以最大化 LLM 理解的方式构建信息
错误处理：以有助于 LLM 恢复的格式包含错误信息。考虑在错误和失败的调用解决后将其从上下文窗口中隐藏。
安全性：控制传递给 LLM 的信息，过滤掉敏感数据
灵活性：根据你的使用情况调整格式
令牌效率：优化上下文格式以提高令牌效率和 LLM 理解
上下文包括：提示、说明、RAG 文档、历史记录、工具调用、记忆

请记住：上下文窗口是您与 LLM 的主要界面。掌控信息的组织和呈现方式可以显著提升代理的性能。
ref:https://x.com/lenadroid/status/1943685060785524824


# 4 工具是LLM的感知
工具执行赋予大模型感知的能力，以及执行的能力


# 5 Agent应该提供使用简单的 API 启动/暂停/恢复

代理只是程序，我们对如何启动、查询、恢复和停止它们有一些期望。

# 6 使用工具来与人类交互
假设有个需求，部署。
那么需要人类同意，这种时候，可以调用一个请求审批Tool。
来与人类交互，请求人类的同意。

![alt text](../../asset/image-6.png)


# 7 模型能够主动结束流程

- 模型要求提供更多信息，打破循环并等待人类的回应
- 型要求部署后端，这是一个高风险的事情，因此打破循环并等待人工批准

# 8 错误信息是重要的上下文

- tool执行可能出错，这也是重要的上下文
- 不过要确保，宁愿是直接报错的信息，也别是虚假的，有误的上下文。（比如文件内容读取不到，应该显示无法读取，让模型自己想办法，调用别的工具，而不是直接返回空字符串，让模型以为文件为空）

# 9 做一个小而精，专注特定任务五的agent
- agent应该只做一件事情
- agent应该专注一件事情
- agent应该小而精

# 10 agent应该是无状态的
LLM是无状态的。

# ref
[humanlayer/12-factor-agents: What are the principles we can use to build LLM-powered software that is actually good enough to put in the hands of production customers?](https://github.com/humanlayer/12-factor-agents)