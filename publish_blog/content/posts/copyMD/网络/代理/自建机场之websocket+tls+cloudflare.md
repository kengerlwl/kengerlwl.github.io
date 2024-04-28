---
title: 自建机场之websocket+tls+cloudflare
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- 机场
- 代理
categories:
- 代理
---

# 介绍

## 工具

- v2ray，功能强大的请求转发工具（优秀的代理工具）

- cloudflare：一个不错的cdn白嫖网站，同时也能够用来做一些dns管理。关键是免费加强大
- racknerk：我的vps购买网站，一个垃圾vps，美国的



## 思路

想要翻越GFW，那么需要有一个境外的服务器，这个服务器能够代理我们的请求，从而访问国外的资源。此外，该服务器还要能够与国内相同，也就是说不在GFW黑名单内。





# 思路

先去买一个域名。

我是用的**namesilo**，一个全球知名的域名购买网站。



## 先将域名的dns删除

如图，我的域名是`kenger.top`

![image-20230212001120974](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/631677d165f07cf277602467d7c9d208.png)

![image-20230212001750936](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/148bef1878a96f0ad50f9c3146690689.png)





## 更改域名的DNS的NS值

NS值，也就是指**nameserver**，域名解析服务器。即DNS服务

进入cloudflare，新增站点

![image-20230212001827761](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/a67e5e4209da493b67ab68151cc79ff6.png)



可以看到上图出现了**两个NS值**。

这个就是cloudflare提供给我们的免费dns服务。把这两个贴到namesilo的相应位置。

## 填入NS值

![image-20230212002056139](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/3d18f0fc84409391c6a5ae604be1857b.png)

然后提交**submit**



## 新增DNS解析记录

如图。

![image-20230212002239985](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/eeceb42e0a3f979ef456d15556aec71e.png)

## 关于cloudflare的CDN代理说明

CDN实际上就是再帮我们的服务器做一次反向代理。

如图，当我们访问`v.kenger.top`时，实际上是先访问cloudflare的服务器，然后cloudflare去访问我们的目标服务器。**优点是非常的安全**

![image-20230212002331566](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/dae299b69528febbfd9ba822f2d7ae90.png)





## 设置SSL

这里最好设置成这个，选择灵活的话，好像访问次数多了，会自动判定访问http。

![image-20230212002502214](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/be5ea4f2f6b73a27e67c543062ab0085.png)









# v2ray+websocker+tls设置

## 工具

- 我用到了宝塔面板的nginx，从而实现tls
- v2ray里面设置了websocket。
- 最好再加上一个网页，以假乱真，搞得像我们真的在访问一个网站。



## v2ray

我用的docker

```
{
  "log": {
    "loglevel": "info"
  },
  "inbounds": [
    {
      "listen": "0.0.0.0",
      "port": 52333,
      "protocol": "vmess",
      "settings": {
        "clients": [
          {
            "id": "8FF6627C-C247-44EB-A9AA-A7EAB8385D4A",
            "alterId": 0,
            "security": "auto"
          }
        ]
      },
      "streamSettings": {     // 载体配置段，设置为websocket
      "network": "ws",
      "wsSettings": {
        "path": "/vpath"  // 与nginx中的路径保持一致
      }
      
    }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom",
      "settings": {},
      "tag": "proxy"
    }
  ]
}
```

```
sudo docker run -it --name v2ray -v $PWD/v2ray/config.json:/etc/v2ray/config.json -p 52333:52333 v2fly/v2fly-core:v4.31.0 
```



## 宝塔nginx

![image-20230212002943126](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/1f73b282a0a1d91092581e7c6f0f523a.png)



### 开启ssl

用免费的就行

![image-20230212003148350](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/16bbf7acfcf511abea9dab049eb1666e.png)



### 配置nginx

关键是这段

```
  location /vpath {
      proxy_redirect off;
      proxy_pass http://127.0.0.1:52333;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
      proxy_set_header Host $host;
      # Show real IP in v2ray access.log
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```



![image-20230212003053921](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/7827842c01801cb2a5de3931b9358eef.png)



## 搭建伪装网站

在`v.kenger.top`上搭建了代理后，还需要在该域名上做一个伪装的网站。不然空访问一个index页面也很假。

就宝塔自带的nginx静态资源代理

![image-20230212183926877](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/75ef46423362d2abe08fc00f562fd960.png)

**将网站放入该文件夹下即可。**

效果

![image-20230212183956514](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/fc32c1779c3ae6bace7fde7dd64e61b6.png)



