import sys, string

# 词频数据对列表
word_freqs = []

# 停止词列表
with open('../stop_words.txt') as f:
    stop_words = f.read().split(',')
stop_words.extend(list(string.ascii_lowercase))

# 逐行迭代文件
for line in open(sys.argv[1]):
    # （行内单词）首字符索引
    start_char = None
    # 行字符索引
    i = 0
    for c in line:
        if start_char == None:
            if c.isalnum():
                start_char = i
        else:
            # 行索引到达单词终点
            if not c.isalnum():
                # 此单词是否已存在词频数据
                found = False
                word = line[start_char:i].lower()
                # 忽略停止词
                if word not in stop_words:
                    # 词频对在列表中索引
                    wf_index = 0
                    for wf in word_freqs:
                        if word == wf[0]:
                            wf[1] += 1
                            found = True
                            break
                        wf_index += 1
                    if not found:
                        word_freqs.append([word, 1])                       
                    # 更新[单词, 频数]对的列表排序前移
                    elif len(word_freqs) > 1:
                        # 频数+1后词频对在列表中冒泡
                        for n in reversed(range(wf_index)):
                            if word_freqs[wf_index][1] > word_freqs[n][1]:
                                # 交换
                                word_freqs[n], word_freqs[wf_index] = word_freqs[wf_index], word_freqs[n]
                                wf_index = n                                
                            else: # 没有比前面的数更大，终止冒泡
                                break 
                # （单词处理完成后）重置
                start_char = None
        i += 1
    
for wf in word_freqs[0:25]:
    print(wf[0], ' - ', wf[1])  
