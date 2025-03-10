---
title: ai-agent八股
top: false
cover: false
toc: true
mathjax: true
draft: false
date: 2023-08-22 15:27:31
password:
summary:
tags:
- ai agent
categories:
- find JOB

---

# 用ai agent的个人智能助手



## 项目结构

**tools：**

- 发送邮件服务
- 查询梗百科
- 执行个人服务监控
- 设置定时通知（通过延时消息队列）
- 帮我预约学校羽毛球场地



**agent核心**

- 架构本身的能力不足，架构不是百分百完美的，是以LLM为核心决策，以tools为扩展实现多方面的计算机任务，达到类似智能化的效果。
- LLM决策智能化有限。
  - LLM目前能力有限，存在幻觉问题等等
  - LLM不能保证100%正确。



**向量数据库Chroma**

用来搭建本地知识库。（有用gpt帮我将从网络上爬取的知识结构化）





**接入交互**

通过qq机器人接入，通过/init等指令实现记忆清除。





**出现问题**

- 个人希望在里面加入ai人格化，就是拟人化，但是效果不好
- 希望通过语料库将ai变得更加接地气，但是不行，对Prompt太敏感了。

- **引入人工干预技术，针对问题：只能执行固定的tools，然后必须输入需要的参数。对于不符合的，就做人机交互来让用户来补充信息。**





## COT原理

**先描述目标任务，让LLM`think step by step`。然后将llm思考出的问题依次交给llm来回答，最后把聊天记录汇总，然gpt根据聊天记录回答出正确答案**





# 主流开源大模型对比

| 模型       | 训练数据                             | 训练数据量     | 模型参数量                       | 词表大小 |
| ---------- | ------------------------------------ | -------------- | -------------------------------- | -------- |
| LLaMA      | 以英语为主的拉丁语系，不包含中日韩文 | 1T/1.4T tokens | 7B、13B、33B、65B                | 32000    |
| ChatGLM-6B | 中英双语，中英文比例为1:1            | 1T tokens      | 6B                               | 130528   |
| Bloom      | 46种自然语言和13种编程语言，包含中文 | 350B tokens    | 560M、1.1B、1.7B、3B、7.1B、176B | 250880   |







