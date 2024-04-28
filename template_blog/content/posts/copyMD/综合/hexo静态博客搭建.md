---
title: hexo静态博客搭建
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- hexo
- 博客
categories:
- 综合
---
# 前置环境安装

- node   v12.16.2
- npm插件安装(要进入到相关目录下面)

```
npm i hexo-cli -g
npm install
```



### push脚本

模板

```
hexo clean
hexo g
cd public


# 初始化
git init

# 设置账号
git config user.name "name"
git config user.email "email"

# commit
git add .
git commit -m "$(date) Update from Action"

# 本地切换分支
git branch gh-pages 
git checkout gh-pages 

# 强制上传
git push --force --quiet "https://kengerlwl:${GITHUB_TOKEN}@github.com/kengerlwl/kengerlwl.github.io.git"  gh-pages    

```







我本地测试

```
hexo clean
hexo g
cd public


# 初始化
git init

# 设置账号
git config --global user.name “kengerlwl”
git config --global user.email "kengerlwl@qq.com"

# commit
git add .
git commit -m "$(date) Update from Action"

# 本地切换分支
git branch gh-pages 
git checkout gh-pages 

# 强制上传
git push --force --quiet "https://kengerlwl:(token)@github.com/kengerlwl/kengerlwl.github.io.git"  gh-pages       
```



