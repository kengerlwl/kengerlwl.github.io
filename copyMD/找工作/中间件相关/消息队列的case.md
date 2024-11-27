



# python 使用kafuka，带确认机制（点对点）

为确保 Kafka 消息只被处理一次，可以使用**消息确认机制（ACKs）**来实现可靠的消息交付。在 Kafka 中，`acks` 是生产者的一项重要配置，可以控制消息被认为是成功写入的条件。

Kafka 提供了三种 `acks` 级别：
1. **acks=0**：生产者不会等待任何来自服务器的确认。这意味着消息会快速发出，但如果服务器没有收到消息，生产者不会知道。
2. **acks=1**：生产者会等待来自**领导者**分区的确认，表示消息已被成功接收。如果领导者分区失败，可能会丢失消息。
3. **acks=all**（或 `acks=-1`）：生产者会等待**所有复制副本**确认消息接收，这提供了最高的可靠性。

为了确保消息只被消费一次，可以通过开启**消费者的自动提交关闭**和**手动提交偏移量**来处理消费者的消息确认。

### Kafka Producer（生产者）带 `acks` 示例

```python
from kafka import KafkaProducer
import json

# 创建一个Kafka生产者，设置acks=all
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',  # 确保消息被所有副本确认
    retries=5    # 重试次数
)

# 发送消息到Kafka的主题
topic_name = 'test_topic'
message = {'key': 'value', 'number': 123}

future = producer.send(topic_name, value=message)

# 等待发送确认
result = future.get(timeout=10)  # 超时机制，确保有确认
print("消息已发送并确认:", result)

# 刷新确保所有消息被处理
producer.flush()
```

### Kafka Consumer（消费者）手动提交偏移量示例

在消费者端，关闭自动提交并使用手动提交来确保消息消费后才确认处理。

```python
from kafka import KafkaConsumer
import json

# 创建一个Kafka消费者，关闭自动提交
consumer = KafkaConsumer(
    'test_topic',
    bootstrap_servers='localhost:9092',
    enable_auto_commit=False,  # 关闭自动提交偏移量，这个其实就是消费者的ack
    auto_offset_reset='earliest',
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# 消费消息并手动提交偏移量
for message in consumer:
    print(f"收到消息: {message.value}")
    
    # 这里添加处理逻辑，例如保存到数据库，确保消息处理完成
    # 如果处理成功，手动提交偏移量
    consumer.commit()  # 手动提交偏移量

    print("偏移量已手动提交")
```

### 重要配置解读：
1. **acks='all'**: 在生产者端，配置了 `acks='all'`，确保所有副本接收到消息后才返回成功确认。这提供了最高的可靠性。
   
2. **enable_auto_commit=False**: 在消费者端，关闭自动偏移量提交，防止在处理消息之前就提交偏移量，确保每条消息处理后才手动确认。

3. **retries=5**: 如果消息发送失败，生产者将最多重试 5 次，以减少临时网络或其他问题导致的消息丢失。

4. **commit()**: 消费者端在成功处理消息后手动提交偏移量，确保每条消息都只处理一次。这样，如果消费者在处理消息时发生故障，下一次从未提交的偏移量重新开始。

通过这种方式，结合生产者的 `acks` 确认机制和消费者的手动提交偏移量，能够最大限度地确保每条消息只被处理一次，同时防止消息丢失或重复处理。





# 工作模式



![img](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/78848a678fba46e3090f37a9e04deac5/2982919d07179229248caaa6e93756e8.png)



点对点和订阅模式是消息系统的两种典型模式，通常用来形容**消息队列（Message Queue）**和**发布-订阅（Pub-Sub）**模型。

1. **点对点模式（Point-to-Point Mode）**：在点对点模式下，消息会发送到一个队列中，**每个消息只会被一个消费者处理**。消费者从队列中消费消息，消费过的消息就不会再被其他消费者看到。Kafka的"指定分区模式"与此有些类似。

2. **订阅模式（Publish-Subscribe Mode）**：在发布-订阅模式下，**消息会广播给多个订阅者**，每个订阅者都会收到所有消息。Kafka的"订阅模式"与此类似。

Kafka 作为一个发布-订阅系统，支持多个消费者消费同一条消息，因此它的主要模式偏向于**发布-订阅**。我们可以通过特定的消费者组（consumer group）模拟点对点模式，或者通过不同的订阅来实现发布-订阅模式。

### 1. **点对点模式（通过Consumer Group实现）**
在Kafka中，**每个消费者组内的每个分区只能有一个消费者**消费。即使有多个消费者同时订阅同一个主题，由于分区分配机制，某个分区中的消息只会被组内的一个消费者消费。

#### 点对点模式样例：
```python
from kafka import KafkaConsumer

# 通过指定 group_id 实现点对点消费模式
consumer = KafkaConsumer(
    'my_topic', 
    bootstrap_servers=['localhost:9092'],
    group_id='my_group',  # 每个消费者组内的消息只会被一个消费者消费
    enable_auto_commit=True,
    auto_offset_reset='earliest',
    value_deserializer=lambda x: x.decode('utf-8')
)

for message in consumer:
    print(f"Point-to-Point message received: {message.value}")
```

在此示例中，`group_id='my_group'`表示该消费者属于`my_group`组。Kafka会将该主题的分区在组内的消费者间分配，每个分区内的消息只会被一个消费者消费。

### 2. **发布-订阅模式**
在发布-订阅模式下，多个消费者组都可以订阅同一个主题，**每个组都会独立消费消息**。这种方式下，消息会被广播给多个消费者组，每个组内的消费者会独立地处理该消息。

#### 发布-订阅模式样例：
```python
from kafka import KafkaConsumer

# 订阅模式下，不同的消费者组都可以独立消费同一主题的消息
consumer1 = KafkaConsumer(
    'my_topic',
    bootstrap_servers=['localhost:9092'],
    group_id='group1',  # 订阅组1
    enable_auto_commit=True,
    auto_offset_reset='earliest',
    value_deserializer=lambda x: x.decode('utf-8')
)

consumer2 = KafkaConsumer(
    'my_topic',
    bootstrap_servers=['localhost:9092'],
    group_id='group2',  # 订阅组2
    enable_auto_commit=True,
    auto_offset_reset='earliest',
    value_deserializer=lambda x: x.decode('utf-8')
)

for message in consumer1:
    print(f"Consumer1 (Group1) received: {message.value}")

for message in consumer2:
    print(f"Consumer2 (Group2) received: {message.value}")
```

在这个示例中，`group_id='group1'` 和 `group_id='group2'` 表示两个独立的消费者组。即使订阅了相同的主题，每个组都会独立地消费所有消息，因此所有消息都会分别被两组消费者接收到。

### 总结：
- **点对点模式**：通过消费者组中的分区分配机制实现，每条消息只会被一个消费者组内的某个消费者消费。
- **订阅模式**：通过不同的消费者组，每条消息会广播给订阅了该主题的所有消费者组，每个组内独立消费。



**group_id 是决定点对点模式和发布-订阅模式的关键区别。**

​	•	**点对点模式**：所有消费者共享相同的group_id，消息在消费者组内分配。

​	•	**发布-订阅模式**：每个消费者组有不同的group_id，所有消费者组都能接收到相同的消息。





