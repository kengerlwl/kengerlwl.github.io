---
title: 使用iptables实现负载均衡
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- openwrt
- iptable
- 负载均衡
categories:
- 网络
---

# 背景

mwan太傻逼了。受不了

使用iptables尝试实现一下。

# 架构

两个部分

第一部分是均匀的给流量打mark标记。

第二部分是根据打的流量分别走不同的路由表







##  两条链打标记

WAN1数据标记：

（这里的WAN1是在mangle表中的链的名字，可以自行命名）

```
iptables -t mangle -N WAN1
iptables -t mangle -A WAN1 -j MARK --set-mark 1
#标记数据包
iptables -t mangle -A WAN1 -j CONNMARK --save-mark
#把数据包中的mark设置到整个连接中
```

WAN2数据标记：

```
iptables -t mangle -N WAN2
iptables -t mangle -A WAN2 -j MARK --set-mark 2
iptables -t mangle -A WAN2 -j CONNMARK --save-mark
```

把已存在连接中的mark设置到数据包中：

```
iptables -t mangle -N RESTORE
iptables -t mangle -A RESTORE -j CONNMARK --restore-mark
iptables -t mangle -A PREROUTING -m conntrack --ctstate ESTABLISHED,RELATED -j RESTORE

```



## 分发数据包

使用[NTH](http://www.haiyun.me/tag/nth)模块公平分发新数据包到WAN1和WAN2：

```
iptables -t mangle -A PREROUTING -m conntrack --ctstate NEW -m statistic --mode nth --every 2 --packet 0 -j WAN1
iptables -t mangle -A PREROUTING -m conntrack --ctstate NEW -m statistic --mode nth --every 2 --packet 1 -j WAN2


-A PREROUTING：将规则附加到 PREROUTING 链中。PREROUTING 链用于在数据包到达系统之前对它们进行处理。
-m conntrack --ctstate NEW：这是一个条件匹配，用于检查数据包的连接状态是否为 NEW。NEW 表示这是一个新的连接或会话请求数据包。这个条件通常用于限制规则只应用于新的连接请求。
--every 2：每第 2 个数据包匹配这个规则，即一个规则匹配一个数据包，然后跳过一个数据包。
--packet 0：这是规则的索引，表示这个规则适用于每第 2 个数据包中的第一个数据包。如果索引为 0，表示匹配第一个数据包。
-j WAN1 对应的是相应的第几个数据包走哪个链
```

## 不同标记走不同路由表

设置路由表：

```
cat /etc/iproute2/rt_tables
#http://www.haiyun.me
255    local
254    main
253    default
0    unspec
252 wan1
251 wan2
```

设置路由表默认路由：

```
以wan1为例
root@OpenWrt:~# ip route show table wan1



default via 183.169.79.254 dev vth1
10.20.0.0/16 dev eth0 proto kernel scope link src 10.20.20.22 #这个是与lan口的通信，不然就会不通
183.169.64.0/20 dev vth1 proto kernel scope link src 183.169.68.19


```

根据iptables标记应用路由：

```
ip rule del from all fwmark 2 2>/dev/null  # fwmark 2代表标记为2的数据包
ip rule del from all fwmark 1 2>/dev/null
ip rule add fwmark 1 table wan1
ip rule add fwmark 2 table wan2
ip route flush cache
```





最后禁用源地址验证：

```
cat /etc/sysctl.conf
net.ipv4.conf.default.rp_filter = 0
```

# 实践

成功。

校园网一共5个wan口，每个限速20mbps。

聚合后。

![image-20230923222820553](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/master/image/d9a3a496f237da2003ac56f66c87928a/a688cb7bcb73473e4da3b14d18f9853e.png)



## 设计

我这里wan的名字和路由表的名字默认一样。

假设有一个lan

### 打标记与分发

```
#!/bin/bash

# 设置循环次数
count=5

# 循环计数变量
i=1

# 循环开始
while [ $i -le $count ]; do
    # 构建变量名
    mangleChain_name="wan${i}_chain"
    wan_name="wan${i}"
    eth_name="vth$i"
    gateway="183.169.79.254"

	
	# 新增打标记的链
    iptables -t mangle -N $mangleChain_name
    iptables -t mangle -A $mangleChain_name -j MARK --set-mark $i
    #标记数据包
    iptables -t mangle -A $mangleChain_name -j CONNMARK --save-mark
    #把数据包中的mark设置到整个连接中


    # 打印变量值
    echo "wan_name: $wan_name"
    

    # 增加计数
    i=$((i + 1))
done


# 存储标记值
iptables -t mangle -N RESTORE
iptables -t mangle -A RESTORE -j CONNMARK --restore-mark
iptables -t mangle -A PREROUTING -m conntrack --ctstate ESTABLISHED,RELATED -j RESTORE


i=1
# 循环开始
while [ $i -le $count ]; do
    # 构建变量名
    mangleChain_name="wan${i}_chain"
    wan_name="wan${i}"
    eth_name="vth$i"
    gateway="183.169.79.254"

    # 均分分发
    iptables -t mangle -A PREROUTING -m conntrack --ctstate NEW -m statistic --mode nth --every $count --packet $((i - 1)) -j $mangleChain_name

    
    # 打印变量值
    echo "wan_name: $wan_name"
    

    # 增加计数
    i=$((i + 1))
done
```



**要删除 mangle 表格中 PREROUTING 链上的所有规则，您可以使用以下命令：**

```
iptables -t mangle -F PREROUTING
```




### 初始化路由表
```
# !/bin/bash
i=1


while [ $i -lt 6 ]; do


    wan_name="wan$i"
    eth_name="vth$i"
	lan_route_ip="10.20.20.22" # lan的路由器ip
	lan_ip="10.20.0.0/16" # lan的范围ip
    gateway="183.169.79.254"

    # 删除该表
    ip route flush table $wan_name


    wan_ip=$(ip -4 -br addr show dev $eth_name | awk '{split($3,a,"/"); print a[1]}')
    ip rule add from all iif $eth_name lookup $wan_name
    ip route add default via $gateway dev $eth_name table $wan_name
    ip route add $lan_ip dev eth0 proto kernel scope link src $lan_route_ip table $wan_name
    ip route add 183.169.64.0/20 dev $eth_name proto kernel scope link src $wan_ip table $wan_name
    
    echo $wan_ip
    echo #wan_name

  i=$((i + 1))
done

```




### 标记转发到路由表

```

#!/bin/bash

# 设置循环次数
count=5

# 循环计数变量
i=1

# 循环开始
while [ $i -le $count ]; do
    # 构建变量名
    mangleChain_name="wan${i}_chain"
    wan_name="wan${i}"  # wan的名字就是表的名字
    eth_name="vth$i"
    gateway="183.169.79.254"

	# 将指定数据包发送到指定路由表
    ip rule del from all fwmark $i 2>/dev/null
    ip rule add fwmark $i table $wan_name
    
    
    # 打印变量值
    echo "wan_name: $wan_name"
    

    # 增加计数
    i=$((i + 1))
done

ip route flush cache
```



三个部分依次执行

# ref

[[OpenWRT/Linux多WAN带宽叠加使用iptables标记策略路由负载均衡](https://www.haiyun.me/archives/iptables-nth-mark-route-load.html)]
