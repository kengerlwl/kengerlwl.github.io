---
title: python里的线程安全问题
top: false
cover: false
toc: true
mathjax: true
date: 2023-08-08 15:27:31
password:
summary:
tags:
- 线程安全
- 消息队列
categories:
- 技术
---



# 背景

需要**实现一个flask里面的消息队列后台执行的功能**，但是不想用第三方库。

原理是基于内存的消息队列



查阅资料看到了使用线程安全的queue.Queue来实现这个功能。使用后台线程来监听。





## 线程安全

背景：

一个进程里面所有线程是共享资源的，那么也就是说，存在一个公共的内存变量区域，可以被所欲的线程都访问到，如果



线程安全是一个计算机编程术语，用于描述多线程环境下，**程序或系统能够在多个线程同时访问共享资源时保持正确性、一致性和可预测性的性质。**在一个多线程的程序中，如果没有适当的同步机制，多个线程可能会同时访问、修改相同的数据，导致竞争条件和不确定性结果。

线程安全的概念包括以下几个方面：

1. **原子性（Atomicity）：** 一个操作被称为“原子操作”时，它在执行时不会被其他线程中断。这意味着操作要么完全执行，要么不执行，没有中间状态。线程安全的程序使用原子操作来确保多个线程在访问共享资源时不会破坏数据的完整性。

2. **可见性（Visibility）：** 当一个线程修改了共享资源的状态时，其他线程应该能够立即看到这种变化。线程安全的机制确保了数据更新在多线程环境下的可见性。

3. **有序性（Ordering）：** 确保多个线程的操作按照某种规则进行排序，以防止指令重排等导致的问题。

4. **竞争条件（Race Conditions）：** 竞争条件是指当多个线程对共享资源进行读写操作时，操作的顺序和时间不确定，从而可能导致意外的结果。线程安全的设计可以避免竞争条件。

5. **同步机制（Synchronization）：** 线程安全的程序使用同步机制来协调多个线程的操作，以确保数据的一致性。常见的同步机制包括锁（Locks）、信号量（Semaphores）、条件变量（Condition Variables）等。

总之，线程安全是一种编程目标，旨在确保在多线程环境中，程序能够正确地处理共享资源，避免竞争条件和数据不一致性问题，从而提供可靠的结果和可预测的行为。







# 原理

想要实现原子操作，一个办法是使用🔐机制。通过锁，将贡献的变量实现原子操作，让读和写等操作不可以被多线程同时执行。



另一个办法是使用线程安全的数据结构，这个无论是在java和python里面都有相应的数据结构。

案例如下：

```
import threading
from flask import Flask, request
import time
import queue
# from flask import current_app as app

app = Flask(__name__)
app.message_queue_id = 0
lock = threading.Lock() # 由于本文唯一需要线程共享的变量已经是线程安全的了，所以就不用锁了。

message_queue = queue.Queue()


def calculate_blocking(blcking_time):
    start_time = time.time()
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= blcking_time:
            break
        # 进行计算操作，可以是任何需要一定时间的任务
        # 请注意，这里的计算操作可能会消耗大量的 CPU 资源
        # 以便更好地模拟计算阻塞的效果
        result = 0
        for i in range(1000):
            result += i
    return result


def process_messages():
    thread_id = threading.get_ident()

    while True:
        try:
            
            # 当系统不知道当前的message_queue_id时，等待1s。并且不删除线程
            if app.message_queue_id == 0:
                print("message queue id is not init, so wait")
                time.sleep(1)
                continue
            
            # 如果不是目标线程，删除
            if thread_id != app.message_queue_id:
                print("current thread id {}".format(thread_id))
                print("thread id is not equal to message queue id， so exit")
                return

            messages = list(message_queue.queue)
            calculate_blocking(5)
            print("all  message is:", messages)
        except Exception as e:
            print(e)


# 查看所有子线程
@app.route('/thread', methods=['GET'])
def get_thread():
        # 查看所有子线程
    all_threads = threading.enumerate()
    for thread in all_threads:
        print("thread id {}".format(thread))
    return "all threads {}".format(all_threads)


@app.route('/produce/<message>', methods=['GET'])
def enqueue_message(message):

    message_queue.put(message)
    return "message produce {}".format(message)


def start_message_thread():
    # 启动一个线程来处理消息
    message_thread = threading.Thread(target=process_messages)

    message_thread.daemon = True # 设置为守护线程，当主线程结束，它也结束
    message_thread.start()

    #  这个变量也是线程安全的，只有这里有写入，其他地方都只有读取
    app.message_queue_id = message_thread.ident
    print("message thread start, id is {}".format(app.message_queue_id))


if __name__ == '__main__':
    start_message_thread()
    app.run(port = 50001,debug=True)

```





# 附录

## python里面使用rabbitmq的例子

```
from flask import Flask, request, jsonify
import pika
import json
import threading
import Kit
from Config import *

app = Flask(__name__)




# 发送消息到RabbitMQ队列
def send_to_queue(message):
    conf = get_config()
    connection = Kit.rabbitmq_conn(conf, "rabbitmq")
    channel = connection.channel()
    channel.queue_declare(queue='my_queue')  # 声明队列
    channel.basic_publish(exchange='', routing_key='my_queue', body=message)
    connection.close()

# 处理从队列接收到的消息
def process_queue_message(ch, method, properties, body):
    """
    处理从队列接收到的消息的回调函数
    :param ch: pika.Channel 表示与 RabbitMQ 之间的连接通道，可用于执行消息操作。
    :param method: pika.spec.Basic.Deliver 包含有关传递消息的方法信息，如交换机、路由键等。
    :param properties: pika.spec.BasicProperties 包含消息的属性，这些属性可以是用户自定义的或者是 RabbitMQ 本身定义的。
    :param body: bytes 实际的消息内容，以字节序列的形式传递。
    :return: None
    """
    print("Received message:", body)
    # 在这里你可以执行你需要的任务，例如数据库操作、计算等


@app.route('/send_message/<message>', methods=['GET'])
def send_message(message):
    
    send_to_queue(message)
    return jsonify({"message": "Message sent to queue successfully"})

if __name__ == '__main__':
    # 启动Flask应用
    thread = threading.Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 50001})
    thread.start()

    # 启动消息处理者
    conf = get_config()
    connection = Kit.rabbitmq_conn(conf, "rabbitmq")
    channel = connection.channel()
    channel.queue_declare(queue='my_queue')
    channel.basic_consume(queue='my_queue', on_message_callback=process_queue_message, auto_ack=True)
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

```

