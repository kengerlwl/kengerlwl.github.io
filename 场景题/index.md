# 场景题




# 高并发场景题

- 架构上：微服务，云原生，可以针对容器引入Prometheus+grafana进行监控告警，流量过高即时扩容
- 流量上：比如常见的令牌桶算法，从用户源头上限流。
- 业务上：
  - 加锁：乐观锁，尽量减少锁冲突，其实乐观锁应对读多写少
  - 优化并行逻辑
  - 优化业务流程，将不需要即时处理的步骤，异步放入后台（直接异步开线程，或者放入消息队列异步削峰）
- 数据库：如果数据库是瓶颈
  - 分库分表
  - 读写分离，读和写的数据分开
  - 慢查询优化
  - 引入更高性能的数据库：TIDB，
- 拆库存（针对数据库数据库存修改的性能优化）：将库存修改为多个记录，轮询着分别进行修改
- 引入缓存优化性能：redis

![refs/heads/master/image-20240910230534572](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/7afb1c8716e4bcd11c397871e7757882/666b1c1eb79ee854b47ed10b7bbf5876.png)



# 使用Redis实现延迟消息队列

实际上使用的是zset。有序集合。

然后将时间作为score，也就是排序的key，放入redis中。

然后引入一个消费者，定期扫描这个zset。

注意：

- zset也是一个key-value。只不过里面的value是一个红黑树





# rabbitmq实现延时消息队列

给普通消息加入ttl。让其超时，然后超时后，会放入死信队列，从死信队列消费就是延迟消息队列

实际上有一个插件可以实现。







# 为什么有了es还要mysql

![refs/heads/master/image-20240912192526555](https://raw.githubusercontent.com/kengerlwl/kengerlwl.github.io/refs/heads/master/image/7afb1c8716e4bcd11c397871e7757882/89f4727372a0ad5b8c8ac799971e1c3c.png)








