---
title: python八股题
top: false
cover: false
toc: true
mathjax: true
draft: false
date: 2024-08-30 15:27:31
password:
summary:
tags:
- python
categories:
- find JOB
---



# TOSEE:

[【建议收藏】50 道硬核的 Python 面试题.._python程序员面试题-CSDN博客](https://blog.csdn.net/weixin_50829653/article/details/129384275)



[taizilongxu/interview_python: 关于Python的面试题](https://github.com/taizilongxu/interview_python)





# 基础语法特性

1. **列表（list）和元组（tuple）的区别**：
   - 列表是可变的，可以进行增删改操作。
   - 元组是不可变的，一旦创建就不能修改。
   - 列表使用方括号`[]`，元组使用圆括号`()`。
   - 列表适合需要频繁修改的数据集合，元组适合不需要修改的数据集合。
2. **如何进行字符串插值**：
   - 使用f-string：`f'Hello {name}'`
   - 使用`%`操作符：`'Hey %s %s' % (name, name)`
   - 使用`str.format()`方法：`'My name is {}'.format(name)`



## python没有指针，实际都是引用

**使用 `id` 函数查看引用**

你可以使用 `id` 函数来查看对象的内存地址，从而验证两个变量是否引用同一个对象。

```
a = [1, 2, 3]
b = a

print(id(a))  # 输出: 对象 a 的内存地址
print(id(b))  # 输出: 与 a 相同的内存地址
```





## python元类

**类同样也是一种对象。是的，没错，就是对象。只要你使用关键字class，Python解释器在执行的时候就会创建一个对象。**下面的代码段：

```
>>> class ObjectCreator(object):
…       pass
…
```

将在内存中创建一个对象，名字就是ObjectCreator。**这个对象（类）自身拥有创建对象（类实例）的能力，而这就是为什么它是一个类的原因。**但是，它的**本质仍然是一个对象**，于是乎你可以对它做如下的操作：

1) 你可以将它赋值给一个变量
2) 你可以拷贝它
3) 你可以为它增加属性
4) 你可以将它作为函数参数进行传递

**使用 `type` 动态创建类**

`type` 函数可以接受三个参数来创建一个新的类：

1. 类的名称（字符串）
2. 父类的元组（你可以指定多个父类）
3. 类的属性和方法的字典

以下是一个示例，展示如何使用 `type` 动态创建一个类：

```
# 动态创建一个类
MyClass = type('MyClass', (object,), {'attr': 42, 'method': lambda self: 'Hello, World!'})

# 创建类的实例
instance = MyClass()

# 访问属性和方法
print(instance.attr)  # 输出: 42
print(instance.method())  # 输出: Hello, World!
```



## @staticmethod和@classmethod

继承：

- **`staticmethod`：静态方法不会被子类继承。**如果子类需要使用静态方法，它必须显式地定义或调用它。
- `classmethod`：类方法会被子类继承。子类可以重写类方法以实现不同的行为

Python其实有3个方法,即静态方法(staticmethod),类方法(classmethod)和实例方法,如下:

```
def foo(x):
    print "executing foo(%s)"%(x)

class A(object):
    def foo(self,x):
        print "executing foo(%s,%s)"%(self,x)

    @classmethod
    def class_foo(cls,x):
        print "executing class_foo(%s,%s)"%(cls,x)

    @staticmethod
    def static_foo(x):
        print "executing static_foo(%s)"%x

a=A()
```





## Python自省（和java反射很像）



这个也是python彪悍的特性.

自省就是面向对象的语言所写的程序在运行时,所能知道对象的类型.简单一句就是运行时能够获得对象的类型.比如type(),dir(),getattr(),hasattr(),isinstance().

```
a = [1,2,3]
b = {'a':1,'b':2,'c':3}
c = True
print type(a),type(b),type(c) # <type 'list'> <type 'dict'> <type 'bool'>
print isinstance(a,list)  # True
```





## Python中单下划线和双下划线

- **单下划线 `_`**: 受保护的变量或方法，不建议类外部访问。
- **双下划线 `__`**: 私有变量，触发名称改写，避免子类覆盖。
- **前后缀双下划线 `__`**: 特殊方法或属性，由解释器使用。



