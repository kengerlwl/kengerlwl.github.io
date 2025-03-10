---
title: AISre技术点汇总
top: false
cover: false
toc: true
mathjax: true
date: 2023-08-22 15:27:31
password:
summary:
tags:
- 找工作
categories:
- find JOB
---



- 技术点

  - 强，为什么强（我有经历，github，博客）
  - 知识面广，适合万兴（结合岗位）：（开发，运维，AI）

- 未来

  - 我以后留在长沙，我对万兴非常向往

    



# AISre技术点汇总



项目介绍

```
这个项目主要是针对我们小组的智能化运营提供LLM支撑。首先我们小组的业务是和在游戏领域的账号处罚领域。然后我这边主要是提供两个智能化能力，一个是QA知识库问答，另一个是内部常见业务接入。
问答的话，我们这边参考了公司内部成熟项目的做法，以及网络上的主流架构。首先构建知识库，我这边用到的公司内的wiki，首先解析成md，然后将md树状化，方便提供更多的元信息。
然后存储检索库，本项目用的多路召回，重排，然后是知识问答，引入大小模型协同来保证回答的准确率和相应快速。有COT机制和通用。引入审核机制
业务接入我们用的langchain这种单智能体框架，通过多个Tools业务，结合ReAct机制，来完成指定业务，具体来说，Tool这边主要还是一些数据查询，error故障分析，tlog平台故障分析。
微调这边我们做的不多，主要是针对内部的一个诊断告警的业务来做的，针对pm这边的告警，触发了什么处罚，来预测最后采取的治愈方案，自部署qwen。
业务技术上来说，这边有用到redis来实现分布式锁，然后用消息队列来解耦LLM生成，然后针对数据库建立索引。

业务接入，
故障：比如出了一个普通的问题，例如数据流平台的一个错误，从error分析错误问题，从知识库检索答案，最后思考总结
生成：lua脚本生成，内部有一些知识字段是纯内部的，外部不可见，加入知识库
```



重复消费的方案

**乐观锁重试机制，重试机制，相关框架**

mybp 

es分片集群。

索引文档过程。还是ES分片

如何删除链表：快速失败异常，迭代器删除。



关于agent架构

```
- 易用性：直接从人工窗口接入，支持多模态输入
- 可靠性：使用mysql，redis作为中间数据层
- 为什么单agent，其实也多少是有一定之前考虑步不周，一开始就是单纯的选择看能不能执行完。后续发现确实有些地方可能需要优化
- 大小模型协同
- 用户如何接入，多种接入方式，确定使用场景
```





# Retrieval

## 数据分割

- 数据获取，webhook，crontab
- 数据解析，html->md。json解析成树。
- 数据切分。语义切分，递归切分
- 数据增强，无QA对，-》增强生成qa对（但是实际上不好用）
- 文档重写更新优化

- 图片生文，增强数据（直接将图片的描述加到图片下方）

## 文档检索

- 多路检索
- 重排，时间，重要性





## 检索扩展

- query重写，增强，用户不一定知道自己想问什么，或者问的不像一个问题
- 需求抽取，带上需求不利于检索。但是需求需要保留。



# 增强生成



## 文档过滤

过滤无关文档



## 答案生成（一开始的离线版本，不要求首字速度）

- 分块生成

- 主次模型：
  - 主模型语言理解能力，概括能力更强，但是上下文能力不足
  - 引入次模型，来辅助长上下文处理。
- 通用问题保底
- 一致性判断，回答是否正确（因为大模型太容易幻觉了）



## 首字客服版本

- 要求输入问题，很快就要有吞吐输出，不能够做完了再回复

- 

## token压缩

生成tokens往往是整个业务中最耗时的部分，因此如何优化这个过程非常重要。

实际体验容易压缩导致语义损失，give up





## 根据业务，灵活选择模型（大小模型协同）

**将一些关键的，但是耗时比较少，token输出少哦业务逻辑，用大模型，其他地方可以用小模型**

**例如：文档过滤，意图识别，逻辑选择**

# 模型部署

## vllm,qwen

## gemma，lamma.cpp





# agent智能接入业务

## 自定义agent

- 自动结束任务，改后的react

## 自定义chain





