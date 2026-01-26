# python的SQLAlchemy 的踩坑历程




# 背景

最近在项目开发的时候，碰到了SQLAlchemy 的一些问题，记录一下，对于其针对数据库的操作有一些疑惑，

SQLAlchemy 是一个python这边的ORM框架



# 事务提交等级



首先，目前的mysql数据库默认的存储引擎是innodb。然后隔离级别是

- **可重复读（\*repeatable read\*）**，指一个事务执行过程中看到的数据，一直跟这个事务启动时看到的数据是一致的，**MySQL InnoDB 引擎的默认隔离级别**；



**事务**

在python使用该框架中，什么时候算是一个事务呢。

```
class xxxService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, doc_eval: xxxuation) -> None:
        self.session.add(doc_eval)
        self.session.commit()
```

每一个commit算是一个事务。



**缓存机制**

**SQLAlchemy 带有对象缓存机制，在重复查询相同的对象时，直接先查询本地的缓存，而不需要从数据库加载数据。**

经过实际查验，发现在查询时，**如果查询条件一样，会直接从本地获取数据，返回的实体对象内存地址是一样的**



# 连接超时问题



## 参数

```
create_engine() 函数和连接池相关的参数有：

pool_recycle, 默认为 -1, 推荐设置为 7200, 即如果 connection 空闲了 7200 秒，自动重新获取，以防止 connection 被 db server 关闭。
pool_size=5, 连接数大小，默认为 5，正式环境该数值太小，需根据实际情况调大
max_overflow=10, 超出 pool_size 后可允许的最大连接数，默认为 10, 这 10 个连接在使用过后，不放在 pool 中，而是被真正关闭的。
pool_timeout=30, 获取连接的超时阈值，默认为 30 秒
```

## 连接池



```undefined
session 和 connection 不是相同的东西， session 使用连接来操作数据库，一旦任务完成 session 会将数据库 connection 交还给 pool。

在使用 create_engine 创建引擎时，如果默认不指定连接池设置的话，一般情况下，SQLAlchemy 会使用一个 QueuePool 绑定在新创建的引擎上。并附上合适的连接池参数
```

**create_engine() 函数和连接池相关的参数有：**

- pool_recycle, 默认为 -1, 推荐设置为 7200, 即如果 connection 空闲了 7200 秒，自动重新获取，以防止 connection 被 db server 关闭。
- pool_size=5, 连接数大小，默认为 5，正式环境该数值太小，需根据实际情况调大
- max_overflow=10, 超出 pool_size 后可允许的最大连接数，默认为 10, 这 10 个连接在使用过后，不放在 pool 中，而是被真正关闭的。
- pool_timeout=30, 获取连接的超时阈值，默认为 30 秒

SQLAlchemy不使用连接池：
在创建引擎时指定参数 poolclass=NullPool 即禁用了SQLAlchemy提供的数据库连接池。SQLAlchemy 就会在执行 session.close() 后立刻断开数据库连接。

**当然，如果没有被调用 session.close()，则数据库连接不会被断开，直到程序终止。（但是数据库有8小时超时）**



## Session

### 概念

一个Session就是一个与数据库的交互过程。**同时只能维持一个事务**

**具有模型绑定机制，针对add等操作，如果没有Commit那么该事务就还没有提交，可以回滚。**



### 关于线程安全：

**session不是线程安全的，在多线程的环境中，默认情况下，多个线程将会共享同一个session。**试想一下，假设A线程正在使用session处理数据库，B线程已经执行完成，把session给close了，那么此时A在使用session就会报错，怎么避免这个问题？

```markdown
1. 可以考虑在这些线程之间共享Session及其对象。但是应用程序需要确保实现正确的锁定方案，以便多个线程不会同时访问Session或其状态。SQLAlchemy 中的 scoped_session 就可以证线程安全，下面会有讨论。
2. 为每个并发线程维护一个Session，而不是将对象从一个Session复制到另一个Session，通常使用Session.merge()方法将对象的状态复制到一个不同Session的新的本地对象中。
```





## model和session是强绑定的：[解决 SQLAlchemy 提示 Instance is not bound to a Session 错误的问题](https://www.cnblogs.com/btxlc/p/12400897.html)

`SQLAlchemy`的ORM方式将数据库中的记录映射成了我们定义好的模型类，但是带来一个问题是，这些类对象的实例只在数据库会话（session）的生命期内有效，假如我将数据库会话关闭了，再访问数据表类的对象就会报错。
如下面这段简单的示例代码：

```pgsql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'USER'

    id = Column(Integer, Sequence('USER_SEQ'), primary_key=True, autoincrement=True)
    name = Column(String(30))
    age = Column(Integer)
    status = Column(String(30))


engine = create_engine(str(db_url), encoding=b'utf-8', echo=echo, convert_unicode=True)
Session = sessionmaker(bind=engine)
session = Session()

user = User(name='John', age=30)
session.add(user)
session.commit()
session.close()   # 关闭后访问就会报错

print user.name
```

**运行到最后一行会抛出异常：**



# ref

[Python多进程时SQLAlchemy查询缓存引发的数据无法更新 - 穆琪的博客](https://muhongqiao.top/post/380.html)





# 待看

[SQLAlchemy 中的 Session、sessionmaker、scoped_session - 长安223 - 博客园](https://www.cnblogs.com/ChangAn223/p/11277468.html)

[Python: SQLAlchemy、engine、session 与多线程_python sqlalchemy 多线程-CSDN博客](https://blog.csdn.net/fengbohello/article/details/121475598)

