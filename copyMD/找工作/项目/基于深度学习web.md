---
title: 基于深度学习web
top: false
cover: false
toc: true
mathjax: true
draft: false
date: 2023-08-22 15:27:31
password:
summary:
tags:
- 项目
categories:
- find JOB

---





# 关于业务

具体来说，第三方会发送给我们需要用于模型训练的数据，我们针对模型实现增量训练。

同时，我们也会提供接口来实现模型的预测。但是预测的话。前端只需要看到当前的预测结果既可，不需要向前端提供数据上传功能。

每次预测结束，我们会将结果存入数据库。

由于业务要求顺序性，所以训练和预测都得按照一定顺序执行。





# 关于消息队列

削峰，解耦合，异步。

同时可能有多个任务。



消息队列创建了不同的队列，不同类型的任务分别走不通的队列，分别执行相应的训练任务。这样也能充分利用机器的性能。实现多个模型同时训练。







# 关于模型放入显存的问题







# 印象最深的问题

印象最深，服务器端时间戳不一致。

在本地测试好后，我们获取最新的日志是通过时间戳来做的。最去最新的n条日志来分析结果。

但是由于服务器端不联网等保密因素，服务器端的时间和客户端是不一致的。请你给出解决方案。

**办法：**

- 数据库会自动分配一个唯一的自增主键值，这个值可以用来排序或标识记录的顺序。
- 可以扩展为分布式id问题。