## agent业务逻辑

先故障诊断，诊断完以后，LLM判断需要进行资源扩缩容，这就是一个良好的react架构逻辑

- query，data，analysis
- qa问题
- cal计算
- error诊断
- zy error

- 数据报表总结生成

# 业务接入与落地

## 企业微信



## 议事厅







# 一些trick

## 验证业务可行性的trick

一开始直接上最好的模型，不要一开始就省资源，验证基于大模型能够跑通。后续在看能不能优化，用小模型替换。





## prompt工程



### 判断LLM回答正确性



### 基于参考文献判断

**为什么该方法重要，对于RAG：**

- 可以确认回答是否幻觉了
- 回答是否与参考文献一致

![refs/heads/master/image-20240815102605090](C:\Users\rainwlliu\AppData\Roaming\Typora\typora-user-refs/heads/master/images\refs/heads/master/image-20240815102605090.png)



## prompt优化

- 让LLM帮你重写（其实一般般）
- 让大模型针对错误case，进行多轮对话
  - 比如：让大模型判断对错，大模型判断错误了
  - 让大模型给出理由，针对大模型给出的理由去优化prompt



# 微调





## case1：如果效果不好，可能需要特定的system prompt

比如，可能需要加上，你是一个由openai开发的人工助手



## case2：如何判断学习了

直接看loss，一个是train上的loss，一个是val上的loss

如果loss都没有下降，那直接凉凉，得反思是不是数据有问题









# AI业务开发上的





## 关于文档更新的回滚。









# 接口暴露



## http



## xrpc，兼容其他项目业务



## 性能

日活用户最高50。周末约等于没有，主要是内部平台。

自己压测大概qps200。ai能力的接口大概是这样的。内部第三方模型提供qps100.自部署模型qps200.。6*V100 *2





# 数据库设计

知识文章信息表

知识文章打分表

日志表，聊天记录



# 数据集

指标日志，从pm里面，然后错误信息。



输出处理方案。





# 业界成功案例

- 一个team做的sre ai方案

[RunWhen Home](https://www.runwhen.com/)

- 一个智能的k8s分析器，这个star数很高

[k8sgpt-ai/k8sgpt: Giving Kubernetes Superpowers to everyone](https://github.com/k8sgpt-ai/k8sgpt)

- 智能客服
- 生成类
  - 数据库分析（实际上也是sql生成）
  - 表单生成（辅助生成一个json，或者一个格式化的数据结构）
  - 文章重写润色
  - 实体抽取
- 分析类
  - 代码分析
  - 错误分析
  - 报表生成分析
- 智能体
  - 终端智能体：辅助操作，执行任务
- 多智能体
  - 项目研发，



# 后日谈

感觉有必要看看论文，国外论坛怎么用，他们比我们早，经验更多，值得借鉴















# 个人开发经验

还是非常有必要写单测，测试完再上传，而且一次性测试，就得测试所有的。因为不好说你改动了这边，导致其他地方繃了





# 关于可控性问题

严防换觉

- rag
- prompt限定
- 生成效验

安全审核

- 接入关键字审核
- 接入人工审核







# 关于回答加速

可以压缩prompt，

结合业务上下文拆分prompt，比如prompt里面有多个可以并行的任务，那么拆分出来，并行执行。





# 关于数据治理

如何保证数据的干净和有效，

- 一个是知识库的数据
- 一个是微调的数据

- 增量数据的治理，例如和用户的回答记录，如果有用户的正反馈，那这就是一种很好的数据，需要入库。





# 关于搜索的粗排和精排



## 粗排

从多个维度，检索出比较多的文档记录。



## 精排

常见的方法

- 重排打分模型
- 分数倒数融合排序算法



## 重排

为了接入业务，即使精排阶段已经产生了准确的推荐结果，但由于业务规则、多样性需求等因素，还需要对推荐结果进行重新排序。



## 关于流式回答

为了应对流式回答，那么必须一次性喂给prompt。

那么多篇文章可能一次性输出，那么就需要rerank模型了。在粗排和精排后，需要重排模型，公司内有现成的。





# ES用redis来加速查询

es 在数据量很大的情况下（数十亿级别）如何提高查询效率啊？

- 可以用到redissearch

