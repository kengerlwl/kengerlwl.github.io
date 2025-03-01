# python协程




# python协程





## 语法

### 定义协程

**协程是使用 `async def` 关键字定义的函数**。协程可以在执行过程中暂停，并在稍后继续执行。

```
import asyncio

async def my_coroutine():
    print("Hello")
    await asyncio.sleep(1)
    print("World")
```



### 运行协程

要运行一个协程，你需要一个事件循环。`asyncio.run` 是一个方便的函数，用于运行顶层的协程。

```
asyncio.run(my_coroutine())
```

### `await` 关键字，阻塞等待，同步

`await` 关键字用于暂停协程的执行，等待另一个协程完成。它只能在协程函数内部使用。

```python
async def my_coroutine():
    print("Start")
    await asyncio.sleep(1)  # 暂停协程，等待 asyncio.sleep(1) 完成
    print("End")
```





### 创建协程任务，（实际上就是新建一个对象）

任务是对协程的进一步封装，它表示一个异步操作的执行单元。你可以使用 `asyncio.create_task` 来创建任务。

```python
async def my_coroutine():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

async def main():
    task = asyncio.create_task(my_coroutine())
    await task

asyncio.run(main())
```



### 异步任务返回结果

让我们通过一个示例来说明如何从异步任务中获取返回值。

**异步函数内返回结果**

```python
import asyncio

async def compute_square(x):
    await asyncio.sleep(1)
    return x * x

async def main():
    # 创建多个任务并发运行
    task1 = asyncio.create_task(compute_square(2))
    task2 = asyncio.create_task(compute_square(3))

    # 等待所有任务完成并获取结果
    result1 = await task1
    result2 = await task2

    print(f"Result 1: {result1}")
    print(f"Result 2: {result2}")

asyncio.run(main())
```

**普通函数调用返回**

```
import asyncio

async def compute_square(x):
    await asyncio.sleep(1)
    return x * x

async def main():
    # 创建多个任务并发运行
    task1 = asyncio.create_task(compute_square(2))
    task2 = asyncio.create_task(compute_square(3))

    # 等待所有任务完成并获取结果
    result1 = await task1
    result2 = await task2

    return result1, result2

def run_coroutine():
    # 在普通函数中调用协程并获取结果
    results = asyncio.run(main())
    print(f"Result 1: {results[0]}")
    print(f"Result 2: {results[1]}")

# 调用普通函数
run_coroutine()
```





## 并发执行多个协程，基于使用 `asyncio.create_task` 或 `asyncio.gather` 可以并发运行多个协程，使它们在等待期间让出控制权给事件循环，从而提高效率。

**并发执行的任务，两个task会同时执**

```python
import asyncio

async def say(what, delay):
    await asyncio.sleep(delay)
    print(what)

async def main():
    # 创建多个任务并发运行
    task1 = asyncio.create_task(say("Hello", 1))
    task2 = asyncio.create_task(say("World", 1))

    # 等待所有任务完成，前面已在create_task的时候，程序就已经在执行了，下面只是依次等待两个返回
    await task1
    await task2

asyncio.run(main())
```



基于gather也可以实现一样的效果

```python
import asyncio

async def say(what, delay):
    await asyncio.sleep(delay)
    print(what)

async def main():
    await asyncio.gather(
        say("Hello", 1),
        say("World", 1)
    )

asyncio.run(main())
```



## 超时控制

```python
import asyncio

async def say(what, delay):
    await asyncio.sleep(delay)
    print(what)

async def main():
    try:
        await asyncio.wait_for(say("Hello", 3), timeout=1)
    except asyncio.TimeoutError:
        print("Timeout!")

asyncio.run(main())
```






