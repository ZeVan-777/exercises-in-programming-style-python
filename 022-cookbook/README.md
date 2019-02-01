# 食谱风格

## 约束

- 没有长跳转
- 使用**过程**抽象、分解问题。过程是实现某一功能的函数块，它们可能接受输入，但未必产生输出。
- **依次调用**过程函数解决较大问题，这些过程函数 可通过**全局变量**的形式共享变量。

## 注解

食谱风格的过程函数通过**数据共享**来实现最终目标。变量状态的改变可能取决于之前的值 —— 过程函数对这些变量具有**副作用**。运算过程的推进，就是通过一个过程函数处理当前数据，并为下一个过程函数准备数据来完成的。

首先声明共享数据：

```python
data = [] # 数据文本
words = [] # 文本单词
words_freqs = {} # 词频数据，需要频繁查询、更新
```

然后声明一系列过程，操作共享数据

```python
# 1. 通过路径读取文件
def read_file(path_to_file):
    global data    
   	data = data + list(f.read())
# 2. 替换非字母数字字符
def filter_chars_and_normalize():
    global data
    for c in data
        if not c.isalnum():
            data[i] = ' '
# 3. 提取数据文件中单词
def scan_words():
    global data
    global words
    words = words + ''.join(data).split()
# 4. 滤除提取单词中的停止词
def remove_stop_words():
	global words:
    for i,w in enumerate(words)
        if w in stop_words:
            words.pop(i)
# 5. 计算词频
def frequencies():
    global words
    global word_freqs
    for w in words
    	if w in word_freqs
        	word_freqs[w] += 1
# 6. 排序
def sort():
    global word_freqs
    word_freqs = sorted(word_freqs.items(), key = lambda wf: wf[1])
```

**过程函数改变共享变量的状态，就像我们按照食谱进行一步操作时，也会随着步骤的推进改变食材的状态一样。**可变状态会导致过程函数可能**非幂等** —— 多次调用一个过程可能会导致状态和输出结果完全不同。例如调用两次  `read_file(path_to_file)`，变量`data`中数据会翻倍。缺乏幂等性被很多人视为编程错误的一个来源。

## 发展历程

在20世纪60年代，有越来越多的大问题需要解决，这对当时的编程技术提出了一种挑战 —— 让其他人理解程序。编程语言的特色化发展，让同一个程序可以通过许多不同的方式表达。一场关于编程语言中（以理解程序为目的）哪些特征是“好”，哪些“坏”的辩论开始了。某种程度上，Dijkstra 引导了这场辩论，他鼓吹限制使用一些“不好的”编程特征，如长跳转；要多多使用非底层的迭代构造，如`while`循环；过程函数以及代码要适当模块化。这些观点的盛行导致了**结构化编程**时代的来临。

在编程中，食谱风格适用于那些计算过程中外部数据会随着时间的推移变化，且行为也取决于数据的计算任务。本例使用全局变量共享状态，但过程应在**更小的作用域中共享变量**。

在系统层面上，架构中的组件共享并改变外部状态，如同存储在数据库中一样。