## python迭代器和生成器

作用：

**可以边使用，边生成，不用一次性生成完**

**迭代器**

**迭代器是一个实现了迭代协议的对象。迭代协议包括两个方法：`__iter__()` 和 `__next__()`。**

你可以通过实现这两个方法来创建一个自定义迭代器。

```
class MyIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

# 使用迭代器
my_iter = MyIterator([1, 2, 3])
for item in my_iter:
    print(item)
```

**生成器**（Python里最常见的**yield就是协程的思想**）

生成器是一个特殊的迭代器，通过使用 `yield` 关键字来生成值。**生成器函数在每次调用 `yield` 时会暂停**，**并在下次调用时从暂停的地方继续执行。**

```
def my_generator():
    yield 1
    yield 2
    yield 3

# 使用生成器
gen = my_generator()
for item in gen:
    print(item)
```

## `*args` and `**kwargs`

`print_all` 函数接受一个必需的参数 `a`**，一个可变长度的位置参数（`*args`），以及一个可变长度的关键字参数（`**kwargs`）**。这意味着您可以在调用此函数时传递任意数量的位置参数和关键字参数。以下是如何定义和使用 `print_all` 函数的示例：

```python
def print_all(a, *args, **kwargs):
    print("a:", a)
    
    # 打印位置参数
    for i, arg in enumerate(args):
        print(f"位置参数 {i + 1}:", arg)

    # 打印关键字参数
    for key, value in kwargs.items():
        print(f"关键字参数 {key}:", value)

# 示例用法
print_all(1, 2, 3, 4, x=5, y=6, z=7)
```

输出结果：

```
a: 1
位置参数 1: 2
位置参数 2: 3
位置参数 3: 4
关键字参数 x: 5
关键字参数 y: 6
关键字参数 z: 7
```

在这个示例中，`print_all` 函数首先打印参数 `a` 的值，**然后遍历 `args` 元组以打印所有位置参数，最后遍历 `kwargs` 字典以打印所有关键字参数。**

## AOP实现

通过注解可以实现





## python一个类可以继承多个类（继承查找顺序）

> 一个旧式类的深度优先的例子

```
class A():
    def foo1(self):
        print "A"
class B(A):
    def foo2(self):
        pass
class C(A):
    def foo1(self):
        print "C"
class D(B, C):
    pass

d = D()
d.foo1()

# A
```



**按照经典类的查找顺序`从左到右深度优先`的规则，在访问`d.foo1()`的时候,D这个类是没有的..那么往上查找,先找到B,里面没有,深度优先,访问A,找到了foo1(),所以这时候调用的是A的foo1()，从而导致C重写的foo1()被绕过**



注意：

**java不可以继承多个类，但是一个类可以实现多个接口**

## `__new__`和`__init__`的区别



这个`__new__`确实很少见到,先做了解吧.

1. `__new__`是一个静态方法,而`__init__`是一个实例方法.
2. `__new__`方法会返回一个创建的实例,而`__init__`什么都不返回.
3. 只有在`__new__`返回一个cls的实例时后面的`__init__`才能被调用.(**`__new__()`在`__init__()`之前被调用，用于生成实例对象**)



## MRO与super（）函数

`super()` 函数用于在类的方法中调用其父类（或兄弟类）的方法。`super()` 函数可以确保在多重继承情况下，类方法的调用顺序遵循 MRO。

### MRO 示例

以下是一个使用 MRO 的多重继承示例：

```python
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")
        super().method()

class C(A):
    def method(self):
        print("C")
        super().method()

class D(B, C):
    def method(self):
        print("D")
        super().method()

d = D()
d.method()
```

在这个示例中，我们有四个类：A、B、C 和 D。类 B 和 C 都继承自类 A，而类 D 则继承自类 B 和 C。当我们调用 `d.method()` 时，输出顺序将是：`D -> B -> C -> A`。这是因为 MRO 确保在调用类 D 的方法之后，首先调用类 B 的方法（因为 D 继承自 B），然后调用类 C 的方法（因为 D 也继承自 C），最后调用类 A 的方法（因为 A 是 B 和 C 的共同父类）。



## 单例

