# 关于手机推送技术架构


# 【Java响应式编程】Project Reactor 实战：从 Flux 入门到 Sinks 进阶

在 Java 后端开发中，随着 Spring WebFlux 的普及（**尤其是当前越来越多的LLM流失开始用到FLUX**），响应式编程（Reactive Programming）变得越来越重要。很多同学可能听说过 `Flux` 和 `Mono`，但在实际业务中，如何将传统的“回调接口”或“外部事件”转换为响应式流，往往是新手最头疼的问题。

今天这篇文章，带你从最基础的 `Flux` 开始，一步步掌握 Reactor 中最强大的工具——**Sinks**。

## 一、 什么是 Flux？

在 Project Reactor（Spring WebFlux 的核心库）中，`Flux<T>` 代表一个**包含 0 到 N 个元素**的异步序列。

你可以把它想象成一条**传送带**（或者水管）：
- **List**：是一次性把所有货物打包给你。
- **Flux**：是货物一件件（或一批批）随着时间推移传送过来。

### 1.1 最简单的 Flux 示例

```java
// 创建一个包含 1, 2, 3 的流
Flux<Integer> flux = Flux.just(1, 2, 3);

// 只有订阅（subscribe）了，流才会开始流动
flux.map(i -> "数字: " + i)
    .subscribe(System.out::println);
```

### 1.2 为什么需要 Flux？
它的强大在于**操作符**。你可以像处理集合一样处理异步流：过滤（filter）、转换（map）、聚合（reduce），甚至处理时间窗口（window）。

```java
// 模拟：每 500ms 产生一个数据，只取前 5 个，且只要偶数
Flux.interval(Duration.ofMillis(500))
    .take(5)
    .filter(i -> i % 2 == 0)
    .subscribe(i -> System.out.println("收到偶数: " + i));
```

---

## 二、 遇到的问题：如何手动触发数据？

上面的例子中，数据源都是**静态**的（`just`）或者**自动生成**的（`interval`）。

但在实际业务中，我们经常遇到这种场景：
> 场景1: 我有一个 MQ 的监听器，或者一个 WebSocket 的连接。当**外部事件**发生时（比如收到一条消息），我希望手动把这个消息“推”到 Flux 里，让下游去处理。
>
> 场景2:有一个Flux流，但是突然我需要服务端主动关闭这个流，并且让前端感知这个特殊的error断开。那么我可以创建一个errorSink。需要的时候对这个sink进行主动的推送。

这时候，`Flux.just()` 就无能为力了。我们需要一个**“水龙头”**，这就是 **Sinks**。

---

## 三、 Sinks：连接传统与响应式的桥梁

**Sinks** 是 Reactor 3.4.0 之后推出的新一代 API，用于替代旧的 `Processor`。它既是数据的**生产者**（我们可以往里塞数据），又是数据的**发布者**（可以被转成 Flux 供人订阅）。

### 3.1 Sinks 的三种常见模式

在使用 `Sinks.many()` 时，我们通常面临三种选择：

1.  **`unicast()` (单播)**：只能有一个订阅者。适合点对点消息。
2.  **`multicast()` (多播)**：支持多个订阅者。适合广播消息。
3.  **`replay()` (重放)**：多播，且新来的订阅者能看到之前的历史数据。

### 3.2 实战代码：将“回调接口”转换为 Flux

这是 Sinks 最经典的用法。假设我们有一个老旧的订单服务，它通过回调通知新订单：

```java
// 1. 这是一个传统的监听器接口
interface OrderListener {
    void onNewOrder(String orderId);
}

// 2. 这是一个传统的服务，只能注册回调
class LegacyOrderService {
    private OrderListener listener;

    public void register(OrderListener listener) {
        this.listener = listener;
    }

    // 模拟收到外部订单
    public void fireEvent(String id) {
        if (listener != null) listener.onNewOrder(id);
    }
}
```

我们要把它改造成响应式的 `Flux<String>`，代码如下：

```java
import reactor.core.publisher.Flux;
import reactor.core.publisher.Sinks;

public class ReactiveBridge {

    // 1. 创建一个 Sink，支持多播，带有背压缓存
    private final Sinks.Many<String> sink = Sinks.many().multicast().onBackpressureBuffer();

    public ReactiveBridge(LegacyOrderService legacyService) {
        // 2. 在传统回调中，把数据“推”进 Sink
        legacyService.register(orderId -> {
            // tryEmitNext 是线程安全的
            // 它会尝试推送，如果失败（比如没有订阅者或流被取消）会返回结果状态
            sink.tryEmitNext(orderId); 
        });
    }

    // 3. 对外暴露 Flux，隐藏 Sink 的写入能力
    public Flux<String> getOrderFlux() {
        return sink.asFlux();
    }
}
```

### 3.3 测试效果

```java
public static void main(String[] args) {
    LegacyOrderService oldService = new LegacyOrderService();
    ReactiveBridge bridge = new ReactiveBridge(oldService);

    // 订阅者 1：处理所有订单
    bridge.getOrderFlux()
          .subscribe(id -> System.out.println("[订阅者1] 处理订单: " + id));

    // 订阅者 2：只关心 VIP 订单
    bridge.getOrderFlux()
          .filter(id -> id.startsWith("VIP"))
          .subscribe(id -> System.out.println("[订阅者2] 发现 VIP: " + id));

    // 模拟外部事件触发
    System.out.println("--- 外部事件开始 ---");
    oldService.fireEvent("ORDER-001");
    oldService.fireEvent("VIP-888");
}
```

**输出结果：**
```text
--- 外部事件开始 ---
[订阅者1] 处理订单: ORDER-001
[订阅者1] 处理订单: VIP-888
[订阅者2] 发现 VIP: VIP-888
```

---

## 四、 避坑指南

在使用 Sinks 时，有两点需要特别注意：

1.  **线程安全**：
    *   尽量使用 `sink.tryEmitNext(data)` 而不是 `sink.emitNext(data, handler)`。
    *   `tryEmitNext` 是线程安全的，适合在多线程环境下（如 Web 请求、MQ 线程池）并发调用。

2.  **背压（Backpressure）**：
    *   在创建 Sink 时，最好指定背压策略，例如 `.onBackpressureBuffer()`。
    *   如果下游消费速度太慢，Sink 默认会缓存数据。如果缓存满了，你需要决定是丢弃新数据还是报错（`FAIL_OVERFLOW`）。

## 五、 总结

*   **Flux** 是**水流**，负责数据的异步传递和处理。
*   **Sinks** 是**水龙头**，负责将外部世界的同步调用、回调事件转换成响应式水流。

