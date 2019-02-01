import sys, re, string, operator

# 数据栈，后进相出数据结构
stack = []
# 数据堆，用于动态内存的分配和释放，如创建列表和对象
heap = {}

# 1. 读取数据文件
def read_file():
    # 取栈顶文件路径
    f = open(stack.pop())
    # 数据文件读取结果入栈
    stack.append([f.read()])
    f.close()

# 2. 优化待处理文本
def filter_chars():
    # FIXME: 正则表达式过于高层
    stack.append(re.compile(r'[\W_]+'))
    # 出栈，小写化文本，非字母、数字字符串替换为空白
    # 入栈，处理后文本
    stack.append(
        [stack.pop().sub(' ', stack.pop()[0]).lower()]
    )

# 3. 扫描单词
def scan_words():
    # FIXME: split 为字符串高级实现
    # 出栈，空白符分割文本为单词，入栈
    stack.extend(stack.pop()[0].split())

# 4. 移除停止词
def remove_stop_words():
    f = open('../stop_words.txt')
    stack.append(f.read().split(','))
    f.close()
    # 增加单字母
    stack[-1].extend(list(string.ascii_lowercase))
    # 存储需要滤除的单词
    heap['stop_words'] = stack.pop()
    heap['words'] = []
    # 循环处理文本中单词
    while len(stack) > 0:
        # （停止词出栈入堆后）检查栈顶单词是否为停止词
        if stack[-1] in heap['stop_words']:
            stack.pop()
        # 非停止词单词存入堆中变量等待批量入栈
        else:
            heap['words'].append(stack.pop())
    stack.extend(heap['words']) # 过滤后单词
    del heap['stop_words']; del heap['words']

# 5. 计算词频
def frequencies():
    heap['word_freqs'] = {}
    # Forth 风格特色
    while len(stack) > 0:
        if stack[-1] in heap['word_freqs']:
            stack.append(heap['word_freqs'][stack[-1]]) # 已存储的频数
            stack.append(1) # 1 操作数入栈
            stack.append(stack.pop() + stack.pop()) # 1 频数 +，更新频数
        else:
            stack.append(1)
        # 更新后词频重新入堆
        heap['word_freqs'][stack.pop()] = stack.pop()

    stack.append(heap['word_freqs'])
    del heap['word_freqs']

# 6. 词频排序
def sort():
    stack.extend(sorted(stack.pop().items(), key = operator.itemgetter(1)))

# 主函数
stack.append(sys.argv[1])
read_file(); filter_chars(); scan_words(); remove_stop_words()
frequencies(); sort()

# 7. 取 top25
stack.append(0)
# 排序后数据栈取 top25
while stack[-1] < 25 and len(stack) > 1:
    heap['i'] = stack.pop()
    (w, f) = stack.pop()
    print(w, ' - ', f)
    # 更新循环计数 i 1 +
    stack.append(heap['i']); stack.append(1)
    stack.append(stack.pop() + stack.pop())
