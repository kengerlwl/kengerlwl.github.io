---
title: chatgpt写论文Prompt
top: false
cover: false
toc: true
mathjax: true
date: 2023-04-3 15:27:31
password:
summary:
tags:
- chatgpt
categories:
- 综合

---



# 学术翻译为英语

````
As a professional academic English editor , you are asked to translate the following paragraph into English, the context is as follows```

```
为了解决上述问题，本文主要针对GitHub平台中的用户身份识别进行了分析与研究，我们收集了GitHub用户的行为数据，提出了基于线性惩罚分割的行为序列分割方法和改进的 PrefixSpan 算法构建了用户的行为序列数据，从时序角度分析了用户的行为模式，并以此提出了一个面向行为序列的GitHub机器人识别模型（BSO-GBD），通过集成时序预训练嵌入模块(TPE）挖掘隐藏在账户行为数据下的机器人特征以及融合GitHub账户的多维特征信息实现对GitHub账户的识别预测。本文的贡献如下：

```
````





# prompt 命令（语法修改） 

````
As a professional academic English editor, you are asked to revise the grammar of the following passage and list the changes made to each section。please keep the latex grammer，the context is as follows```
```
From Table 5, we can see that our BSO-GBD has the best classification effect compared to existing methods.The two models BIAMN and BoDeGHa mainly classify accounts from the textual similarity of the account comments, but due to the sparseness of the textual content, they do not perform well on our dataset.BotHunter, although it takes into account numerous user features, such as account information, account behavior indicators, and text similarity. However, it relies too much on some features, such as whether the account profile contains strings such as 'bot' or not. After removing this information, the effect will be greatly reduced. In the end, our model achieves excellent results after considering the behavioral sequence information of accounts and some important account features.
```
````









# ref处理

采用名字对应的方式