# 启动bbr加速内核

`wget -N --no-check-certificate "https://raw.githubusercontent.com/chiakge/Linux-NetSpeed/master/tcp.sh" && chmod +x tcp.sh && ./tcp.sh`

1. 先在[1 – 3]切换内核（第一次显示为bbr内核也要切换一遍），重启

有部分系统会出现下面的选项，移动光标选择no

![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/f7a1d604dfbcc7eceffa6a1fdd24235a.png)

2. 重启后输入

```
 ./tcp.sh
```



# 一些不知道的问题

- 不知道为什么，第一天搭建好后效果很差，又反复重新搭建了几次，突然又变还不错了。
- 延迟可能会很高，但是带宽好像还能跑起来。有点时好时坏的感觉。感觉是这么一种情况，突然用这个节点的话，会很慢，但是如果使用了几分钟后，速度就还行了，至少油管2k可以了。
- 可能我买的vps不行，虽然理论上有1gbps的带宽，但是和国内通信只能跑到很有限。反而在套上cloudflare后变快了。





# ref

https://sh.tmioe.com/772.html

https://www.triadprogram.com/v2ray-build-by-yourself/

https://www.winhow.top/archives/14/#Joe-8



# 附录



## clash配置

```
    - {name: my1, server: v.kenger.top, port: 443, type: vmess, uuid: 8FF6627C-C247-44EB-A9AA-A7EAB8385D4A, alterId: 0, cipher: auto, tls: true, network: ws, ws-opts: {path: vpath}}
```

**注意：clash延迟会很高，可能导致失败**



## v2ray填写

![2802654365](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/cf57b2981859559f5ce35c14818242a9/a55fc95b24d0dda05ce13eef52b43eba.png)



## 完整nginx文件

```
server
{
    listen 80;
		listen 443 ssl http2;
    server_name v.kenger.top;
    index index.php index.html index.htm default.php default.htm default.html;
    root /www/wwwroot/v.kenger.top;

    #SSL-START SSL相关配置，请勿删除或修改下一行带注释的404规则
    #error_page 404/404.html;
    #HTTP_TO_HTTPS_START
    if ($server_port !~ 443){
        rewrite ^(/.*)$ https://$host$1 permanent;
    }
    #HTTP_TO_HTTPS_END
    ssl_certificate    /www/server/panel/vhost/cert/v.kenger.top/fullchain.pem;
    ssl_certificate_key    /www/server/panel/vhost/cert/v.kenger.top/privkey.pem;
    ssl_protocols TLSv1.1 TLSv1.2 TLSv1.3;
    ssl_ciphers EECDH+CHACHA20:EECDH+CHACHA20-draft:EECDH+AES128:RSA+AES128:EECDH+AES256:RSA+AES256:EECDH+3DES:RSA+3DES:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    add_header Strict-Transport-Security "max-age=31536000";
    error_page 497  https://$host$request_uri;
		#SSL-END

    #ERROR-PAGE-START  错误页配置，可以注释、删除或修改
    #error_page 404 /404.html;
    #error_page 502 /502.html;
    #ERROR-PAGE-END

    #PHP-INFO-START  PHP引用配置，可以注释或修改
    include enable-php-00.conf;
    #PHP-INFO-END

    #REWRITE-START URL重写规则引用,修改后将导致面板设置的伪静态规则失效
    include /www/server/panel/vhost/rewrite/v.kenger.top.conf;
    #REWRITE-END

    #禁止访问的文件或目录
    location ~ ^/(\.user.ini|\.htaccess|\.git|\.env|\.svn|\.project|LICENSE|README.md)
    {
        return 404;
    }

    #一键申请SSL证书验证目录相关设置
    location ~ \.well-known{
        allow all;
    }

    #禁止在证书验证目录放入敏感文件
    if ( $uri ~ "^/\.well-known/.*\.(php|jsp|py|js|css|lua|ts|go|zip|tar\.gz|rar|7z|sql|bak)$" ) {
        return 403;
    }

    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
    {
        expires      30d;
        error_log /dev/null;
        access_log /dev/null;
    }

    location ~ .*\.(js|css)?$
    {
        expires      12h;
        error_log /dev/null;
        access_log /dev/null;
    }
    access_log  /www/wwwlogs/v.kenger.top.log;
    error_log  /www/wwwlogs/v.kenger.top.error.log;
    
    
  location /vpath {
      proxy_redirect off;
      proxy_pass http://127.0.0.1:52333;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
      proxy_set_header Host $host;
      # Show real IP in v2ray access.log
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

