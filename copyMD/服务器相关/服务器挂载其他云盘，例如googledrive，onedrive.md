---
title: 服务器挂载其他云盘，例如googledrive，onedrive
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- 服务器
- 挂载
categories:
- 服务器
---
# 服务器可以挂载很多云网盘

**用到的工具Rclone**

可以支持很多的云盘，不仅仅是google，还有onedrive等。



# 安装相关库

```
curl https://rclone.org/install.sh | sudo bash


yum install fuse
```



# 用rclone登录云盘配置

```
rclone config
```

out

```
2020/03/04 17:17:28 NOTICE: Config file "/root/.config/rclone/rclone.conf" not found - using defaults
No remotes found - make a new one
n) New remote
s) Set configuration password
q) Quit config
```

选择n，建立新的远程连接

然后输入名字。这个可以随便自己填。

然后有：

![refs/heads/master/image-20220831231450455](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/ddc552e2fb60427a31c6b3d28ba21944/69b94b1ad4cfc3d4acb3f2f4f190bf2a.png)

**对于这个id以及secret，输入enter跳过就行。**



然后要选择Rclone对Google Drive网盘文件的操作权限：选择1

```
Option scope.
Scope that rclone should use when requesting access from drive.
Enter a string value. Press Enter for the default ("").
Choose a number from below, or type in your own value.
 1 / Full access all files, excluding Application Data Folder.
   \ "drive"
 2 / Read-only access to file metadata and file contents.
   \ "drive.readonly"
   / Access to files created by rclone only.
 3 | These are visible in the drive website.
   | File authorization is revoked when the user deauthorizes the app.
   \ "drive.file"
   / Allows read and write access to the Application Data folder.
 4 | This is not visible in the drive website.
   \ "drive.appfolder"
   / Allows read-only access to file metadata but
 5 | does not allow any access to read or download file content.
   \ "drive.metadata.readonly"
scope> 1

```

然后是一些设置

```
# 一
Edit advanced config?
y) Yes
n) No (default)
y/n> n

# 二
Use auto config?
 * Say Y if not sure
 * Say N if you are working on a remote or headless machine

y) Yes (default)
n) No
y/n> n


```



**关键；然后会出现一个需要到网页登录验证的连接。用nginx做跨越访问代理到公网。**

```
2022/08/31 23:17:42 NOTICE: If your browser doesn't open automatically go to the following link: http://127.0.0.1:53682/auth?state=-y3AQQerN0TGxaYaTe7TIQ
2022/08/31 23:17:42 NOTICE: Log in and authorize rclone for access
2022/08/31 23:17:42 NOTICE: Waiting for code...
```

对于http://127.0.0.1:53682/auth?state=-y3AQQerN0TGxaYaTe7TIQ 代理到公网访问登录。



后面会出现一些设置选项，基本选择yes。然后可以退出了。



# 挂载

```
rclone mount GoogleDrive: /google --allow-other --allow-non-empty --vfs-cache-mode writes
```

解释：

**rclone mount 我之前输入的云盘名字: 本地被挂载的路径--allow-other --allow-non-empty --vfs-cache-mode writes**



挂载onedrive

```
rclone mount one_drive_test1: /onedrive --allow-other --allow-non-empty --vfs-cache-mode writes
```





# 查看

```
df -h
```

![refs/heads/master/image-20220831232119105](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/ddc552e2fb60427a31c6b3d28ba21944/750110b64a59b0a23bc6cf808c7f6e1a.png)



可以正常访问。





# 关于挂载onedrive云盘。

我这里用的是从pdd上买的5T永久免费盘。
基本流程和上面是一致的，但是要注意：
- 这个要选择第一个

- ![refs/heads/master/image-20220917175707801](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/ddc552e2fb60427a31c6b3d28ba21944/4efac40a129a35d631dd81cb33b5acb3.png)

  



# ref

https://www.unvone.com/69270.html

https://333rd.net/posts/tech/linux%E4%BD%BF%E7%94%A8rclone%E6%8C%82%E8%BD%BDgoogle-drive%E7%BD%91%E7%9B%98/