# 单子风格

## 约束

- 有一个可以修改数据的抽象
- 抽象提供三个操作：1.封装数据；2.将若干函数逐个绑定，建立函数调用顺序；3.打开封装，查看数据的最终结果

## 注解

单子风格是顺序调用函数的另一种变体，不同于其他传统的函数组合方式，我们建立了在**值与函数之间充当胶水的抽象方式**——“单子”。它包括两个主要操作：

1. 封装操作，输入一个简单值并返回一个胶水抽象的实例
2. 绑定操作，将封装的数据传递给函数

```python
class WFTHeOne:
    def __init__(self, v):
        self._value = v

    def bind(self, func):
        self._value = func(self._value)
        return self

    def printme(self):
        print(self._value)
```

## 发展历程

单子起源风格起源于 Haskell 的单位原子。Haskell 是有着严格**零副作用**约束的函数式编程语言。Haskell 的设计者使用单子，来定义程序中概念，如状态、异常等。
