---
title: python项目依赖管理
top: false
cover: false
toc: true
mathjax: true
date: 2024-07-18 15:27:31
password:
summary:
tags:
- python
- pip
categories:
- 综合
---



# 背景

python包管理是一个非常抽象的问题，尤其是设计cuda登显卡环境的时候更加如此。

cu的问题我解决不了，但是普通工程的依赖问题需要解决一下。



# 方法

### 1. 使用pipreqs生成requirements.txt

`pipreqs` 是一个工具，可以根据你的项目代码自动生成 `requirements.txt` 文件。

#### 安装pipreqs

```
pip install pipreqs
```

#### 生成requirements.txt

在项目根目录下运行以下命令：

```
pipreqs . --force
```

这将扫描你的项目代码，并生成一个 `requirements.txt` 文件，列出所有直接使用的库。

### 2. 使用pip-tools整理依赖

为了确保依赖的版本一致性和可重复性，可以使用 `pip-tools` 来整理和锁定依赖。

#### 安装pip-tools

```
pip install pip-tools
```

#### [创建requirements.in](http://xn--requirements-sy5ts55l.in/)

将 `pipreqs` 生成的 `requirements.txt` 文件重命名为 `requirements.in`：

```
mv requirements.txt requirements.in
```

#### 生成requirements.txt

使用 `pip-compile` 命令生成 `requirements.txt` 文件：

```
pip-compile requirements.in
```
