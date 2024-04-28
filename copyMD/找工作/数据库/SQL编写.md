---
title: SQL编写
top: false
cover: false
toc: true
mathjax: true
draft: true
date: 2024-03-14 15:27:31
password:
summary:
tags:
- 计数据库
categories:
- find JOB

---



# 基础

```
## 注释
SELECT *
FROM mytable; -- 注释
/* 注释1
   注释2 */
```



数据库创建与使用：

```sql
CREATE DATABASE test;
USE test;
```





# 创建表

```
CREATE TABLE mytable (
  # int 类型，不为空，自增
  id INT NOT NULL AUTO_INCREMENT,
  # int 类型，不可为空，默认值为 1，不为空
  col1 INT NOT NULL DEFAULT 1,
  # 变长字符串类型，最长为 45 个字符，可以为空
  col2 VARCHAR(45) NULL,
  # 日期类型，可为空
  col3 DATE NULL,
  # 设置主键为 id
  PRIMARY KEY (`id`));
  
  
  CREATE TABLE mytable (
  列名， 类型， 是否空， 自增
  )
```





# 修改表

```
添加列

ALTER TABLE mytable
ADD col CHAR(20);
```

删除表

```sql
DROP TABLE mytable;
```



# 数据处理 CRUD



## 插入



普通插入

```sql
INSERT INTO mytable(col1, col2)
VALUES(val1, val2);
```

插入检索出来的数据

```sql
INSERT INTO mytable1(col1, col2)
SELECT col1, col2
FROM mytable2;
```

## 更新

```sql
UPDATE mytable
SET col = val
WHERE id = 1;
```

## 删除

```sql
DELETE FROM mytable
WHERE id = 1;
```

**TRUNCATE TABLE** 可以清空表，也就是删除所有行。

```sql
TRUNCATE TABLE mytable;
```

当涉及多个表时，可以使用`DELETE JOIN`语句来从多个表中删除数据。以下是一个示例：

```sql
DELETE t1, t2
FROM table1 t1
JOIN table2 t2 ON t1.id = t2.id
WHERE condition;
```

## 查询

### DISTINCT

**相同值只会出现一次。它作用于所有列，也就是说所有列的值都相同才算相同。**

```sql
SELECT DISTINCT col1, col2
FROM mytable;
```

### LIMIT

**限制返回的行数**。可以有**两个参数，第一个参数为起始行，从 0 开始；第二个参数为返回的总行数。**

返回前 5 行：

```sql
SELECT *
FROM mytable
LIMIT 5;
```

**返回第 3 ~ 5 行：**

```sql
SELECT *
FROM mytable
LIMIT 2, 3;
```

### 过滤where

不进行过滤的数据非常大，导致通过网络传输了多余的数据，从而浪费了网络带宽。因此尽量使用 SQL 语句来过滤不必要的数据，而不是传输所有的数据到客户端中然后由客户端进行过滤。

```sql
SELECT *
FROM mytable
WHERE col IS NULL;
```

下表显示了 WHERE 子句可用的操作符

| 操作符  |     说明     |
| :-----: | :----------: |
|    =    |     等于     |
|    <    |     小于     |
|    >    |     大于     |
|  <> !=  |    不等于    |
|  <= !>  |   小于等于   |
|  >= !<  |   大于等于   |
| BETWEEN | 在两个值之间 |
| IS NULL |  为 NULL 值  |

## 排序

- **ASC** ：升序（默认）
- **DESC** ：降序

可以按多个列进行排序，并且为每个列指定不同的排序方式：

```sql
SELECT *
FROM mytable
ORDER BY col1 DESC, col2 ASC;
```

## 通配符(where xxx like)

通配符也是用在过滤语句中，但它只能用于文本字段。

- **%** 匹配 >=0 个任意字符；
- **_** 匹配 ==1 个任意字符；
- **[ ]** 可以匹配集合内的字符，例如 [ab] 将匹配字符 a 或者 b。用脱字符 ^ 可以对其进行否定，也就是不匹配集合内的字符。

