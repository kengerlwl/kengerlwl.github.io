---
title: 程序辅助工程Prompt
top: false
cover: false
toc: true
mathjax: true
date: 2023-06-8 15:27:31
password:
summary:
tags:
- chatgpt
categories:
- 综合
---

# TMP草稿区

```
假设你是一个资深的python程序员，接下来我有一些问题问你，请你辅助回答我，理解请回复收到。
```



````

````



````
请你针对下面的函数帮我做出修改，具体修改如下：

````





# 身份

```
假设你是一个资深的python程序员，接下来我有一些问题问你，请你辅助回答我，理解请回复收到。
```







## 代码摘要解释代码

很多时候有些代码懒得阅读，又没有注释，直接甩给chatgpt，问问他有什么想法

````
请问下面这段代码是什么意思，代码内容在下文```代码块内：
```
xxx
```

要求：
1. 总体的说明这段代码的目标是实现什么功能
2. 对代码中的部分函数以及一些关键性的点做出点评
````





# 实现配置脱敏

实际开发中我们经常要配置大量配置文件，其中生产环境文件是本地的，案例文件是可以放到云端作为参考的，但是案例文件需要进行脱敏，同时又包含原有的命名格式。所以需要一个脱敏工具

````
请你帮我实现下面json配置文件的脱敏工作，具体配置文件在下文```块内。
```
{
  "secrets":{
      "token":"xxx"
  },
  "email": {
      "smtpserver": "smtp.163.com",
      "user": "293487943@163.com",
      "password": "23487293"
  },
  "proxy":{
      "proxy_server":"123123",
      "proxy_port":234234
  }
}
```
要求：
1. 保留原有的json配置文件结构
2. 保留原有的文件类型，例如原来是字符串，那就还是字符串"xxx"，原来是数字，那就变为123
3. 对于部分特殊的字符串，例如上文中的邮件，要在替换特定的名称以及后缀名后，仍然保持邮件的特征

请直接输出脱敏后的json文件
````





## 完善代码

写到一半不想写了，但是如果直接提功能chatgpt又不一定能完成，那么选择写一半，并且写好关键IO信息。同时写好程序逻辑也许能有用

````
请你帮我完善下面代码，代码内容在下文```代码块内：
```
class User:
    """
    User类
    含有以下json的属性：
    例如：user_json: {
      "name": "VWANtest",
      "eth_name":"VTH0",
      "username": "224712284",
      "password": "xxxxx",
      "type": "cmccn",
      "local_ip": "192.168.31.219"
    }
    以及
    wan_name： 等于WAN_xx(xx是eth_name), 例如WAN_VTH0
    members_name: 等于xx(xx是wan_name)_M1_W1，例如：WAN_VTH0_M1_W1

    要求，该类题型一个初始化函数，传入json数据，然后自动生成相关属性的值
    """
    def __init__(self) -> None:
        pass

```

要求:
1. 按照代码里面提到的注释实现相关功能。
2. 尽量保证原有的大方向架构不要变
````









# T2C代码生成（一个非常成功的案例）

尝试1：直接把目标甩给他，然后在代码里面标注一下要更改的地方。没用

尝试2：尝试利用思维链的方式，让程序先找到xxx模块，然后匹配是否含有wan属性，然后修改network属性。成功！



````
请你帮我完成一个python程序，修改下文```块中的一个配置。具体修改地方我会在代码中标注。

```
config zone
        option name 'lan'
        option input 'ACCEPT'
        option output 'ACCEPT'
        option forward 'ACCEPT'
        option network 'lan'

config zone
        option name 'wan'  # 仅在name属性为wan的zone模块，才修改network属性
        option input 'REJECT'
        option output 'ACCEPT'
        option forward 'REJECT'
        option masq '1'
        option mtu_fix '1'
        option network 'wan wan6 WAN1 school_wan WAN_VTH0' # 可以修改该属性''内的值
```

你应该遵循如下思路：
1. 先找到option name 为`wan`的指定模块
2. 然后在该模块内查找option network属性，修改``的内容为xxx
3. 写入文件
4. 读取的配置文件叫做`./firewall`
5. 请用函数封装一下

````





mwan配置读取编写。**success**

````
请你帮我完成一个python程序，读取解析下文```块中的一个配置。
```
config globals 'globals'
  option mmx_mask '0x3F00'
  option rtmon_interval '5'


config interface 'WAN_TEMPLATE'
  option check_quality '0'
  option count '1'
  option down '3'
  option enabled '1'
  option failure_interval '5'
  option family 'ipv4'
  option flush_conntrack 'never'
  option initial_state 'online'
  option interval '5'
  option recovery_interval '5'
  option reliability '1'
  option size '56'
  option timeout '2'
  list track_ip 'baidu.com'
  option track_method 'ping'
  option up '3'

config member 'WAN_TEMPLATE_M1_W1'
  option interface 'WAN_TEMPLATE'
  option metric '1'
  option weight '3'

config member 'WAN_VTH0_M1_W1'
  option interface 'WAN_VTH0'
  option metric '1'
  option weight '3'

config policy 'BALANCE'
  option last_resort 'unreachable'
  list use_member 'wan_m1_w3 WAN_VTH0_M1_W1'

config rule 'default_rule'
  option dest_ip '0.0.0.0/0'
  option use_policy 'balanced'

config interface 'WAN_VTH0'
  option check_quality '0'
  option count '1'
  option down '3'
  option enabled '1'
  option failure_interval '5'
  option family 'ipv4'
  option flush_conntrack 'never'
  option initial_state 'online'
  option interval '5'
  option recovery_interval '5'
  option reliability '1'
  option size '56'
  option timeout '2'
  list track_ip 'baidu.com'
  option track_method 'ping'
  option up '3'


```

要求，
1. config总共分为rule,interface,member,globals,policy...几类 (用省略号是因为有可能有更多种类，chatgpt对`等`这个词不敏感)
2. 按照分类读取为一个map，这个map有前面收集到的类别作为keys。
3. 每个keys下面还有一个map，这个map以该类别里面的名字作为key。例如`rule类别就有https,default_rule等keys`
3.1 注意，之所以用map作为结构，是因为interface, member,policy, rule等类别们可以有多个实体，每个实体的名字作为key区分。
4. option代表的是该实体的可选属性，例如属性proto为tcp类似。
4.1 list代表的是该实体的list相关属性，例如，list属性member key为wan_m1_w3 xxx。共两个值，是一个列表
4.2 list属性读取的时候，单引号字符'也算作字符了，实际上这应该不算
5. 读取的配置文件叫做./mwan3
6. 请实现读取配置文件为json，以及将json写为配置文件的功能。
7. 请以函数封装好上述功能


你应该遵循的步骤逻辑是：
1. 把每个类别识别出来
2. 针对每个类别的所有不同属性分别存储到map
3. 同样的逻辑写入到文件
````

