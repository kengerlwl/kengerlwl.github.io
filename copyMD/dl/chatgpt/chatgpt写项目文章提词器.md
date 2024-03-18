---
title: chatgpt写项目文章提词器
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

# 说明

gpt ai不是万能的，只能用来辅助编写一些简单的弱逻辑性文字，而且有很多缺点

- 容易忘或者记不住，如果你给了多个要求，但是却有些冲突，那么很可能会很矛盾
- 推理能力若，得分步骤

![image-20230713140201811](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/213a09f034a4c01d390b2d1214041d01/30603d9ec5f67aec294c6cb53aa1c826.png)







# 使用身份限定

```
假定你是一个LLM领域的教授专家，接下来请你指导我回答一些问题
```





```
假定你是一个计算机领域的教授专家，主要研究方向是开源社区，健康性分析，生存预测。接下来请你辅助我完成我的论文编写。
```





# 生成大纲

````
我们计划写一份实现基于大模型的上下文关联代码生成的项目研究思路。
大概的研究思路入下文```代码块内的草稿（不完整）：
```
任务上，分为常见的T2C,C2C
方法上：
- Prompt设计：
  - 精简化
  - 上下文细节信息
  - 。。。

- 连续对话设计：判断上文信息的影响
  - 通过思维链进行推导

- 如何通用领域，针对多语言实现泛化
```
要求：
请你帮我写一份基于该方案的目录。
请以markdown的形式返回给我
````







# 降重

````
请你帮我将下面这段话用另一种表达方式写出来，但是不要改变原有意思。
要求:
1. 语句通顺，逻辑正常。
2. 保留[数字]这种引用不要变相对位置。
3. 忽略文中大量的\n换行符
段落内容在下文```块内：
```
云计算
```
````



# 批量发送论文

````
接下来我将向你分段，分多条消息输入一篇论文，你需要阅读理解他，然后再回答问题，在我发送过程中，我将遵守格式


论文内容在下文```块内：
```
xxx
```

我要继续发送后序内容，理解请回复"收到"。


请你只回复"收到"。
当发送结束，我会说：”论文发送完成”。
然后你再回答我问题。

````





# 标参考文献[n]

```
杨以光, 于会智. 基于 AES 和 RSA 加密的数据安全传输技术[J]. 电脑知识与技术: 学术版, 2006 (3): 84-86.


李瑞轩, 董新华, 辜希武, 等. 移动云服务的数据安全与隐私保护综述[J]. 通信学报, 2013, 34: 12.


请帮我给上面的参考文献，每个文献前按照顺序加上[n]，n从1开始逐渐递增输出
```







# 完善两段中间的衔接



````
请帮我完成 段A，和 段B之间的衔接段。要求语句通顺，符合逻辑，且不要用分点的方式去写，要写成一个整段。
段A内容在下文```块内：
```
xxx
```
段B内容在下文```块内：
```
xxx
```
````





# 给定主题等条件开编

````
接下来请以作战规则库为对象，技术思路是知识图谱方向，目标对象是作战规则，主题内容在下文```块内：
```
作战条令文本导入及演训数据导入分别支持批量上传对应不同类型的文件数据。条令文本导入支持上传常见的文本类型，包括但不限于. txt、. doc、. docx。演训数据导入支持上传多模态多类型数据，包括但不限于.rar、.zip、 .doc、 . docx
、.pdf、 .jpg。 多文件格式支持
```
请给出详细的设计思路，技术方案，和背景介绍，以及总结
要求：
不要出现例如1,2,3这样的序号点，可以分段，但是尽量不要分点。
不少于2000字
````





# 给定主题继续编（有前文）

````
请帮我续写下面段落，在该段落中，要以作战条令为主体，主题是：使用CI/CD 持续集成部署技术 实现从开发工具直接部署规则到集成运行环境，实现作战规则的实时更新。

续写段落的前文内容在下文```块内：
```
部署作战条令规则库在服务器上与本地 PC 上开发有很大差异。为了确保系统能够在预定环境中正常运行，遵循作战条令的要求，我们采用 Docker 技术进行部署。这样可以屏蔽系统部署对服务端环境的影响，同时方便系统功能的调整和扩展。在 Docker 中创建服务容器，其中Nginx容器可以负责多个数据间的数据负载均衡问题，Neo4j容器负责存储作战条令规则库。此外我们使用 Docker-compose.yml 文件编排各个容器为一个整体项目，以符合作战条令的规定。  部署技术架构如图 5-1 所示，与开发技术架构相比，我们将各个部分的数据以及服务用Docker来运行，通过平台层来为 Docker 提供运行环境和端口映射，使用 Docker 容器构建的逻辑层屏蔽了环境更改对应用层的影响。这种部署方式不仅保证了系统的稳定性和可靠性，同时也符合作战条令的规定和标准要求
```

````











# 在某段中加入某个要素

````
请帮我润色，修改下面```块内段落内容，在该段落中，加入作战条令的要素，构建的主体是作战规则库。（删除所有的参考文献）
```
随着
```


````







# 完善图片识别的段落

