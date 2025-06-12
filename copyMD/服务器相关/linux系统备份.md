---
title: linux系统备份
top: false
cover: false
toc: true
mathjax: true
date: 2025-06-12 15:27:31
password:
summary:
tags:
- 服务器
- 系统备份
categories:
- 服务器
---
# 背景

需要备份一下系统，方便迁移。



# 方法

#### 1. 创建备份目录

```
mkdir -p /home/kenger/backup
```

#### 2. 执行打包备份

```
sudo tar --exclude=/proc \
          --exclude=/tmp \
          --exclude=/sys \
          --exclude=/dev \
          --exclude=/run \
          --exclude=/mnt \
          --exclude=/media \
          --exclude=/lost+found \
          --exclude=/home/kenger/backup \
          -cvpzf /home/kenger/backup/full-backup.tar.gz /
```

- `--exclude=/home/kenger/backup` 防止打包自身导致死循环。
- 替换 `kenger` 为你自己的用户名。

------

### ✅ 备份完成后

你会在 `/home/kenger/backup/` 下看到一个压缩包：

```
full-backup.tar.gz
```

大小大概在 5～15GB（取决于你系统安装的软件和数据量）。

------

### ✅ 恢复方式（将来重装或灾难恢复）

> 启动 Live USB 后挂载原系统所在分区为 `/mnt`，然后：

```
sudo tar -xvpzf /mnt/home/kenger/backup/full-backup.tar.gz -C /mnt
```

然后重新 chroot 和安装 grub。