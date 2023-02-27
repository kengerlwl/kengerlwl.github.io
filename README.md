# 如何使用自建github图床搭建github pages博客

## 技术
- 博客使用hexo框架
- 图源管理使用自己写的python脚本，存储是基于github的源接口
- 自动化使用的是github action

## 关于hexo使用

**环境**

- node-v12
- hexo插件

**命令**

```
npm install # 安装库

hexo g 生成静态文件到public文件夹
hexo s 启用本地local服务端
```



关键是一些配置如何管理，可以参考[blog](https://godweiyang.com/2018/04/13/hexo-blog/)



## 关于图源管理

具体参考以前的仓库

[MDing 图源](https://github.com/kengerlwl/MDimg)



## 关于github action

- 当每次更新仓库后，会自动将`copyMD`文件夹下面的所有文件重新打包上传到另一个分支里面

