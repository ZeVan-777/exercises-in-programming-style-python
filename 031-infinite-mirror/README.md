# 无限镜像风格

## 约束

- 使用归纳法对问题或其核心部分进行建模，即已知 `n = 0`时情况和`n`到`n+1`的推导规则

## 注解

在计算机应用中，归纳法常用**递归**表示。

示例程序使用了两次归纳法：词频统计`count`、输出词频统计结果`wf_print`。方法基本相同，首先**检查基本情况** —— 空列表时停止递归调用；然后**确定处理一般情况的规则** —— 先处理列表头部，再递归调用函数处理列表的其他元素。

直观来看，归纳法推导方向与函数递归调用顺序相反。但如果将函数调用看做一个**问题传递、返回的过程** —— 调用栈入栈、出栈。而递归则进一步强调每一次解决问题的函数相同 —— 同一逻辑加工上一出栈函数的结果。

``` python
def count(words, stop_words, word_freqs):
    if len(words) == 0:
        return
    # head word
    word = words[0]
    if word not in stop_words:
        if word in word_freqs:
            word_freqs[word] += 1
        else:
            word_freqs[word] = 1
    # tail words
    count(words[1:], stop_words, word_freqs)
```

逻辑上可以无限归纳，但内存有限。过长的调用栈最终会导致栈内存耗尽溢出。因此，我们不对整个单词列表运行`count`，而是先将单词列表分为`N块`：

``` python
# 单词列表每一块单词数 —— 递归深度
RECURSIVE_LIMIT = 3000
# 调用栈深度，在递归深度上适当增加
sys.setrecursionlimit(RECURSIVE_LIMIT + 50)

# ...

for i in range(0, len(words), RECURSIVE_LIMIT):
    count(words[i: i+RECURSIVE_LIMIT], stop_words, word_freqs)
```

**尾调用**是指一个函数的最后一个动作是函数调用，**尾递归**即在函数的尾部发生递归调用。尾调用返回时栈中不需要其他操作，先前的栈记录可以安全的删除 —— **尾调用优化**。函数调用过程变成了**迭代**，有效节省了内存和时间。然而，Python 并不进行尾调用优化，因此手动限制了调用栈深度。
