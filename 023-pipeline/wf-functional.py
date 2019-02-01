import sys, re, string, functools

""" 
函数
"""
def read_file(path_to_file):
    with open(path_to_file) as f:
        data = f.read()
    return data

def filter_chars_and_normalize(text):
    pattern = re.compile(r'[\W_]+')
    return pattern.sub(' ', text).lower()

def scan_Words(text):
    return text.split()

def remove_stop_words(words):
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in words if not w in stop_words]


def frequencies(words):
    word_freqs = {}
    for w in words:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

def sort(wfDict):
    return sorted(wfDict.items(), key=lambda wf: wf[1], reverse=True)

def print_all(wfRankList):
    if (len(wfRankList) > 0):
        print(wfRankList[0][0], ' - ', wfRankList[0][1])
        print_all(wfRankList[1:])

# 函数按序拼接为流水线
def pipeline(*funcs):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), reversed(funcs), lambda x: x)

# 主函数
pipeline(
    read_file,
    filter_chars_and_normalize,
    scan_Words,
    remove_stop_words,
    frequencies,
    sort,
    lambda rankList: rankList[0:25],
    print_all,
)(sys.argv[1])