---
title: RLHF算法
top: false
cover: false
toc: true
mathjax: true
date: 2024-07-23 15:27:31
password:
summary:
tags:
- pytorch
- RLHF
- LLM
categories:
- 学术
---



# 背景



- **PPO(Proximal Policy Optimization)近端策略优化算法**

它属于策略梯度方法的一种，旨在通过限制新策略和旧策略之间的差异来稳定训练过程。PPO通过引入一个称为“近端策略优化”的技巧来避免过大的策略更新，从而减少了训练过程中的不稳定性和样本复杂性。





# 方法



## 强化学习背景概念

### 强化学习基本概念



![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/cbe20f3c867c494a3822fcf8ee25f5b2/ecc5ef3a07ad7c820e92179ec29f5d54.webp)

- 强化学习的两个实体：**智能体（Agent）**与**环境（Environment）**

- 强化学习中两个实体的交互：

- - **[状态空间](https://zhida.zhihu.com/search?q=状态空间&zhida_source=entity&is_preview=1)S**：S即为State，指环境中所有可能状态的集合
  - **动作空间A**：A即为Action，指智能体所有可能动作的集合
  - **奖励R：**R即为Reward，指智能体在环境的某一状态下所获得的奖励。

以上图为例，智能体与环境的交互过程如下：

- 在 t 时刻，环境的状态为 St ，达到这一状态所获得的奖励为 Rt
- 智能体观测到 St 与 Rt ，采取相应动作 At
- 智能体采取 At 后，环境状态变为 St+1 ，得到相应的奖励 Rt+1

智能体在这个过程中学习，它的最终目标是：**找到一个策略，这个策略根据当前观测到的环境状态和奖励反馈，来选择最佳的动作。**



### 如何更好的选择下一个动作，使用价值函数

**t时刻状态s的总收益 = 身处状态s能带来的即时收益 + 从状态s出发后能带来的未来收益。**写成表达式就是：
`Vt=Rt+γVt+1`

其中：

- Vt ： t 时刻的总收益，注意这个收益蕴涵了“即时”和“未来”的概念
- Rt ： t 时刻的[即时收益](https://zhida.zhihu.com/search?q=即时收益&zhida_source=entity&is_preview=1)
- Vt+1 ： t+1 时刻的总收益，注意这个收益蕴涵了“即时”和“未来”的概念。而 Vt+1 对 Vt 来说就是“未来”。
- γ ：折扣因子。它决定了我们在多大程度上考虑将“未来收益”纳入“当下收益”。







## NLP与强化学习

对应于强化学习的概念。

- 智能体->待训练的模型，我们希望这个模型表现得更加符合我们的期望，得分更高
- 环境->已有的prompt输入，ref model。
- 状态->当前模型的输入，以及输出的token
- 动作->模型的下一个输出



NLP任务做强化学习（RLHF）的目的：**我们希望给模型一个prompt，让模型能生成符合人类喜好的response**。再回想一下[gpt模型](https://zhida.zhihu.com/search?q=gpt模型&zhida_source=entity&is_preview=1)做推理的过程：**每个时刻** t **只产生一个token，即token是一个一个蹦出来的，先有上一个token，再有下一个token。**

![v2-eb250d428d3b9a751d4ba3aeae70e290_1440w](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/cbe20f3c867c494a3822fcf8ee25f5b2/9d41c9cf600d23244d8e67a3ba7b6f7a.webp)





### 四个相关模型

如下图，**在[RLHF-PPO阶段](https://zhida.zhihu.com/search?q=RLHF-PPO阶段&zhida_source=entity&is_preview=1)，一共有四个主要模型**，分别是：

- **Actor Model：[演员模型](https://zhida.zhihu.com/search?q=演员模型&zhida_source=entity&is_preview=1)**，这就是我们想要训练的目标语言模型
- **Critic Model：评论家模型**，它的作用是预估总收益 Vt
- **[Reward Model](https://zhida.zhihu.com/search?q=Reward+Model&zhida_source=entity&is_preview=1)：奖励模型**，它的作用是计算即时收益 Rt
- **Reference Model：[参考模型](https://zhida.zhihu.com/search?q=参考模型&zhida_source=entity&is_preview=1)**，它的作用是在RLHF阶段给语言模型增加一些“约束”，防止语言模型训歪（朝不受控制的方向更新，效果可能越来越差）

![v2-22c2f6fce157dc4385a14f0de50d8136_r](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/cbe20f3c867c494a3822fcf8ee25f5b2/3c0dd9a02fdbd15ebfd81498f14bd8d8.jpg)



其中:

- **Actor/Critic Model**在RLHF阶段是**需要训练**的（图中给这两个模型加了粗边，就是表示这个含义）；而**Reward/Reference Model**是**参数冻结**的。
- 实际上，actor和ref model通常用的同一个模型， reward和critic也是同一个模型，只不过一个冻结，一个不断迭代更新。



### actor model

![v2-eb250d428d3b9a751d4ba3aeae70e290_1440w](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/cbe20f3c867c494a3822fcf8ee25f5b2/9d41c9cf600d23244d8e67a3ba7b6f7a.webp)

实际上，每次是输入一个prompt，然后输出一个answer。一次性计算当前的Rt



### Reference Model（参考模型）

**Reference Model（以下简称Ref模型）一般也用SFT阶段得到的SFT模型做初始化，在训练过程中，它的参数是冻结的。**[Ref模型](https://zhida.zhihu.com/search?q=Ref模型&zhida_source=entity&is_preview=1)的主要作用是防止Actor”训歪”，那么它具体是怎么做到这一点的呢？

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/cbe20f3c867c494a3822fcf8ee25f5b2/84b3ed2927623236b9c89e9e0a546c32.webp)

“防止[模型训歪](https://zhida.zhihu.com/search?q=模型训歪&zhida_source=entity&is_preview=1)”换一个更详细的解释是：**我们希望训练出来的Actor模型既能达到符合人类喜好的目的，又尽量让它和SFT模型不要差异太大**

简言之，**我们希望两个模型的输出分布尽量相似**。那什么指标能用来衡量输出分布的相似度呢？我们自然而然想到了**KL散度**。



**如图所示！！！：**

- **对Actor模型**，我们喂给它一个prompt，它正常输出对应的response。那么response中每一个token肯定有它对应的log_prob结果呀，我们把这样的结果记为**log_probs**
- **对Ref模型**，我们把Actor生成的"prompt + response"喂给它，那么它同样能给出每个token的log_prob结果，我们记其为**ref_log_probs**
- 那么这两个模型的输出分布相似度就可以用**`ref_log_probs - log_probs`**来衡量，我们可以从两个方面来理解这个公式：



### Critic Model（评论家模型）

**Critic Model用于预测期望总收益** Vt **，和Actor模型一样，它需要做参数更新**。

这里critic和reward用的同一个模型参数



**所以总结来说，在RLHF中，我们不仅要训练模型生成符合人类喜好的内容的能力（Actor），也要提升模型对人类喜好[量化判断](https://zhida.zhihu.com/search?q=量化判断&zhida_source=entity&is_preview=1)的能力（Critic）！！！！！！**。这就是Critic模型存在的意义。我们来看看它的大致架构：

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/cbe20f3c867c494a3822fcf8ee25f5b2/c5f04c942d5294e3082781ee6e2759b7.webp)

- value head很多时候就是一个全连接层，用于做维度变换

在图中， Vt 表示Critic模型对 t 时刻及未来（response完成）的收益预估。



### Reward Model（奖励模型）

Reward Model用于计算生成token At 的即时收益，它就是RW阶段所训练的奖励模型，在RLHF过程中，它的参数是冻结的。

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/cbe20f3c867c494a3822fcf8ee25f5b2/01b9dfe72bb65905a6b978ffbc473a5a.webp)


**你可能想问：为什么Critic模型要参与训练，而同样是和收益相关的Reward模型的参数就可以冻结呢？**
这是因为，Reward模型是站在上帝视角的。这个上帝视角有两层含义：

- 第一点，Reward模型是经过和“估算收益”相关的训练的，因此在RLHF阶段它可以直接被当作一个能产生客观值的模型。
- 第二点，Reward模型代表的含义就是“即时收益”，你的token At 已经产生，因此即时收益自然可以立刻算出。





## LOSS计算

- **[Actor loss](https://zhida.zhihu.com/search?q=Actor+loss&zhida_source=entity&is_preview=1)：**用于评估Actor是否产生了符合人类喜好的结果，将作用于Actor的BWD上。
- **[Critic loss](https://zhida.zhihu.com/search?q=Critic+loss&zhida_source=entity&is_preview=1)：**用于评估Critic是否正确预测了人类的喜好，将作用于Critic的BWD上。





## 总体流程

![a2fbc36040619a6267fb9816b06ff9b4.jpeg](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/cbe20f3c867c494a3822fcf8ee25f5b2/158714cbb383e72c18d8369f5974020d.jpeg)

- 首先用actor model在**推理模式**下根据prompt生成一个answer（prompt对应强化学习里边的state，answer对应一些列的action）

- 然后利用reward model和ciric model对输出的prompt+answer进行打分（PPO训练时使用的奖励值并不单单是reward model的输出还要考虑kl散度，后文介绍）

- actor model是我们想通过强化学习微调的大模型，但是强化学习过程很容易把模型训练“坏”，因此需要另外一个**不会参数更新**的 ref_model来当作标的，别让actor mode跑偏太远。我们在**训练模式**下，**将prompt+answer分别输入到actor mode和ref model，用KL散度来衡量 ref model和actor mode输出的差别。同时将KL散度（衡量数据分布差距大小）纳入损失函数**（KL散度本质是纳入到奖励值里边的，奖励值被纳入到了损失函数），进而来约束 ref_model和actor mode的输出分布别差距太大。具体代码如下：

  

  ### PPO训练

  ![3996c57c1ce7ff9114fa4f7d5fff24c5](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/cbe20f3c867c494a3822fcf8ee25f5b2/2550d8af3c5b5b17bfd5e23b043e952c.jpeg)







# ref

[图解大模型RLHF系列之：人人都能看懂的PPO原理与源码解读 - 知乎](https://zhuanlan.zhihu.com/p/677607581?utm_psn=1816795120613322752)

[详解大模型RLHF过程（配代码解读） - 知乎](https://zhuanlan.zhihu.com/p/624589622)
