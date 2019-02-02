import sys, re, string
#
# 单子类
#
class WFTHeOne:
    def __init__(self, v):
        self._value = v
    
    def bind(self, func):
        self._value = func(self._value)
        return self
    
    def printme(self):
        print(self._value)

#
# 函数
#
def read_file(path_to_file):
    with open(path_to_file) as f:
        data = f.read()
    return data

def filter_chars(text):
    pattern = re.compile(r'[\W_]+')
    return pattern.sub(' ', text)

def normalize(text):
    return text.lower()

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

def top25(wfRankList):
    top25 = ""
    for (w, f) in wfRankList[0:25]:
        top25 += str(w) + ' - ' + str(f) + '\n'
    return top25

WFTHeOne(sys.argv[1])\
    .bind(read_file)\
    .bind(filter_chars)\
    .bind(normalize)\
    .bind(scan_Words)\
    .bind(remove_stop_words)\
    .bind(frequencies)\
    .bind(sort)\
    .bind(top25)\
    .printme()