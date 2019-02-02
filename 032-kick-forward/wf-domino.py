import sys, re, string

def read_file(path_to_file, func):
    with open(path_to_file) as f:
        data = f.read()
    func(data, normalize)

def filter_chars(text, func):
    pattern = re.compile(r'[\W_]+')
    func(pattern.sub(' ', text), scan_words)

def normalize(text, func):
    func(text.lower(), remove_stop_words)

def scan_words(text, func):
    func(text.split(), frequencies)

def remove_stop_words(words, func):
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    func([w for w in words if not w in stop_words], sort)

def frequencies(words, func):
    word_freqs = {}
    for w in words:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    func(word_freqs, print_text)

def sort(word_freqs, func):
    func(sorted(word_freqs.items(), key=lambda wf:wf[1], reverse=True), no_operate)

def print_text(wfRankList, func):
    for (w, f) in wfRankList[0:25]:
        print(w, ' - ', f)
    func(None)

def no_operate(func):
    return

#
# 主函数
#
read_file(sys.argv[1], filter_chars)