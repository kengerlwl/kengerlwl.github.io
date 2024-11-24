---
title: 大模型agent框架调研
top: false
cover: false
toc: true
mathjax: true
date: 2024-07-25 14:27:31
password:
summary:
tags:
- pytorch
- 推理
- LLM
categories:
- 学术
---



# 背景

最近需要用到这玩意儿，但是我目前只知道langchain等框架，对市场缺乏一个调研。

需要做一个技术选型。

实际上：agent，本质上就是一个tool选择器。根据NLP输入的需求，选择需要执行的tool动作，



# 决策模型



## ReAct框架

目前Agent主流的决策模型是ReAct框架，也有一些ReAct的变种框架，以下是两种框架的对比。



- 传统ReAct框架：Reason and Act



ReAct=少样本prompt + Thought + Action + Observation 。是调用工具、推理和规划时常用的prompt结构，先推理再执行，根据环境来执行具体的action，并给出思考过程Thought。



![refs/heads/master/image](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/2af73fc674bc1670e2bbb53830958266/ff8a902d9f6ce504309c32968ef5ba9d.png)



## Plan-and-Execute ReAct



类BabyAgi的执行流程：一部分Agent通过优化规划和任务执行的流程来完成复杂任务的拆解，将复杂的任务拆解成多个子任务，再依次/批量执行。



优点是对于解决复杂任务、需要调用多个工具时，也只需要调用三次大模型，而不是每次工具调用都要调大模型。



![refs/heads/master/image](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/2af73fc674bc1670e2bbb53830958266/634ae8defb304246f81912feb855a5e9.jpeg)

LLmCompiler：并行执行任务，规划时生成一个DAG图来执行action，可以理解成将多个工具聚合成一个工具执行图，用图的方式执行某一个action





# Single-Agent一个智能体来解决任务

## LangChain 

不说了，目前第一

## Outlines

([GitHub - outlines-dev/outlines: Structured Text Generation](https://github.com/outlines-dev/outlines))这个工具让开发者能精确控制文本生成，提供了多种生成方法，能保证输出符合正则表达式或JSON模式。它还支持所有模型，让开发者能更灵活地使用

## AgentGPT

([GitHub - reworkd/AgentGPT: 🤖 Assemble, configure, and deploy autonomous AI Agents in your browser.](https://github.com/reworkd/AgentGPT))为企业设计的一个解决方案，通过网页浏览器介绍自给自足的AI代理。它依赖用户输入来完成任务，还能长期记忆和探索网页。

## LlamaIndex 

([LlamaIndex 🦙 v0.10.18.post1](https://docs.llamaindex.ai/en/stable/))一个多功能的数据管理工具，可以从API、PDF、SQL数据库等多种来源提取数据，然后优化数据格式，让LLMs能更好地理解。它支持自然语言查询，让你能更自然地跟数据对话。

# autoGPT

[Significant-Gravitas/AutoGPT: AutoGPT is the vision of accessible AI for everyone, to use and to build on. Our mission is to provide the tools, so that you can focus on what matters.](https://github.com/Significant-Gravitas/AutoGPT)

AutoGPT 定位类似个人助理，帮助用户完成指定的任务，如调研某个课题。AutoGPT比较强调对外部工具的使用，如搜索引擎、页面浏览等。

同样，作为早期agent，autoGPT**麻雀虽小五脏俱全**，虽然也有很多缺点，比如无法控制迭代次数、工具有限。但是后续的模仿者非常多，基于此演变出了非常多的框架。

## HuggingGPT

git: https://github.com/microsoft/JARVIS

paper: https://arxiv.org/abs/2303.17580

HuggingGPT的任务分为四个部分：

1. 任务规划：将任务规划成不同的步骤，这一步比较容易理解。
2. 模型选择：在一个任务中，可能需要调用不同的模型来完成。例如，在写作任务中，首先写一句话，然后希望模型能够帮助补充文本，接着希望生成一个图片。这涉及到调用到不同的模型。
3. 执行任务：根据任务的不同选择不同的模型进行执行。
4. 响应汇总和反馈：将执行的结果反馈给用户。







## GPT-Engineer

git: https://github.com/AntonOsika/gpt-engineer

基于langchain开发，单一的工程师agent，**解决编码场景的问题。CODE领域**

目的是创建一个完整的代码仓库，在需要时要求用户额外输入补充信息。





# Multi-Agent使用多个智能体来解决更复杂的问题

**比如要开发一个程序，不仅仅需要程序员，还需要产品，运维，市场，销售，老板来参与进来。需要大家共同来讨论，因此，基于多个agent分别扮演不同的角色，通过交互来实现复杂智能组，解决一些复杂问题。**

## 斯坦福虚拟小镇

git：https://github.com/joonspk-research/generative_agents

paper：https://arxiv.org/abs/2304.03442

虚拟小镇作为早期的multi-agent项目，很多设计也影响到了其他multi-agent框架，里面的反思和记忆检索feature比较有意思，模拟人类的思考方式。

## MetaGPT

git：https://github.com/geekan/MetaGPT

doc：https://docs.deepwisdom.ai/main/zh/guide/get_started/introduction.html

**metaGPT是国内开源的一个Multi-Agent框架，目前整体社区活跃度较高和也不断有新feature出来，中文文档支持的很好。**

metaGPT以软件公司方式组成，目的是完成一个软件需求，输入一句话的老板需求，输出用户故事 / 竞品分析 / 需求 / 数据结构 / APIs / 文件等。

![e2576f30dd664ff240603479e29c22dd.png](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/2af73fc674bc1670e2bbb53830958266/a8f88e35e62d2f996b742249cc9c43bb.png)

MetaGPT内部包括产品经理 / 架构师 / 项目经理 / 工程师，它提供了一个软件公司的全过程与精心调配的SOP





## AutoGen

doc：https://microsoft.github.io/autogen/docs/Getting-Started

AutoGen是**微软**开发的一个通过代理通信实现复杂工作流的框架。目前也是活跃度top级别的Multi-Agent框架，与MetaGPT“不相上下”。