```python
class Singleton(object):
    def __new__(cls, *args, **kw):。
        if not hasattr(cls, '_instance'): # 如果没有，说明还没有创建实例。
            orig = super(Singleton, cls) # 获取父类（即 object）的一个代理对象。
            cls._instance = orig.__new__(cls, *args, **kw) # 用父类的 __new__ 方法创建一个新实例，并将其赋值给类的 _instance 属性。
        return cls._instance # 返回类的唯一实例。
    

# 继承自单例，所以本身也是单例
class MyClass(Singleton):
    a = 1
```





**方案二：基于python的模块导入是一个天然的单例模式**

作为python的模块是天然的单例模式

```
# mysingleton.py
class My_Singleton(object):
    def foo(self):
        pass

my_singleton = My_Singleton()

# to use
from mysingleton import my_singleton

my_singleton.foo()
```





**方案3：装饰器**

```
1 def singleton(cls):
2     instances = {}
3     
4     def getinstance(*args, **kwargs):
5         if cls not in instances:
6             instances[cls] = cls(*args, **kwargs)
7         return instances[cls]
8     return getinstance
```





## python的模块导入机制（有缓存）

在 Python 中，模块的导入机制确保每个模块只执行一次，即使它被多个其他模块导入。这是通过 `sys.modules` 字典实现的，该字典缓存了所有已经导入的模块。

文件内容如下：

