# git子仓库





# 背景

一个仓库下面用到了另一个仓库。

**那么什么是Git的子仓库呢?**

通俗上的理解, 一个Git仓库下面放了多个其他的Git仓库,其他的Git仓库就是我们父级仓库的子仓库。





# 方法



## ` git submodule(子模块)`

Git子模块允许我们将一个或者多个Git仓库作为另一个Git仓库的子目录,它能让你将另一个仓库克隆到自己的项目中,同时还保持提交的独立。

### 添加子模块

要将一个 Git 仓库添加为子模块到你的项目中，可以使用 `git submodule add` 命令：

```
bash
Copy code
git submodule add <repository_url> <path>
```

- `<repository_url>` 是子模块的 Git 仓库地址。
- `<path>` 是子模块将被添加到的目录路径。

### 初始化子模块

一旦子模块被添加到项目中，需要初始化它。这将会拉取子模块的内容到本地：

```
bash
Copy code
git submodule update --init
```

### 更新子模块

要更新子模块到它的最新版本，可以使用以下命令：

```
bash
Copy code
git submodule update --remote
```

### 提交对子模块的更改

在对子模块进行修改后，需要将这些更改提交到父仓库：

```
bashCopy codecd <submodule_directory>
# 在子模块中进行修改
git add .
git commit -m "Updated submodule"
cd ..
git add <submodule_directory>
git commit -m "Updated submodule reference"
```

### 删除子模块

如果需要移除一个子模块，需要执行以下步骤：

1. 删除 `.gitmodules` 文件中子模块的相关条目。
2. 删除 `.git/config` 文件中子模块的相关配置。
3. 删除子模块的目录。
4. 提交这些更改到父仓库。







# ref

[git-github 子模块仓库更新（git submodule）/git中submodule子模块的添加、使用和删除_git submodule sync-CSDN博客](https://blog.csdn.net/inthat/article/details/108416238)

