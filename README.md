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





## 基于jsDelivr来对github的静态资源做静态加速

使用方法：[https://cdn.jsdelivr.net/gh/](https://link.zhihu.com/?target=https%3A//cdn.jsdelivr.net/gh/)你的用户名/你的仓库名@发布的版本号/文件路径

例如：

```text
https://cdn.jsdelivr.net/gh/TRHX/CDN-for-itrhx.com@1.0/images/trhx.png
https://cdn.jsdelivr.net/gh/TRHX/CDN-for-itrhx.com@2.0.1/css/style.css  
https://cdn.jsdelivr.net/gh/moezx/cdn@3.1.3//The%20Pet%20Girl%20of%20Sakurasou.mp4
```

注意：版本号不是必需的，是为了区分新旧资源，如果不使用版本号，将会直接引用最新资源，除此之外还可以使用某个范围内的版本，查看所有资源等，具体使用方法如下：

```text
// 加载任何Github发布、提交或分支
https://cdn.jsdelivr.net/gh/user/repo@version/file

// 加载 jQuery v3.2.1
https://cdn.jsdelivr.net/gh/jquery/jquery@3.2.1/dist/jquery.min.js

// 使用版本范围而不是特定版本
https://cdn.jsdelivr.net/gh/jquery/jquery@3.2/dist/jquery.min.js   https://cdn.jsdelivr.net/gh/jquery/jquery@3/dist/jquery.min.js
 
// 完全省略该版本以获取最新版本
https://cdn.jsdelivr.net/gh/jquery/jquery/dist/jquery.min.js
 
// 将“.min”添加到任何JS/CSS文件中以获取缩小版本，如果不存在，将为会自动生成
https://cdn.jsdelivr.net/gh/jquery/jquery@3.2.1/src/core.min.js
 
// 在末尾添加 / 以获取资源目录列表
https://cdn.jsdelivr.net/gh/jquery/jquery/
```