使用 Like 来进行通配符匹配。

```sql
SELECT *
FROM mytable
WHERE col LIKE '[^AB]%'; -- 不以 A 和 B 开头的任意文本
```

## 函数

各个 DBMS 的函数都是不相同的，因此不可移植，以下主要是 MySQL 的函数

### 汇总

|  函 数  |      说 明       |
| :-----: | :--------------: |
|  AVG()  | 返回某列的平均值 |
| COUNT() |  返回某列的行数  |
|  MAX()  | 返回某列的最大值 |
|  MIN()  | 返回某列的最小值 |
|  SUM()  |  返回某列值之和  |



### OVER(PARTITION BY)函数介绍

**over函数的写法**：

　　over（partition by class order by sroce） 按照sroce排序进行累计，order by是个默认的开窗函数，按照class分区。

**开窗的窗口范围：**

　　over（order by sroce range between 5 preceding and 5 following）：窗口范围为当前行数据幅度减5加5后的范围内的。

　　over（order by sroce rows between 5 preceding and 5 following）：窗口范围为当前行前后各移动5行。


## 分组

把具有相同的数据值的行放在同一组中。

**若要在 SQL 查询中使用`GROUP BY`对多个属性进行分组**

多属性例题：[1280. 学生们参加各科测试的次数 - 力扣（LeetCode）](https://leetcode.cn/problems/students-and-examinations/?envType=study-plan-v2&envId=sql-free-50)

多个属性分组是指：只要有一个不同就是不同

**HAVING**：

- **`HAVING`子句通常用于在对结果集进行分组后对分组数据进行过滤。**
- 它用于条件筛选汇总数据，基于聚合函数（如SUM、COUNT等）的结果。

可以对同一分组数据使用汇总函数进行处理，例如求分组数据的平均值等。

指定的分组字段除了能按该字段进行分组，也会自动按该字段进行排序。

```sql
SELECT column1, COUNT(*)
FROM table_name
GROUP BY column1
HAVING COUNT(*) > 10;

```

假设`mytable`表包含以下数据：

```
复制代码|  col   |
|--------|
|   A    |
|   B    |
|   A    |
|   C    |
|   B    |
```

应用上述查询语句后，将获得以下结果：

```
复制代码|  col   |  num  |
|--------|-------|
|   A    |   2   |
|   B    |   2   |
|   C    |   1   |
```

这些结果显示了`col`列中每个唯一值的出现次数。

GROUP BY 自动按分组字段进行排序，ORDER BY 也可以按汇总字段来进行排序。

```sql
SELECT col, COUNT(*) AS num
FROM mytable
GROUP BY col
ORDER BY num;
```

## 子查询

**子查询可以返回单个值，也可以返回一个结果集（表）**,例题（返回表）： [184. 部门工资最高的员工 - 力扣（LeetCode）](https://leetcode.cn/problems/department-highest-salary/)

```
SELECT
    D.NAME Department,
    E.NAME Employee,
    E.Salary
FROM
    Employee E,
    Department D,
    (SELECT max(Salary) as Salary, departmentId from Employee group by departmentId) as M
where 
    E.departmentId = D.id and
    E.departmentId = M.departmentId and
    E.Salary = M.Salary;
```

**如果子查询中使用了 `SELECT` 语句而没有聚合函数（关键），那么它可能返回一个结果集（表），这时候我们称之为子查询返回了一个表。例如：**



**查询语句可以访问上一级查询语句中引用的表。这种查询方式称为关联子查询或相关子查询。（但是不能直接访问同层级的表。）**



可以将子查询的结果作为 WHRER 语句的过滤条件：

用于从`Customers`表中选择每个客户的名称`cust_name`以及与其关联的订单数量。

```sql
# 使用上一个层级的样例
SELECT cust_name, (SELECT COUNT(*)
                   FROM Orders
                   WHERE Orders.cust_id = Customers.cust_id)
                   AS orders_num
FROM Customers
ORDER BY cust_name;
```

## 连接

通俗的理解就是先在一个表查询，然后在另外一个表查询，判断查询出来的行们之间遍历做检索。

**如果在连接两个表时没有指定任何条件，那么会产生笛卡尔积（Cartesian Product），即两个表的每一行都与另一个表的每一行进行组合，返回结果集中的行数为两个表的行数乘积。（从结果上来说，行数变成两个表行数的乘积，列数变为两个表列数的和）**

**连接用于连接多个表，使用 JOIN 关键字，并且条件语句使用 ON 而不是 WHERE。**

连接可以替换子查询，并且比子查询的效率一般会更快。

可以**用 AS 给列名、计算字段和表名取别名，给表名取别名是为了简化 SQL 语句以及连接相同表。**

### 内连接

**内连接又称等值连接，使用 INNER JOIN 关键字。**

```sql
SELECT A.value, B.value
FROM tablea AS A INNER JOIN tableb AS B
ON A.key = B.key;
```

### 自连接

例题：[196. 删除重复的电子邮箱 - 力扣（LeetCode）](https://leetcode.cn/problems/delete-duplicate-emails/submissions/511838665/)

删除表内重复的元素。

自连接可以看成内连接的一种，只是连接的表是自身而已。

一张员工表，包含员工姓名和员工所属部门，要找出与 Jim 处在同一部门的所有员工姓名。

子查询版本

```sql
SELECT name
FROM employee
WHERE department = (
      SELECT department
      FROM employee
      WHERE name = "Jim");
```





### 外连接

外连接保留了没有关联的那些行。分为左外连接，右外连接以及全外连接，**左外连接就是保留左表没有关联的行。(也就是左边的表里面所有的能够有的行都会保留，如果其在右表查不到，就会补null)**

检索所有顾客的订单信息，包括还没有订单信息的顾客。

```sql
SELECT Customers.cust_id, Customer.cust_name, Orders.order_id
FROM Customers LEFT OUTER JOIN Orders
ON Customers.cust_id = Orders.cust_id;
```





## 组合查询

使用 **UNION** 来组合两个查询，如果第一个查询返回 M 行，第二个查询返回 N 行，那么组合查询的结果一般为 M+N 行。

**每个查询必须包含相同的列、表达式和聚集函数。（两个表的查询出来的东西字段要一致）**

默认会去除相同行，如果需要保留相同行，使用 UNION ALL。

只能包含一个 ORDER BY 子句，并且必须位于语句的最后。

```sql
SELECT col
FROM mytable
WHERE col = 1
UNION
SELECT col
FROM mytable
WHERE col =2;
```





## 视图（逻辑上聚合几个表形成一个新表）

**视图是虚拟的表，本身不包含数据，也就不能对其进行索引操作（索引加快检索）。**

对视图的操作和对普通表的操作一样。

视图具有如下好处：

- 简化复杂的 SQL 操作，比如复杂的连接；
- 只使用实际表的一部分数据；
- 通过只给用户访问视图的权限，保证数据的安全性；
- 更改数据格式和表示。

```sql
CREATE VIEW myview AS
SELECT Concat(col1, col2) AS concat_col, col3*col4 AS compute_col
FROM mytable
WHERE col5 = val;
```





## 存储过程（类似于函数）

存储过程可以看成是对一系列 SQL 操作的批处理。

使用存储过程的好处：

- 代码封装，保证了一定的安全性；
- 代码复用；
- 由于是预先编译，因此具有很高的性能。

命令行中创建存储过程需要自定义分隔符，因为命令行是以 ; 为结束符，而存储过程中也包含了分号，因此会错误把这部分分号当成是结束符，造成语法错误。

包含 in、out 和 inout 三种参数。

给变量赋值都需要用 select into 语句。

每次只能给一个变量赋值，不支持集合的操作。

```sql
# 这段代码执行了一个存储过程，通过计算mytable表中col1列的总和的平方，并将结果返回。

delimiter //

create procedure myprocedure( out ret int )
    begin
        declare y int;
        select sum(col1)
        from mytable
        into y;
        select y*y into ret;
    end //

delimiter ;
call myprocedure(@ret);
select @ret;
```



## 游标

**游标 (Cursor)**：是一个数据库对象，用于在SQL查询结果集上进行迭代处理。游标提供了对查询结果集的行级别访问，使得可以逐行处理结果集，类似于编程语言中的迭代器。**游标通常用于需要逐行处理结果集的情况。**

游标主要用于交互式应用，其中用户需要对数据集中的任意行进行浏览和修改。

使用游标的四个步骤：

1. 声明游标，这个过程没有实际检索出数据；
2. 打开游标；
3. 取出数据；
4. 关闭游标；

```sql
delimiter //
create procedure myprocedure(out ret int)
    begin
        declare done boolean default 0;

        declare mycursor cursor for
        select col1 from mytable;
        # 定义了一个 continue handler，当 sqlstate '02000' 这个条件出现时，会执行 set done = 1
        declare continue handler for sqlstate '02000' set done = 1;

        open mycursor;

        repeat
            fetch mycursor into ret;
            select ret;
        until done end repeat;

        close mycursor;
    end //
 delimiter ;
```



## 触发器

触发器会在某个表执行以下语句时而自动执行：DELETE、INSERT、UPDATE。



## 事务管理

**事务管理是数据库系统中用于确保数据的一致性、完整性和持久性的重要机制。通过将一系列数据库操作（SQL语句）组合成一个逻辑工作单元，事务可以确保这些操作要么全部成功执行，要么完全不执行，从而避免数据异常和不一致性。（ACID）**

基本术语：

- 事务（transaction）指一组 SQL 语句；
- 回退（rollback）指撤销指定 SQL 语句的过程；
- 提交（commit）指将未存储的 SQL 语句结果写入数据库表；
- 保留点（savepoint）指事务处理中设置的临时占位符（placeholder），你可以对它发布回退（与回退整个事务处理不同）。

不能回退 SELECT 语句，回退 SELECT 语句也没意义；也不能回退 CREATE 和 DROP 语句。

MySQL 的事务提交默认是隐式提交，每执行一条语句就把这条语句当成一个事务然后进行提交。当出现 START TRANSACTION 语句时，会关闭隐式提交；当 COMMIT 或 ROLLBACK 语句执行后，事务会自动关闭，重新恢复隐式提交。

```sql
START TRANSACTION;  -- 开始事务

-- 执行一系列数据库操作，如INSERT、UPDATE、DELETE等

COMMIT;  -- 提交事务，如果所有操作成功，则将更改保存到数据库
-- 或者
ROLLBACK; -- 回滚事务，如果出现错误或需要撤销操作，将取消之前的更改

-- 结束事务

```





# 关于null的各种判断



**IS NULL**：用于检查值是否为 NULL。

```
SELECT column_name
FROM table_name
WHERE column_name IS NULL;
```

**IS NOT NULL**：用于检查值是否不为 NULL。

```sql
sql复制代码SELECT column_name
FROM table_name
WHERE column_name IS NOT NULL;
```

# where的顺序

where的顺序是在连接后的。所有时候建议先连接再从连接的集合里面考虑使用where。例题：[183. 从不订购的客户 - 力扣（LeetCode）](https://leetcode.cn/problems/customers-who-never-order/)

# if语句

#### IF 表达式

```sql
IF( expr1 , expr2 , expr3 )
```

expr1 的值为 TRUE，则返回值为 expr2 
expr1 的值为FALSE，则返回值为 expr3



# ref

[SQL 练习 | CS-Notes 面试笔记](https://cyc2018.xyz/%E6%95%B0%E6%8D%AE%E5%BA%93/SQL%20%E7%BB%83%E4%B9%A0.html#_595-big-countries)



