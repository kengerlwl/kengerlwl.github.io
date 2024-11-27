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
此外，我们还加入了最新的两种Github社区项目推荐的模型，GHTRec和GCNRec。其中，GHTRec主要基于开发者历史行为生成项目特征进行推荐，GCNRec则通过构建开发者用户网络，使用图卷积神经网络来进行推荐。
```
````





# prompt 命令（语法修改） 

````
As a professional academic English editor, you are asked to revise the grammar of the following passage and list the changes made to each section。please keep the latex grammer，the context is as follows```
```
\textbf{Temporal Pretraining Embedding Module (TPE): }Temporal Pretraining Embedding Module (TPE): In previous research on robot detection, distinguishing between humans and robots has often relied on manually observed feature creation or a text semantic perspective (Abdellatif et al., 2022). The utilization of artificial features in behavioral data typically remains at the level of statistical features, and the exploration of behavioral pattern differences between human and robot accounts is not sufficiently in-depth. Classification methods based on a text semantic approach face challenges in effectively differentiating between machine-generated text and human-generated text, especially in the context of large language models. Therefore, we primarily focus on the procedural behavior sequences of robots and propose the Temporal Pretraining Embedding module to deeply explore the robot features hidden beneath account behavioral data. It is noteworthy that in our experiments, we observed that during the data fusion process, simultaneous utilization of temporal and numerical feature data leads to the loss being trapped in a local optimum, thus unable to effectively extract temporal features. 

Therefore, our approach is to first divide the dataset into training, testing, and validation sets. 
Then, we use only the the training set data as a complete dataset  to pretrain a TPE module capable of extracting account temporal features. Subsequently, this TPE is embedded into a fusion layer as a low-dimensional vector.

In the TPE module, we train the account data using the Bi-LSTM model. On one hand, compared to a unidirectional LSTM, Bi-LSTM can better capture long-term dependencies and patterns in long sequences, ensuring the accuracy of our model (Siami et al., 2019). On the other hand, compared to models like Transformer, the deployment training cost of BiLSTM is lower, which is conducive to practical model deployment in engineering. This is significant for 实际项目落地

After obtaining a well-pretrained model, we extract the Bi-LSTM layer and incorporate it into the subsequent Feature Fusion module.
```
````





# 根据审稿意见修改

````
please help me to fix the error in my paper. I will give you the suggestions from reviewers.
here is the paper content
```
where $x_{i}$ represents the $i$th semaphore and $MA_i$ represents the $i$th semaphore after smoothing. $K$ is the step size used in the smoothing move.

Since GitHub account behaviors are usually concentrated over a period of time and then fall into a waiting void. In order to better represent the distribution state of user behavior over time. We use Bezier curves to reconstruct the raw data to more accurately reflect changes in user behavior.

```
and next is the suggestions
```
- "Since GitHub account behaviors are usually concentrated over a period of time and then fall into a waiting void." => unsubstantiated claim.

```


````









# ref处理

采用名字对应的方式



