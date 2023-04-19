---
title: latex第一次实践
top: false
cover: false
toc: true
mathjax: true
date: 2023-04-15 15:27:31
password:
summary:
tags:
- pytorch
categories:
- 学术
---
# latex





# 会议常用模板

## 单列模板 sample-acmsmall

顾名思义，就是单栏的模板。

![34e8d716411043c08c7ffba9fbba23de.png](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7f588d14531a9e2231c0950d124be9df/793e82e3ab7d848ddec0d1f3b1ace133.png)

## 双列模板 sample-sigconf

**就是双栏的模板，这是大多数时候都适用的模板。下面也是以这个展开**







# 关于CFF 会议论文



## CCS CONCEPTS 论文分类

CCS CONCEPTS这个东西简单来说可以看作一个论文的分类索引，**是ACM出版论文时论文中必须要附带的东西，一般来说不需要提前放入，等到论文出版时自然会有编辑通知是否需要插入。**

例如：

![image-20230416214128225](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7f588d14531a9e2231c0950d124be9df/7fda6ebc57bacaaa2323abdc9edd159a.png)

前往[https://dl.acm.org/ccs#](https://dl.acm.org/ccs#)可以查看分类检索系统。







## 首段缩进

CCF会议以及期刊论文，某个section的，或者subsecion。第一个段落都省略缩进。

![image-20230416215615378](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7f588d14531a9e2231c0950d124be9df/820fc704d0fcb0ab842e61dfb53b940c.png)



**在使用CCF提供的会议模板时，您不需要使用\noindent命令就可以达到首段无缩进的效果**

因为在CCF提供的会议模板中，在正文部分的每个新段落开头，默认情况下都不会有缩进。这是因为该模板中已经定义了一个新的段落格式，其中包含了取消首行缩进的设置。





## 图表

在latex中要使用图表的话需要导入一些库和宏包。具体来说，例如

**单图插入的基本用法**

```text
%导言区插入下面三行
\usepackage{graphicx} %插入图片的宏包
\usepackage{float} %设置图片浮动位置的宏包
\usepackage{subfigure} %插入多图时用子图显示的宏包

\begin{document}

\begin{figure}[H] %H为当前位置，!htb为忽略美学标准，htbp为浮动图形
\centering %图片居中
\includegraphics[width=0.7\textwidth]{DV_demand} %插入图片，[]中设置图片大小，{}中是图片文件名
\caption{Main name 2} %最终文档中希望显示的图片标题
\label{Fig.main2} %用于文内引用的标签
\end{figure}

\end{document}
```

![v2-23b67081dc78de280d25e4f4e1362964_b](https://pic1.zhimg.com/v2-23b67081dc78de280d25e4f4e1362964_b.jpg)



**多图横排+默认编号**

```tex
%导言区插入下面三行
\usepackage{graphicx}
\usepackage{float} 
\usepackage{subfigure}

\begin{document}
Figure \ref{Fig.main} has two sub figures, fig. \ref{Fig.sub.1} is the travel demand of driving auto, and fig. \ref{Fig.sub.2} is the travel demand of park-and-ride.

\begin{figure}[H]
\centering  %图片全局居中
\subfigure[name1]{
\label{Fig.sub.1}
\includegraphics[width=0.45\textwidth]{DV_demand}}
\subfigure[name2]{
\label{Fig.sub.2}
\includegraphics[width=0.45\textwidth]{P+R_demand}}
\caption{Main name}
\label{Fig.main}
\end{figure}
\end{document}
```

编译完成后的效果：

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7f588d14531a9e2231c0950d124be9df/5aeff1da6bd1851da2fb6dd839bd06bb.png)



### 表格过宽问题

```c
\usepackage{graphicx} # 记得加宏包
\resizebox{\linewidth}{!}{  #此处！表示根据根据宽高比进行自适应缩放
\begin{tabular}...
....
....
\end{tabular}
} # 注意加的位置在\begin{tabular}和\end{tabular}前后
```

关键就是：

```
\resizebox{\linewidth}{!}{  #此处！表示根据根据宽高比进行自适应缩放

表格

}
```











# ref

[如何选择论文模板](https://blog.csdn.net/baishuiniyaonulia/article/details/125005752)

[如何插入图片](https://zhuanlan.zhihu.com/p/32925549)



