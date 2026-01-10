# 夸克网盘实现nas云备份





# 背景

我有很多重要的文件需要上云备份，主要是为了防止本地的文件出问题。比如万一谁把我电脑丢了。

- **思路：**决定使用夸克网盘自带的文件夹自动备份功能。



# 方法

## 将目标文件挂载到windows指定目录

由于夸克只在window上使用。所以需要将nas文件夹挂载到指定目录。

注意，window默认只能挂着https的webdav。

**建议修改注册表，然后使用ip挂载！！！！！！**



## 夸克开启自动备份



挂载好后选择指定目录进行同步。

![refs/heads/master/image-20240506160205057](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/0e04e8ea6120b2de4d0ccb630b46271a/b04d07970e965da86361a62ded7a80dd.png)





# ref

[windows10挂载webdav_win10 webdav-CSDN博客](https://blog.csdn.net/qq_38894585/article/details/128818512)

