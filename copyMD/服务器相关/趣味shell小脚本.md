---
title: 趣味shell小脚本，防卷
top: false
cover: false
toc: true
mathjax: true
date: 2020-01-15 15:27:31
password:
summary:
tags:
- 服务器
categories:
- 服务器
---

# 监控哪些人在服务器卷小脚步

```
#coding=gbk
import os, re
import requests
import time

# 要留下就返回true
def is_none(s):
    if s:
        return True
    else:
        return False


# execute command, and return the output
def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text


def send_msg(msg):
    # url = 'http://110.40.204.239:5700/send_group_msg?group_id={}&message={}'.format(
    #     '590020444',
    #     msg
    # )

    url = 'http://127.0.0.1:5700/send_private_msg?user_id={}&message={}'.format(
        '2892211452',
        msg
    )
    print(msg)
    requests.get(url)
    pass



if __name__ == '__main__':
    listen_username = 'testuser'
    cmd = "w | grep {}".format(listen_username)
    online_users = {}
    while True:

        result = execCmd(cmd)
        print(result)
        result = result.split('\n')
        online_tty = {}
        all_msgs = ""
        for i in result:

            try:
                # 字符串划分
                i = list(filter(is_none, i.split(' ')))
                print(i)
                username = i[0]
                id = i[1]
                online_tty[id] = 1
                date = i[3]

                # 不在，通知并且添加到在线用户
                if id not in online_users:
                    online_users[id] = {
                        "username":username,
                        "date":date
                    }
                    all_msgs = all_msgs + "{} 于 {} 登录了服务器\n".format(username, date)
                else: # 如果id一样，但是用户不一样了，代表也是有新用户登录了
                    if username != online_users[id]['username']:
                        online_users[id] = {
                            "username": username,
                            "date": date
                        }
                        all_msgs = all_msgs + "{} 于 {} 登录了服务器\n".format(username, date)
            except Exception as e:
                print(e)

        if all_msgs:
            send_msg(all_msgs)


        # 清理掉不在线的终端
        del_key = []
        for key in online_users:
            if key not in online_tty:
                print("{} 终端已经下线".format(online_users[key]))
                del_key.append(key)
        for key in del_key:
            online_users.__delitem__(key)
        print(online_users)
        time.sleep(5)
```



## 防卷v2

```
#coding=utf-8
#coding=gbk
import os, re
import requests
import time

# 要留下就返回true
def is_none(s):
    if s:
        return True
    else:
        return False


# execute command, and return the output
def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text


def send_msg(msg):
    # url = 'http://110.40.204.239:5700/send_group_msg?group_id={}&message={}'.format(
    #     '590020444',
    #     msg
    # )

    url = 'http://110.40.204.239:5700/send_private_msg?user_id={}&message={}'.format(
        '2892211452',
        msg
    )
    rsp = requests.get(url)
    print("发送消息结果" + rsp.text)



if __name__ == '__main__':
    all_listen_username = {"lwl"}
    online_users = {}
    while True:

        # 针对每一个用户都进行检测
        for listen_username in all_listen_username:
            cmd = "w | grep {}".format(listen_username)
            result = execCmd(cmd)
            # print(result)
            result = result.split('\n')
            online_tty = {} # 当前在线终端
            all_msgs = ""
            for i in result:

                try:
                    # 字符串划分
                    i = list(filter(is_none, i.split(' ')))
                    # print(i)
                    username = i[0]
                    id = i[1]
                    
                    date = i[3]

                    # 用人和时间做key值
                    key = date + " " + username

                    online_tty[key] = 1
                    
                    # 剔除掉非目标用户
                    if username != listen_username:
                        continue

                    # 不在，通知并且添加到在线用户
                    if key not in online_users:
                        online_users[key] = {
                            "username":username,
                            "date":date
                        }
                        all_msgs = all_msgs + "{} 于 {} 登录了服务器\n".format(username, date)
    
                except Exception as e:
                    print(e)

        if all_msgs:
            send_msg(all_msgs)


        # 清理掉不在线的终端
        del_key = []
        for user_key in online_users:
            if user_key not in online_tty:
                print("{} 终端已经下线".format(online_users[user_key]))
                del_key.append(user_key)
        for user_key in del_key:
            online_users.__delitem__(user_key)
            del_msg = "{} 用户已经下线".format(user_key)
            send_msg(del_msg)
        # print(online_users)
        time.sleep(5)
```





# 自动下线小脚本

自动下线指定用户的终端，**一经发现，直接下线**

```
username=M1ld
while(true)
do
	sleep(500);
	who | grep $username | awk -F ' ' '{print $2}' | xargs  pkill -kill -t 
done;
```





# 输出带颜色的字体

```
s=fuck
echo -e "\033[00;41m$s\033[0m"
```



## 输出文字到其他在线终端

```
[testuser@reg ~]$ w
 16:21:27 up 125 days,  5:46,  5 users,  load average: 0.11, 0.06, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
fang     pts/25   202.197.34.34    08:17    1:08m  0.01s  0.00s tmux attach -t
csuerlk  pts/27   202.197.33.133   日21   18:07m  0.05s  0.05s -bash
testuser pts/60   202.197.33.131   14:34    1:30   0.10s  0.00s sshd: testuser
wxh      pts/61   119.39.65.148    15:37   36:39   0.01s  0.01s -bash
testuser pts/62   202.197.33.217   16:18    6.00s  0.02s  0.00s w

命令
s=我建议你下线
echo -e "\033[00;41m$s\033[0m"  > /dev/pts/60
```



# 恐吓萌新的代码

```
#!/bin/bash

echo -e "\033[31m检测到您的电脑正在运行高危脚本，10s后将会自动关机。\033[0m"

countdown=10
while [ $countdown -gt 0 ]
do
    echo -e "\033[31m$countdown\033[0m"
    sleep 1
    countdown=$((countdown - 1))
done

echo -e "\033[31m关机ing...\033[0m"
```

运行

```
bash test.sh > /dev/pts/$num
```

