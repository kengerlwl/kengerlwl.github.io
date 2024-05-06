```
title: hugo+LoveIt博客基本搭建
top: false
cover: false
toc: true
mathjax: true
date: 2024-05-06 09:27:31
password:
summary:
tags:
- 博客
categories:
- 综合
```







# 背景

hexo的博客编译太慢了。需要升级一下。

注意到LoveIt的主题好像很好用，决定使用





# 踩坑

-  **LoveIt**需要使用hugo的extend版本！！！！！！
- 搜索使用的是第三方插件`algolia`
  - 每次使用还需要基于npm上传到服务器

-  github pages 的重定向老是重置。
   -  在静态文件的public目录下新建一个CNAME文件，然后重定向到指定目录。