**[a.py](http://a.py/)**:

```
print("Module a is being executed")

def hello():
    print("Hello from module a")
```

**[b.py](http://b.py/)**:

```
import a
```

**[c.py](http://c.py/)**:

```
import a
```

**[d.py](http://d.py/)**:

```
import b
import c

print("Module d is being executed")
```

当你运行 `d.py` 时，输出将是：

```
复制Module a is being executed
Module d is being executed
```





## 作用域

Python 中，一个变量的作用域总是由在代码中被赋值的地方所决定的。

当 Python 遇到一个变量的话他会按照这样的顺序进行搜索：

**本地作用域（Local）→当前作用域被嵌入的本地作用域（Enclosing locals）→全局/模块作用域（Global）→内置作用域（Built-in）**





## python*解释器全局锁（GIL）*

**GIL 的主要目的是保护 Python 解释器的内部数据结构，特别是 CPython 的内存管理和引用计数机制。它防止多线程同时执行时出现数据竞争和其他线程安全问题。**



为了避免在多线程环境下引用计数更新时出现竞争条件，**GIL 被引入来确保同一时间只有一个线程在执行 Python 代码。**

**跟多线程，手动加一个lock不一样，这个GIL是python这个语言的**

- GIL 是**全局的**，作用于整个 Python 解释器。它确保同一时间只有一个线程在**执行 Python 字节码**。

- `threading.Lock` 是**局部的**，**作用于特定的代码块或资源**。它用于保护共享资源，确保同一时间只有一个线程可以访问该资源。



1. **多线程性能**：
   - **在多线程 CPU 密集型任务中，GIL 会导致性能瓶颈，因为同一时间只有一个线程能够执行 Python 代码**。即使在多核 CPU 上，Python 也无法充分利用多核优势。
   - 对于 I/O 密集型任务（如网络请求、文件读写），GIL 的影响较小，因为线程在等待 I/O 操作完成时会释放 GIL，从而允许其他线程执行。

以下是一个简单的示例，展示了 GIL 对多线程性能的影响：

```
python已复制import threading
import time

def cpu_bound_task():
    start = time.time()
    count = 0
    while count < 10**7:
        count += 1
    end = time.time()
    print(f"Task completed in {end - start:.2f} seconds")

# 创建两个线程
thread1 = threading.Thread(target=cpu_bound_task)
thread2 = threading.Thread(target=cpu_bound_task)

# 启动线程
thread1.start()
thread2.start()

# 等待线程完成
thread1.join()
thread2.join()
```

在这个示例中，两个线程都在执行一个 CPU 密集型任务。由于 GIL 的存在，两个线程不能真正并行执行，因此总的执行时间不会显著减少。

**解决方案**

- **多进程**：
  - 使用 `multiprocessing` 模块可以创建多个进程，每个进程都有自己的 Python 解释器和 GIL，从而可以充分利用多核 CPU。
- **其他 Python 解释器**：
  - 一些 Python 解释器没有 GIL，例如 Jython（基于 Java 的 Python 实现）和 IronPython
- **异步编程**：
  - 对于 I/O 密集型任务，使用异步编程（如 `asyncio` 模块）可以有效地提高性能，而不受 GIL 的限制。





## Python垃圾回收机制(内存管理)

### 引用计数

引用计数是 Python 内存管理的基础机制。每个对象都有一个引用计数器，记录有多少个引用指向该对象。当对象的引用计数变为零时，说明没有任何引用指向该对象，该对象就可以被回收。

### 标记-清除

上一小节提到，**引用计数算法无法解决循环引用问题**，循环引用的对象会导致大家的计数器永远都不会等于`0`，带来无法回收的问题。

`标记-清除`算法主要用于潜在的循环引用问题，该算法分为2步：

> 基本思路是先按需分配，等到没有空闲内存的时候**从寄存器和程序栈上的引用出发，遍历以对象为节点、以引用为边构成的图，把所有可以访问到的对象打上标记，然后清扫一遍内存空间，把所有没标记的对象释放。**



### 分代技术

分代回收的整体思想是：**将系统中的所有内存块根据其存活时间划分为不同的集合，每个集合就成为一个“代”，垃圾收集频率随着“代”的存活时间的增大而减小**，存活时间通常利用经过几次垃圾回收来度量。

Python默认定义了三代对象集合，索引数越大，对象存活时间越长。

举例： 当某些内存块M经过了3次垃圾收集的清洗之后还存活时，我们就将内存块M划到一个集合A中去，而新分配的内存都划分到集合B中去。当垃圾收集开始工作时，大多数情况都只对集合B进行垃圾回收，而对集合A进行垃圾回收要隔相当长一段时间后才进行，这就使得垃圾收集机制需要处理的内存少了，效率自然就提高了。在这个过程中，集合B中的某些内存块由于存活时间长而会被转移到集合A中，当然，集合A中实际上也存在一些垃圾，这些垃圾的回收会因为这种分代的机制而被延迟。



## python list对象

Python中的列表是由**对其它对象的引用组成的连续数组**，指向这个数组的指针及其长度被保存在一个列表头结构中。

1. **动态数组**：
   - Python 的 `list` 实际上是一个动态数组。动态数组的一个关键特性是它可以在需要时自动扩展，以容纳更多的元素。
   - 当 `list` 的容量不足以容纳新元素时，Python 会分配一个更大的内存块，并将现有元素复制到新的内存块中。
2. **预分配策略**：
   - 为了减少频繁的内存分配和数据复制操作，Python 的 `list` 实现采用了预分配策略。当 `list` 需要扩展时，它通常会分配比实际需要更多的内存，以便为将来的扩展预留空间。
   - 这种策略使得 `list` 的扩展操作在摊销时间复杂度上是 O(1) 的。
3. **内存布局**：
   - Python 的 `list` 是一个对象数组，每个元素都是一个指向实际数据的指针。这意味着 `list` 可以存储任意类型的对象，包括其他 `list`、字典、字符串等。
   - 由于 `list` 存储的是指针而不是实际数据，因此在 `list` 中存储大型对象时，内存使用效率较高。



## Python的is



is是对比地址,==是对比值

## read,readline和readlines



- read 读取整个文件
- readline 读取**下一行**,使用生成器方法
- readlines 读取整个文件到一个**迭代器**以供我们遍历



## range and xrange

  所以 xrange做循环的性能比range好 ，尤其是返回很大的时候，尽量用xrange吧，除非你是要返回一个列表。



## super（）方法



`super()` 是 Python 中一个非常有用的函数，特别是在涉及继承和多重继承时。它允许你调用父类（或基类）的方法，而不需要显式地引用父类的名字。这样做的主要好处是提高代码的可维护性和灵活性，特别是在多重继承的情况下。

**基本用法**

**在单继承的情况下，`super()` 可以用来调用父类的方法。例如：**

```
class Parent:
    def __init__(self):
        print("Parent init")

class Child(Parent):
    def __init__(self):
        super().__init__()  # 调用父类的 __init__ 方法
        print("Child init")

child = Child()
```

在多重继承的情况下，**`super()` 的优势更加明显。它遵循一种称为“方法解析顺序”（MRO）的规则，确保每个类的方法只被调用一次，并且按照正确的顺序调用。**

例如：

```
class A:
    def __init__(self):
        print("A init")

class B(A):
    def __init__(self):
        super().__init__()
        print("B init")

class C(A):
    def __init__(self):
        super().__init__()
        print("C init")

class D(B, C):
    def __init__(self):
        super().__init__()
        print("D init")

d = D()
```

输出：

```
A init
C init
B init
D init
```







# 应用题



## CPython缓存池

```
a, b, c, d = 1, 1, 1000, 1000
True False
```

**上面代码中`a is b`的结果是`True`但`c is d`的结果是`False`，这一点的确让人费解。CPython解释器出于性能优化的考虑，把频繁使用的整数对象用一个叫`small_ints`的对象池缓存起来造成的。**`small_ints`缓存的整数值被设定为`[-5, 256]`这个区间，也就是说，在任何引用这些整数的地方，都不需要重新创建`int`对象，而是直接引用缓存池中的对象。如果整数不在该范围内，那么即便两个整数的值相同，它们也是不同的对象。



**扩展**：如果你用PyPy（另一种Python解释器实现，支持JIT，对CPython的缺点进行了改良，在性能上优于CPython，但对三方库的支持略差）来运行上面的代码，你会发现所有的输出都是True。



## 闭包

下面这段代码的执行结果是什么。

```scss
def multiply():
    return [lambda x: i * x for i in range(4)]
print([m(100) for m in multiply()])
```

**这段代码的执行结果是 `[300, 300, 300, 300]`。**

为了理解为什么会这样，我们需要分析 `multiply` 函数的实现。这个函数返回一个由 `lambda` 函数组成的列表，这些 `lambda` 函数捕获了变量 `i` 的值。然而，`i` 的值在列表推导式的整个过程中都在变化。**当列表推导式结束时，`i` 的值将保持为 3（因为 `range(4)` 的最后一个值是 3）。因此，所有 `lambda` 函数都捕获了相同的 `i` 值，即 3。**

## 请解释Python中with关键字的用法

with 语句的原理:上下文管理协议(Context ManagementProtocol):

**包含方法enter ()和exit ()，支持该协议的对象要实现这两个方法。**



## python 内存区域

我们知道变量的定义会把变量值存储在内存中。其实，具体的是把

- **变量值存放在内存的堆区中，**

- **把变量名和变量值的绑定关系存放在栈区。绑定关系就是变量名保存变量值所在的内存地址。**



#### 直接引用 & 间接应用

![img](https://i-blog.csdnimg.cn/blog_migrate/9f1e556a4322cc194c09d6ff9541c6d8.jpeg)

![img](https://i-blog.csdnimg.cn/blog_migrate/fe38b91a974aa2ca14023bb072457592.jpeg)

## 可变数据类型于不可变数据类型

可变数据类型：**列表list和字典dict**

- 不可变数据类型，**不允许变量的值发生变化，如果改变了变量的值，相当于是新建了一个对象，而对于相同的值的对象，在内存中则只有一个对象**，就是不可变数据类型**引用的地址的值不可改变**改变对象的值，其实是引用了不同的对象



不可变数据类型：**整型int、浮点型float、字符串型string和元组tuple**





## property注解

将函数变成属性来访问

**让方法属性化调用**



## 4G内存，读取8G大小文件

基于yield和read的分块

```
def read_large_file(file_path, block_size=4 * 1024 * 1024):
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(block_size)
            if not data:
                break
            yield data
```





## Python中为什么没有函数重载?

首**先Pvthon是解释型语言，函数重载现象通常出现在编译型语言中。其次Python是动态类型语言，函数的参数没有类型约束，也就无法根据参数类型来区分重载**。再者Python中函数的参数可以有默认值，可以使用可变参数和关键字参数，因此即便没有函数重载，也要可以让一个函数根据调用者传入的参数产生不同的行为。
