import sys, re
# 限制递归深度（过大可能栈溢出）
RECURSIVE_LIMIT = 3000
# 调用栈深度适当增加
sys.setrecursionlimit(RECURSIVE_LIMIT + 50)

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

def wf_print(word_freqs):
    if len(word_freqs) == 0:
        return
    (w, f) = word_freqs[0]
    print(w, ' - ', f)
    wf_print(word_freqs[1:])

stop_words = set(open('../stop_words.txt').read().split(','))

words = re.findall(r'[a-z]{2,}', open(sys.argv[1]).read().lower())

word_freqs = {}

for i in range(0, len(words), RECURSIVE_LIMIT):
    count(words[i: i+RECURSIVE_LIMIT], stop_words, word_freqs)

wf_print(sorted(word_freqs.items(), key=lambda wf: wf[1], reverse=True)[:25])
