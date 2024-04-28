# win上使用mklink创建软连接实现跨盘共享

win上使用mklink创建软连接实现跨盘共享



# 背景

想要将win上nas的文件，上传到onedrive。

计划先将nas挂载到本地作为z盘。

然后把z盘创建软连接到onedrive的目录。





# 方法

```
mklink /d  "C:\Users\kenger\OneDrive - 6svtmz\vr\done" "Z:\kenger\done\#整理完成"


相当于把"Z:\kenger\done\#整理完成"文件夹里面的内容，挂载到"C:\Users\kenger\OneDrive - 6svtmz\vr\done"里面
```


