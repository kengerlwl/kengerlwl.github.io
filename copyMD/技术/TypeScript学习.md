---
title: TypeScript学习
top: false
cover: false
toc: true
mathjax: true
date: 2025-09-05 15:27:31
password:
summary:
tags:
- ts
categories:
- 技术

---



# demo

我们新建一个 app.ts 的文件，代码如下：

var message:string = "Hello World"  console.log(message)

通常我们使用 **.ts** 作为 TypeScript 代码文件的扩展名。

然后执行以下命令将 TypeScript 转换为 JavaScript 代码：

```
tsc app.ts
```

![img](https://www.runoob.com/wp-content/uploads/2019/01/typescript_compiler.png)

这时候在当前目录下（与 app.ts 同一目录）就会生成一个 app.js 文件，代码如下：

var message = "Hello World"; console.log(message);

使用 node 命令来执行 app.js 文件：

```
$ node app.js 
Hello World
```





# 特性

TypeScript 的一些关键特性：

- **静态类型检查**：TypeScript 在编译时就会检查代码的类型是否匹配，能够发现很多潜在的错误。即使是简单的错误（例如拼写错误或类型不一致），也可以在编写代码时被捕获到。
- **类型推断**：TypeScript 能够自动推断变量的类型。比如当你声明一个变量并赋值时，TypeScript 会根据赋值来推断这个变量的类型，不需要每次都显式声明类型。
- **接口和类型定义**：TypeScript 提供了 `interface` 和 `type` 关键字，允许你定义复杂的数据结构。这对于项目中不同部分的代码协作和数据交互来说非常重要。
- **类和模块支持**：TypeScript 支持面向对象编程中的类（class）概念，增加了构造函数、继承、访问控制修饰符（如 `public`、`private`、`protected`），并且支持 ES 模块化规范。
- **工具和编辑器支持**：TypeScript 拥有良好的编辑器支持，特别是与 Visual Studio Code 集成时，能提供智能提示、自动补全、重构等工具，使开发过程更高效。
- **兼容 JavaScript**：TypeScript 是 JavaScript 的超集，这意味着所有合法的 JavaScript 代码都是合法的 TypeScript 代码。这使得 JavaScript 项目可以逐步迁移到 TypeScript，而无需完全重写。



**总结：ts和java很像了，很多java这边的特性，ts也有，面向对象，枚举，类型，接口，继承，抽象类，泛型。但是细节语法不一样**

同时，ts还有其特性，函数能够脱离类而存在，其模块逻辑和python比较像





# 语法

## let 和 var 都是 JavaScript 中用于声明变量的关键字，但它们有一些重要的区别：

- `let` 推荐用于现代 JavaScript 编码，具有更安全的作用域和更少的意外行为。

### 作用域不同

- **var** 声明的变量是**函数作用域**（function scope），即在函数内部声明的变量在整个函数内都可访问，在函数外声明则为全局变量。
- **let** 声明的变量是**块级作用域**（block scope），即只在最近的一对花括号 `{}` 内有效，比如在 if、for、while、代码块等内部声明的变量只在该块内有效。

### 重复声明

- **var** 允许在同一作用域内重复声明同一个变量，不会报错。
- **let** 不允许在同一作用域内重复声明同一个变量，会报错。

const和let一样，但是是常量。





## 模块

### **模块和命名空间**

TypeScript 提供了基于 ES6 的模块系统，使用 `import` 和 `export` 导入和导出模块。此外，TypeScript 还支持命名空间（Namespace），用于组织代码和避免命名冲突。

```
// math.ts
export function add(a: number, b: number): number {
  return a + b;
}

// main.ts
import { add } from "./math";
console.log(add(2, 3));
```

**必须使用 `export`，否则无法被其他模块导入和使用。**





## 函数声明（Function Declarations）

函数声明：TypeScript 允许声明带有类型注解的函数，包括参数类型和返回值类型。

```
function greet(name: string): string {
  return "Hello, " + name;
}
```

## 类型推断（Type Inference）

TypeScript 在某些情况下会自动推断变量的类型。例如，在声明变量并赋值时，TypeScript 会推断出该变量的类型。

```
let num = 10; *// TypeScript 推断 num 为 number 类型*
```







## 异步编程（Asynchronous Programming）

TypeScript 完全支持异步编程，可以使用 async/await 语法来处理异步操作。

```
async function fetchData(): Promise<string> {
    const response = await fetch("https://example.com");
    const data = await response.text();
    return data;
}
```





## 类

```
class Car { 
    // 字段 
    engine:string; 
 
    // 构造函数 
    constructor(engine:string) { 
        this.engine = engine 
    }  
 
    // 方法 
    disp():void { 
        console.log("发动机为 :   "+this.engine) 
    } 
}
```

实例化：

```
var object_name = new class_name([ arguments ])
```





## 对象

对象是包含一组键值对的实例。 值可以是标量、函数、数组、对象等，如下实例：

```
var object_name = { 
    key1: "value1", // 标量
    key2: "value",  
    key3: function() {
        // 函数
    }, 
    key4:["content1", "content2"] //集合
}
```

