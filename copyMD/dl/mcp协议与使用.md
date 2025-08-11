---
title: mcp协议与使用
top: false
cover: false
toc: true
mathjax: true
date: 2025-08-15 15:27:31
password:
summary:
tags:
- mcp
- agent
categories:
- 学术
---
# 背景

什么是mcp。

Model Context Protocol (MCP)。是一个模型上下文协议。

MCP 提供：

- **越来越多的预建集成**可供您的 LLM 直接插入
- 为 AI 应用程序构建自定义集成**的标准化方法**
- 每个人都可以自由实施和使用的**开放协议**
- 在不同应用程序之间切换并随身携带上下文的**灵活性**



# 使用

mcp实际上就是tool。prompt，resource等资源的接入服务。
将传统的代码强耦合解耦。

其提供了

- stdio接入
- http接入
  - streamable接入
  - sse接入



