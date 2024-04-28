---
title: ldap服务搭建
top: false
cover: false
toc: true
mathjax: true
date: 2023-05-05 15:27:31
password:
summary:
tags:
- ldap
- linux
- docker
categories:
- 服务器

---

# 需求

需要一套ldap服务来将我的各种平台实现统一登录以及管理



# 方案

- docker安装好openldap

- docker安装管理界面，

  - **ldapaccountmanager/lam**

    \- 该管理界面的初始密码是lam



# 方法

### 1安装好容器

前往[docker容器](https://github.com/kengerlwl/docker_demo)





本地测试命令

```
ldapsearch -x -H ldap://hw.ldap.kenger.work:389 -b dc=kenger,dc=work -D "cn=admin,dc=kenger,dc=work" -w your_passwd
```







# 2 web页面基本配置



前往服务器页面配置

![image-20230626233101033](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/50413a0d020bf2ec31e1ff8e5c463589/59bd63e7605b973abe66b1209401a73b.png)





![image-20230626233035756](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/50413a0d020bf2ec31e1ff8e5c463589/680fc6ee17c166b4ae3cc1a6e7e0b95c.png)

**继续下滑修改**

![image-20230626233156075](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/50413a0d020bf2ec31e1ff8e5c463589/cce3cbf73acd1999e7e683af1c832d17.png)



**前往账户类型进行修改**

修改dc，dc两个字段即可

![image-20230626233247131](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/50413a0d020bf2ec31e1ff8e5c463589/da9873c4ec0a5deadba86089ddfd7bfb.png)



修改

![image-20230626233303282](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/50413a0d020bf2ec31e1ff8e5c463589/49bd92d30799062fa3aa8be295ce8a51.png)



前往模块设置

![image-20230626233330414](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/50413a0d020bf2ec31e1ff8e5c463589/ed21d419b0228617b3db884c98460e22.png)

设置用户和组的id范围以及一些基础设置

![image-20230626233411088](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/50413a0d020bf2ec31e1ff8e5c463589/3ea199e8b6d6eb53cbe44ed360cf086e.png)









# 坑

- 我的服务器host dns解析有问题，我手机编辑，然后吧默认的docker网关设置为ldap服务器
- 

