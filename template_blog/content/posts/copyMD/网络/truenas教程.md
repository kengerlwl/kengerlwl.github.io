---
title: truenas教程与入门
top: false
cover: false
toc: true
mathjax: true
date: 2023-06-20 15:27:31
password:
summary:
tags:
- zerotier
- 路由表
- nas
categories:
- 网络
---





# 需求

需要一个大的存储来存放一些我的个人数据。折腾了很久，要虚拟化，要功能强大，那就truenas scale了。

# 实操

- esxi 安装truenas， skip不展开讲

- esxi 基本概念，也不展开讲

  - 新建pool，这里会涉及到raid

  - 新建dataset

  - 设置网络管理（很强大）

  - 设置smb挂载

  - 设置访问权限

    



# 坑

- truenas网络问题，不提供真正的docker，提供的是k8s的使用方式，直接命令行用不了docker，只能用它的软件源里面的插件。
- 

# 结论

我建议看司波图的视频学习



# ref

[truenas换源与开启zerotier](https://www.bilibili.com/video/BV1GM4y1q7xV/?spm_id_from=..top_right_bar_window_history.content.click&vd_source=56312c73bc0637fc9a7e871063e28f0f)

[truenas教程全套视频](https://www.bilibili.com/video/BV1gG411T751/?spm_id_from=333.788&vd_source=56312c73bc0637fc9a7e871063e28f0f)



