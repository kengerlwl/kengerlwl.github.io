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

**通常模板ACM Reference Format和左下角的会议信息会和今年的不符，我们不需要修改，中稿后编辑会给你发新的信息**





## 匿名

投稿中不能出现各种个人信息，最好的办法是使用给定的匿名模式：

```
\documentclass[sigconf,anonymous]{acmart}
```



## 标识

此外，为了标识文章，需要事先申请ID，先到所投会议处投个abstract申请一下id。比如[MM 2019的Easychair链接](https://easychair.org/conferences/?conf=acmmm2019)，然后写在文章中：

```
\acmSubmissionID{***}
```

此外，和会议相关的信息可以不用改。

例如，202就是我的id

![image-20230420111132042](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7f588d14531a9e2231c0950d124be9df/952ed478d7e14957e6efe698d26563b9.png)



## 关于机构冲突问题

主要看看有没有所属机构有冲突，没有就填None之类





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

![v2-23b67081dc78de280d25e4f4e1362964_b](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7f588d14531a9e2231c0950d124be9df/7777188702cac7c62991c637ec555c67.png)



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







## 左上角的会议名称

```

\acmConference[Internetware 2023]{Make sure to enter the correct
  conference title from your rights confirmation emai}{ August 4-6, 2023}{Hangzhou, China}
  
  名为 "Internetware 2023"，将于 2023 年 8 月 4 日至 6 日在中国杭州举行。该会议可能涉及互联网技术、软件工程和计算机科学等领域的研究成果和趋势。
```







![image-20230419204928081](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7f588d14531a9e2231c0950d124be9df/800bf5664042fce1de778abbc9fa6650.png)







# 如何查找会议或者期刊的bib引用

- 使用谷歌学术
- ![image-20230419213615531](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7f588d14531a9e2231c0950d124be9df/29f8b5bf1fa566f42e1cf060267713a0.png)



- 使用chatgpt生成。具体参考gpt提词器博客

- 对于名字不全，只能在文章中提到做什么的论文，可以把对该论文的描述发给new bing看能不能搜索到，如何我搜索到了

![image-20230419214052251](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/7f588d14531a9e2231c0950d124be9df/3eabb9953f63e269f1b44453d7e47153.png)







# 纠错

### Misplaced alignment tab character &. 

1. 如果您想要输出一个“&”符号，请使用“\\&”代替。比如，在给定的例子中，可以将“Free & Open-Source”修改为“Free and Open-Source”，或者使用“Free \textbackslash& Open-Source”来输出带有“&”符号的文本。

   注意，不仅在正文tex里面要注意这个问题，还有bib文件里面也要注意这个问题。

   



# ref

[如何选择论文模板](https://blog.csdn.net/baishuiniyaonulia/article/details/125005752)

[如何插入图片](https://zhuanlan.zhihu.com/p/32925549)

[ref的参考文献顺序](https://blog.csdn.net/zjc910997316/article/details/117418402)

[会议投稿心得1](http://wang22ti.com/2019/04/10/%E7%AC%94%E8%AE%B0-%E4%BC%9A%E8%AE%AE%E6%8A%95%E7%A8%BF-MM/)



