# git使用




# 当本地版本修改与云端发生冲突解决办法

## 未commit

使用`git stash`

- **功能**:
  - **将当前未提交的工作保存到 Git 栈中，以便稍后恢复(将当前文件恢复到上次commit)**。
  - 允许你在不想提交改动的情况下切换分支或者进行其他操作。
- **应用场景**:
  - 当你正在进行一些修改但需要紧急切换到其他分支时。
  - 在不想提交所有改动，但需要临时保存工作现场时。
  - 用于暂存工作，以便在其他地方继续工作而不丢失当前进度。

### 用法（常用就push 和pop）

1. **`git stash push`**: 这是 `git stash` 的完整形式，将未提交的更改暂存起来。

   ```
   git stash push
   ```

2. **`git stash list`**: 显示当前保存的 stash 列表。

   ```
   git stash list
   ```

3. **`git stash apply`**: 恢复最近的 stash，但不删除它。

   ```
   git stash apply
   ```

4. **`git stash pop`**: 恢复最近的 stash，并将其从栈中移除。

   ```
   git stash pop
   ```

5. **`git stash drop`**: 丢弃最近的 stash，从栈中移除。

   ```
   git stash drop
   ```

这些是基本的 `git stash` 命令及其常见用法。根据具体情况，你可以根据需要进行调整和深入学习。



`git stash pop`结果

![refs/heads/master/image-20240320002801980](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/b2f8414f6cbfc15e7744f2112f9bde7d/6564124d1c13fba84ff5a68727fc7a10.png)

然后做出修改，相当于在之前的分支上继续







## 已经commit





`git pull`

![refs/heads/master/image-20240320003754753](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/b2f8414f6cbfc15e7744f2112f9bde7d/9d9c71e96815daf4b20625a2939c90ef.png)



查看文件

![refs/heads/master/image-20240320003815852](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/b2f8414f6cbfc15e7744f2112f9bde7d/5fdf6af1eda4fd9dd760c61a225d8c95.png)



选择修改。例如二者都接受



![refs/heads/master/image-20240320003841710](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/b2f8414f6cbfc15e7744f2112f9bde7d/92ce6f1a30134b1939f9db89e452488c.png)



`merge 后push`

![refs/heads/master/image-20240320004238882](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/b2f8414f6cbfc15e7744f2112f9bde7d/eb2a32111ff31d8fa046a25e248f26c2.png)









# fetch和pull



`git fetch`是将远程主机的最新内容拉到本地，用户在检查了以后决定是否合并到工作本机分支中。

而`git pull` 则是将远程主机的最新内容拉下来后直接合并，即：`git pull = git fetch + git merge`，这样可能会产生冲突，需要手动解决。







# git rebase 和 git merge 的区别



Rebase（变基）**是将一个分支上的提交逐个地应用到另一个分支上，使得提交历史变得更加线性**。当执行rebase时，Git会将目标分支与源分支的共同祖先以来的所有提交挪到目标分支的最新位置。这个过程可以看作是将源分支上的每个提交复制到目标分支上。简而言之，rebase可以将提交按照时间顺序线性排列。

![refs/heads/master/image-20241127145850893](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/b2f8414f6cbfc15e7744f2112f9bde7d/c91a6962cf95228ea82b50b90d09959a.png)

Merge（合并）**是将两个分支上的代码提交历史合并为一个新的提交。在执行merge时，Git会创建一个新的合并提交，将两个分支的提交历史连接在一起**。这样，两个分支的修改都会包含在一个合并提交中。合并后的历史会保留每个分支的提交记录。



![refs/heads/master/image-20241127145843452](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/b2f8414f6cbfc15e7744f2112f9bde7d/38e5537a6cedbf87bf4ea17e72c7c29d.png)

