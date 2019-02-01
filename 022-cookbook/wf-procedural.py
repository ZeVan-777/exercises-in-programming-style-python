import sys, string

# （过程函数）共享状态数据
data = []
words = []
# 需要频繁查询、更新词频数据
word_freqs = {}

""" 
过程
"""
def read_file(path_to_file):
    global data
    with open(path_to_file) as f:
        data.extend(f.read())

def filter_chars_and_normalize():
    global data
    for i,c in enumerate(data):
        # 非字母数字字符替代为空白符
        if not c.isalnum():
            data[i] = ' '
        else:
            data[i] = c.lower()

def scan_Words():
    global data
    global words
    # 拼接文本数据字符串，通过空白符分割出单词
    data_str = ''.join(data)
    words.extend(data_str.split())

def remove_stop_words():
    global words
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    # 需要滤除的停止词在 words 中索引
    indexes = []
    for i in range(len(words)):
        if words[i] in stop_words:
            indexes.append(i)
    # 反向迭代，出栈索引查找更快
    for i in reversed(indexes):
        words.pop(i)

def frequencies():
    global words
    global word_freqs
    for w in words:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1

def sort():
    global word_freqs
    word_freqs = sorted(word_freqs.items(), key = lambda wf: wf[1])

""" 
主函数
"""
read_file(sys.argv[1])
filter_chars_and_normalize()
scan_Words()
remove_stop_words()
frequencies()
sort()

for (w, f) in reversed(word_freqs[-25:]):
    print(w, ' - ', f)
