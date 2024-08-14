---
title: 大模型token压缩
top: false
cover: false
toc: true
mathjax: true
date: 2024-08-14 15:27:31
password:
summary:
tags:
- pytorch
- Tokens压缩
- LLM
categories:
- 学术
---

# 背景

最近在大模型推理方面遇到了瓶颈，需要进一步优化性能，因此决定记录一下这方面的研究。

**Tokens 压缩旨在减少语言模型处理的文本量，以提高效率和泛化能力**。根据是否利用特定任务信息，提示压缩方法分为两大类：任务感知型压缩和任务不可知型压缩。

### 好处

- 提高上下文利用率，减少冗余信息
- 降低计算成本

### 任务感知型压缩

任务感知型压缩方法专注于根据下游任务或当前查询来定制压缩策略。例如，LongLLMLingua采用了问题感知的压缩方法，通过粗到细的策略估计令牌的信息熵，并根据问题调整这一估计。此外，基于强化学习的方法通过下游任务的奖励信号来训练压缩模型，而软提示调整方法则通常需要针对特定任务进行微调。

- **优点**：这些方法能够为特定任务生成高度定制化的压缩提示，提高任务执行的准确性。
- **缺点**：由于过度定制，这些方法的泛化能力受限，可能不适用于未见过的任务或数据集。此外，它们可能需要针对每个新任务进行额外的训练或调整，增加了部署成本。

### 任务不可知型压缩

与任务感知型压缩不同，任务不可知型压缩方法不依赖于特定任务的信息，因此更适合广泛的应用场景和黑盒语言模型。这类方法通常使用基于信息熵的度量来识别并移除提示中的冗余信息。代表性做法是利用小型语言模型来评估令牌的重要性。基于总结的压缩方法也被用于任务不可知型压缩，以压缩文本而不考虑特定任务。

- **优点**：任务不可知型压缩方法具有更好的适应性和通用性，能够应对多种任务和语言模型。
- **缺点**：这些方法可能无法有效捕捉特定语言模型优化的令牌重要性分布，且计算开销较大。基于总结的压缩方法可能会遗漏关键细节，影响压缩文本的质量和泛化能力。



# 业务

选择第二种，基于LLMlingua2实现。

[microsoft/LLMLingua: To speed up LLMs' inference and enhance LLM's perceive of key information, compress the prompt and KV-Cache, which achieves up to 20x compression with minimal performance loss.](https://github.com/microsoft/LLMLingua)

直接缩短了接近一半。

![image-20240814154442191](https://cdn.jsdelivr.net/gh/kengerlwl/kengerlwl.github.io/image/8aa8605ff9d42c05e3d8fab4d9dbe35e/55c00a0e7b68357f6a89418eaaeeec1a.png)





# 注意

对于我遇到的稀烂的文档，最好还是谨慎压缩，压缩出来效果不太好。

**至少压缩出来人都读不懂了。。。**





不过倒是可以考虑让个轻量级的大模型来重塑。。。
