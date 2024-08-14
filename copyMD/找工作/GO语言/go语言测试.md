---
title: go测试
top: false
cover: false
toc: true
mathjax: true
date: 2024-07-22 15:27:31
password:
summary:
tags:
- go
categories:
- find JOB
---



# 背景

正在编写go的测试用例case，但是对基本流程不熟。

建议还是用goland开发，用vscode有点难受



# 方法



在Go语言中，编写测试函数和设计测试用例是非常重要的部分，特别是在开发过程中确保代码的正确性和稳定性。Go语言内置了一个强大的测试框架，位于`testing`包中。以下是如何编写测试函数和设计测试用例的详细指南。

### 编写测试函数

1. **创建测试文件**：**测试文件的命名必须以 `_test.go` 结尾。例如，如果你有一个名为 `math.go` 的文件，那么相应的测试文件应该命名为 `math_test.go`。**

2. **导入 `testing` 包**：在测试文件中，导入 `testing` 包。

3. **编写测试函数**：测**试函数的命名必须以 `Test` 开头，并且接受一个指向 `testing.T` 类型的指针作为参数。例如：**

```go
package math

import "testing"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    expected := 5
    if result != expected {
        t.Errorf("Add(2, 3) = %d; want %d", result, expected)
    }
}
```

### 设计测试用例

设计测试用例时，需要考虑各种可能的输入和边界情况。以下是一些常见的测试用例设计方法：

1. **正常情况**：测试函数在正常输入下的行为。
2. **边界情况**：测试函数在边界输入下的行为，例如空输入、最大值、最小值等。
3. **错误情况**：测试函数在错误输入下的行为，例如负数、非数字字符等。

### 示例

假设我们有一个简单的 `Add` 函数，定义如下：

```go
package math

func Add(a, b int) int {
    return a + b
}
```

我们可以为这个函数编写多个测试用例：

```go
package math

import "testing"

func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"zero and positive number", 0, 5, 5},
        {"negative and positive number", -1, 1, 0},
        {"two negative numbers", -2, -3, -5},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d", tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

### 运行测试

在命令行中，使用以下命令运行测试：

```sh
go test
```

这将自动查找当前目录下所有以 `_test.go` 结尾的文件，并运行其中的测试函数。

### 其他测试功能

- **基准测试**：用于测试函数的性能，函数名以 `Benchmark` 开头。
- **示例测试**：用于生成文档和验证代码示例，函数名以 `Example` 开头。

### 基准测试示例

```go
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(2, 3)
    }
}
```

### 示例测试示例

```go
func ExampleAdd() {
    fmt.Println(Add(2, 3))
    // Output: 5
}
```

通过这些步骤和示例，你可以在Go语言中编写和设计有效的测试用例，确保代码的质量和可靠性。
