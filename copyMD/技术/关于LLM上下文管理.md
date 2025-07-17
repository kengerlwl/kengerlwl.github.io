---
title: 关于LLM上下文管理
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

# 背景


# 方法

# 1. 裁剪
超过一定长度的token，或者超过指定阈值。
就将更远（旧）的上下文直接裁剪掉。

# 2. 压缩
同上，但是不是裁剪，而是压缩更旧的上下文。
比如更远的，70%的压缩，保留较近的30%的上下文。

但是怎么压缩是有讲究的，一般是用小模型。
来总结出，目标，关键点，约束，历史计划，已经执行步骤，进度。这些可能分为来一个json。或者xml格式。

# 3.
