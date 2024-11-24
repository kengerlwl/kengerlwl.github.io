---
title: LoRA微调原理解读，及相关经验
top: false
cover: false
toc: true
mathjax: true
date: 2024-05-28 15:27:31
password:
summary:
tags:
- pytorch
- LoRA
- LLM
categories:
- 学术
---


# 介绍

LoRA属于PEFT。一种利用微调训练少量参数，来达到全量微调的效果的技术。

在实际工程中非常常用。

文本主要将LoRA原理以及为什么LoRA这么快。



## **低阶自适应参数高效微调 (LoRA) 简介**

一些微调的最佳实践包括使用强正则化、使用较小的学习率和少量的epochs。一般来说，像卷积神经网络用于图像分类的神经网络并不完全微调，这样做很昂贵，可能导致灾难性遗忘。我们只微调最后一层或最后几层。

对于LLM，我们使用一种类似的方法，称为参数高效微调（PEFT）。其中一种流行的PEFT方法是低秩适应（LoRA），LoRA 是低秩适应 (Low-Rank Adaptation) 的缩写，其是一种用于微调深度学习模型的新技术，它在模型中添加了少量可训练参数模型，而原始模型参数保持冻结。LoRA 是用于训练定制 LLM 的最广泛使用、参数高效的微调技术之一。

LoRA 可以将可训练参数数量减少 10,000 倍，GPU 内存需求减少 3 倍。尽管可训练参数更少、训练吞吐量更高且无需额外推理，LoRA 在 RoBERTa、DeBERTa、GPT-2 和 GPT-3 上的模型质量表现与微调相当或更好延迟。



# 模型结构

输入：原来的x，

计算：原来的Transformer模型固定不动。

- 原模型计算
- 新加的低秩矩阵运算。

输出：将两个计算相加合并起来。



**这样，保证了输出输出维度不变，整体的原模型结构不变，想要转换下游任务，只需要更换lora的旁路举证即可。**

![1](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/2334a36e26dc4a650f990ba36b6135d4/9a44b99c0b54b9d84cab5cd93c5ecf1a.png)



**运算图**

![refs/heads/master/image-20240528163601110](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/2334a36e26dc4a650f990ba36b6135d4/3247ebac413cbc584577a25b76210f9f.png)



## 函数

LoRA 的实现相对简单。我们可以将其视为 LLM 中全连接层的修改前向传递。在伪代码中，如下所示：

```python
input_dim = 768 # e.g., the hidden size of the pre-trained model
output_dim = 768 # e.g., the output size of the layer
rank = 8 # The rank 'r' for the low-rank adaptation

W = ... # from pretrained network with shape input_dim x output_dim

W_A = nn.Parameter(torch.empty(input_dim, rank)) # LoRA weight A
W_B = nn.Parameter(torch.empty(rank, output_dim)) # LoRA weight B

# Initialization of LoRA weights
nn.init.kaiming_uniform_(W_A, a=math.sqrt(5))
nn.init.zeros_(W_B)

def regular_forward_matmul(x, W):
    h = x @ W
return h

def lora_forward_matmul(x, W, W_A, W_B):
    h = x @ W  # regular matrix multiplication
    h += x @ (W_A @ W_B)*alpha # use scaled LoRA weights
return h
```





## LoRA为什么快和占用显存低呢

### 显存

**LoRA的显存节省在于梯度和优化器状态部分**。被冻结住的参数不用更新，自然也就不需要相应的梯度，以及Adam一阶和二阶动量。设模型参数的显存占用为**x**，原本全量训练时显存占用为**4x**，LoRA冻结住主干参数，增加了**m**%可训练的LoRA权重，则LoRA训练时，显存占用为：

- 参数部分：**(1+m%)x**；
- 梯度部分：**m%x**；
- 优化器状态部分：**2m%x.**

加起来就是**(1+4m%)x。**如**m**=1%时，最终的显存占用就从**4x**降低到了**1.04x**。



### 为什么速度快

首先分析，正常训练模型，耗时在哪。

**一个epoch：**

- 正向传播，O(n)
- 反向传播，O(n)
- 梯度更新，O(n)

加入LoRA后，各部分的耗时。

- **由于显存占用更低：batch size可以更大，**
- **正向传播没有减小**
  - 因为有了旁路矩阵，所以对于后面的层的输入X就发生的变化，所以每次都需要完整的，进行前向传播
- **反向传播可以计算并更新更少的梯度。**





# 微调经验



## 选择精度

选择半精度，节约显存，提高速度

## 通用参数

通用性的参数：学习器，学习率，epoch，batch，选择base模型

## lora参数

- 是否在不同的层加入lora

- **平衡 LoRA 超参数：R 和 Alpha**（r是秩，alpha是因子，是训练时可以设置的两个参数）

  - LoRA 权重的值越大，影响就越大。

    在之前的实验中，我采用的参数是 r=8，alpha=16，这导致了 2 倍的扩展。在用 LoRA 为大模型减重时，将 alpha 设置为 r 的两倍是一种常见的经验法则。

- **一般来说，让参数量到主模型5%，就能有不少效果**













# ref

[大模型实战：使用 LoRA（低阶适应）微调 LLM - 知乎](https://zhuanlan.zhihu.com/p/672999750)

目前常用LLAMA lora

[tloen/alpaca-lora: Instruct-tune LLaMA on consumer hardware](https://github.com/tloen/alpaca-lora)

