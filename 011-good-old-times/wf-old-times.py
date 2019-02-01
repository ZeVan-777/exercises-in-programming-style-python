import sys, os

# 文件缓存（覆盖式）新建并返回
def touchopen(filename, *args, **kwargs):
    try:
        os.remove(filename)
    except OSError:
        pass
    # touch <filename>
    open(filename, "a").close()
    return open(filename, *args, **kwargs)

# 指代申请的内存空间
data = []

# 一、划分内存空间 —— 初始化
# 无标识符的限制 => 注释内存单元
f = open('../stop_words.txt')
data = [f.read(1024).split(',')] # data[0] - 需要滤除的停止词
f.close()

data.append([])                  # data[1] - 数据行（≤ 80 chars）
data.append(None)                # data[2] - 当前处理单词的首字符行索引
data.append(0)                   # data[3] - 当前处理字符行索引
data.append(False)               # data[4] - 是否在辅存中找到当前处理单词
data.append('')                  # data[5] - 当前处理单词
data.append('')                  # data[6] - 辅存中，当前处理单词词-频数据
data.append(0)                   # data[7] - 当前处理单词频数

# 创建新的词频统计文件（辅存），且支持 binary mode 写入文件末尾
word_freqs = touchopen('word_freqs', 'rb+')
# 打开数据文件，支持读取
f = open(sys.argv[1], 'r')

# 二、处理数据文件
while True:
    data[1] = [f.readline()]
    # 文件末尾 —— （行处理）循环终止条件
    if data[1] == ['']:
        break
    # 补全行末换行符
    if data[1][0][len(data[1][0]) - 1] != '\n':
        data[1][0] = data[1][0] + '\n'
    # 重置行索引
    data[2] = None
    data[3] = 0
    # 行字符循环
    # FIXME: 尝试通过索引遍历数据行
    for c in data[1][0]:
        # 没有正在处理的单词，找单词开头
        if data[2] == None:
            if c.isalnum():
                data[2] = data[3]
        else:
            # 2.1 单词结尾 => 行数据中截取出待处理单词
            if not c.isalnum():
                # 重置辅存记录查找的标志位
                data[4] = False
                data[5] = data[1][0][data[2]:data[3]].lower()
                # 滤除停止词及短单词
                if data[5] not in data[0] and len(data[5]) >= 2:
                    # 2.2（word_freqs 中查询）是否已有统计数据
                    while True:
                        data[6] = str(word_freqs.readline().strip(), 'utf-8')
                        if data[6] == '':
                            break
                        data[7] = int(data[6].split(',')[1])
                        data[6] = data[6].split(',')[0].strip()
                        # 当前处理单词有匹配词频记录，介绍查询
                        if data[5] == data[6]:
                            data[7] += 1
                            data[4] = True
                            break
                    # 2.3 新增、更新辅存记录
                    if not data[4]:
                        word_freqs.seek(0, 1)
                        word_freqs.write(bytes("%20s,%04d\n" % (data[5], 1), 'utf-8'))
                    else:
                        word_freqs.seek(-26, 1)
                        word_freqs.write(bytes("%20s,%04d\n" % (data[5], data[7]), 'utf-8'))
                    # 移动文件读取指针到文件开头
                    word_freqs.seek(0,0)
                data[2] = None
        # 更新行字符索引
        data[3] += 1

f.close()
word_freqs.flush()

# 三、分析、统计辅存中记录 => top25
# 约束：不可使用内存中数据
del data[:]

data = data + [[]] * (25 - len(data)) # data[0:25] 存储当前 top 25
data.append('') # data[25] - word,freq
data.append(0)  # data[26] - 词频

while True:
    data[25] = str(word_freqs.readline().strip(), 'utf-8')
    if data[25] == '': # EOF
        break
    data[26] = int(data[25].split(',')[1])    # freq
    data[25] = data[25].split(',')[0].strip() # word
    # 当前 word,freq 是否大于目前 top 25
    for i in range(25):
        if data[i] == [] or data[i][1] < data[26]:
            data.insert(i, [data[25], data[26]])
            del data[26] # 删除被挤出 top25 的 [<word>, <freq>]
            break


for wf in data[0:25]:
    if len(wf) == 2:
        print(wf[0], ' - ', wf[1])

word_freqs.close()