````
请帮我润色，修改以下```块内段落内容，要求，不要对该段内容做出较大修改，仅修改语法，以及排版上的小错误，同时要保证段落语句流程，逻辑通顺。
```
如图5-8所示，本文分别为两类频繁序列生成了主题图。从图中可以观察到，
人类用户数据中涉及的事件类型较多，与机器人用户相比，具有更丰富的有向关
系。这表明人类用户在平台上的行为更加多样化。相反，机器人用户数据中的主
题图表现较为稀疏，这是因为机器人更多地从事简单重复性的活动。
通过主题图的可视化分析，可以直观地了解人类用户和机器人用户在频繁序
列中的行为特征，从而揭示他们在平台上的操作习惯和行为差异。
```
````







# 翻译Prompt

````
下面我让你来充当翻译家，你的目标是把任何语言翻译成中文，请翻译时不要带翻译腔，而是要翻译得自然、流畅和地道，使用优美和高雅的表达方式。请去除上文中的[数字]标签，下面```块内是需要翻译的内容
```
We evaluate the performance of various methods for forecasting tourism demand. The data used include 366 monthly series, 427 quarterly series and 518 yearly series, all supplied to us by tourism bodies or by academics from previous tourism forecasting studies. The forecasting methods implemented in the competition are univariate and multivariate time series approaches, and econometric models. This forecasting competition differs from previous competitions in several ways: (i) we concentrate only on tourism demand data; (ii) we include approaches with explanatory variables; (iii) we evaluate the forecast interval coverage as well as point forecast accuracy; (iv) we observe the effect of temporal aggregation on forecasting accuracy; and (v) we consider the mean absolute scaled error as an alternative forecasting accuracy measure. We find that pure time series approaches provide more accurate forecasts for tourism data than models with explanatory variables. For seasonal data we implement three fully automated pure time series algorithms that generate accurate point forecasts and two of these also produce forecast coverage probabilities which are satisfactorily close to the nominal rates. For annual data we find that Naïve forecasts are hard to beat.


```
````



````
下面我让你来充当翻译家，你的目标是把任何语言翻译成英文，请翻译时不要带翻译腔，而是要翻译得自然、流畅和地道，使用优美和高雅的表达方式。请去除上文中的[数字]标签，下面```块内是需要翻译的内容
```
在Github开源社区中，随着越来越多的软件机器人参与日常活动，对开源项目的健康发展造成了影响，同时也对开源社区的基础研究数据造成了一定程度污染。目前针对Github账户的人机身份识别方法的研究还较为有限，同时也缺乏对GitHub用户行为数据的充分分析与评估。为了解决这个问题，我们提出了面向行为序列的GitHub机器人识别模型（BSO-GBD）（Behavior Sequence-based GitHub Bot Detection）。首先，我们针对5000个不同的Github账户收集了其行为数据，并针对账户行为数据做了常见序列分析。基于该行为数据集，我们设计了设计了基于线性惩罚分割的GitHub用户行为序列分割方法，并建立了行为序列驱动的GitHub用户行为信息挖掘模块（BDUEG）来挖掘用户的行为特征信息。其次，为了更加全面的考虑机器人账户的多维度特征，我们综合了GitHub账户在行为活动、社交网络、用户文本、账户资料等四个维度的35项用户特征数据，采用特征嵌入的方式融合用户行为特征，实现对GitHub账户性质的高效识别预测。实验结果表明，BSO-GBD对比已有的预测模型具有更好的预测性能，在同样账户的数据集上F1-score达到了94.1%，AUC达到了99.2%，为开源社区基础数据研究和用户身份认知提供了有力支持。
```
````







# 文章文献的引用格式生成

注意带[J]的是期刊

注意带[C]的是会议



期刊

```
这是一段论文的引用文本：AALTONEN M T. From proprietary to open-source—Growing an open-source ecosystem [J]. Journal of Systems and Software, 2012, 
请帮我写成如下格式

@article{xxx,
  title="{xxx}",
  author={xx},
  journal={xxx},
  year={2012}
}

注意：
1 如果文本中没有pages参数，就请不要随机生成，可以是空值。
2 请不要随便增删会议或期刊名字，没有期刊名字时也可以是空值
3 请不要随便增删作者名字，哪怕是缩写也不要补全成其他样子，请保持原样
4 title属性的""不要省略
5 对于一些类似于publisher等的参数，没有可以选择不要加上去
```



会议

```
这是一段论文的引用文本：DECAN A, MENS T, CLAES M, et al. On the Development and Distribution of R Packages: An Empirical Analysis of the R Ecosystem; proceedings of the ACM, F, 2015 [C].

@inproceedings{xxx,        %引用时缩写
  title="{xxx}",
  author={xx},
  booktitle={xxx},          %会议名称
  pages={xxx},                      %页码
  year={xx}                           %年份
}

注意：
1 如果文本中没有pages参数，就请不要随机生成，可以是空值。
2 请不要随便增删会议或期刊名字，没有期刊名字时也可以是空值
3 请不要随便增删作者名字，哪怕是缩写也不要补全成其他样子，请保持原样
4 title属性的""不要省略
5 对于一些类似于publisher等的参数，没有可以选择不要加上去
```



 \cite{Liao2018Empirical}前面不要加入点 .

例如错误，会编译失败
```
. \cite{Liao2018Empirical}
```

  







# ref 格式上的要求

- 请写的更多一点，但是不要分点，一段一段的写就可以了
- 不要出现例如1,2,3这样的序号点，可以分段，但是尽量不要分点。