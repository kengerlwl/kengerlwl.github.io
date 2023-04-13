---
title: mac软件推荐记录-------以及新mac的装配
cover: false
toc: true
mathjax: true
date: 2023-04-13 15:27:31
password:
summary:
tags:
- mac
- 软件
categories:
- 综合


---







# mac软件推荐记录-------以及新mac的装配

- Alfred 一个快捷工具
- bandzip 解压缩工具
- Bartender 4 上应用栏隐藏工具
- Easy New File 文件新建程序，可以类似win，右键新建某类型的程序
- iStat Menus 状态栏显示电脑信息
- Iterm 一个优秀的命令行工具
- Magnet，类似win的窗口工具
- Snipaste 图片粘贴工具
- Sublime Text 文本编辑工具







# mac zsh主题

## 安装Powerlevel9k / Powerlevel10k主题

zsh使用最多的主题

```bash
git clone https://github.com/romkatv/powerlevel10k.git $ZSH_CUSTOM/themes/powerlevel10k
复制代码
```

编辑 `~/.zshrc`  设置 `ZSH_THEME="powerlevel10k/powerlevel10k".`

再增加一行配置:`POWERLEVEL9K_MODE="awesome-patched"`

## 安装字体

- macos

```perl
https://github.com/powerline/fonts/blob/master/SourceCodePro/Source%20Code%20Pro%20for%20Powerline.otf
https://github.com/Falkor/dotfiles/blob/master/fonts/SourceCodePro%2BPowerline%2BAwesome%2BRegular.ttf
复制代码
```

打开下载的字体，然后按“安装字体”。 在iTerm2中设置字体（Preperence->Profiles->Text→Change Font）,选择`Source Code Pro + Font Awesome`,大小18，最好对“字体”和“非ASCII字体”都进行设置。重新启动iTerm2，以使所有更改生效.

## zsh配置主题

```bash
source ~/.zshrc
复制代码
```

或者执行下面的命令,重新配置

```
p10k configure
```







# ref

https://juejin.cn/post/6985123210782212132   mac主题