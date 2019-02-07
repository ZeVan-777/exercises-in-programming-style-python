import sys, re, string

def extract_words(obj, path_to_file):
    with open(path_to_file) as f:
        obj['data'] = f.read()
    pattern = re.compile(r'[\W_]+')
    text = pattern.sub(' ', obj['data']).lower()
    obj['data'] = ''.join(text).split()

def load_stop_words(obj):
    with open('../stop_words.txt') as f:
        obj['stop_words'] = f.read().split(',')
    obj['stop_words'].extend(list(string.ascii_lowercase))

def increase_count(obj, w):
    obj['freqs'][w] = 1 if w not in obj['freqs'] else obj['freqs'][w] + 1

data_storage_obj = {
    'data': [],
    'init': lambda path_to_file: extract_words(data_storage_obj, path_to_file),
    'words': lambda : data_storage_obj['data']
}

stop_words_obj = {
    'stop_words': [],
    'init': lambda : load_stop_words(stop_words_obj),
    'is_stop_word': lambda word: word in stop_words_obj['stop_words']
}

word_freqs_obj = {
    'freqs': {},
    'increase_count': lambda w: increase_count(word_freqs_obj, w),
    'sorted': lambda : sorted(word_freqs_obj['freqs'].items(), key=lambda wf: wf[1], reverse=True)
}

data_storage_obj['init'](sys.argv[1])
stop_words_obj['init']()

for w in data_storage_obj['words']():
    if not stop_words_obj['is_stop_word'](w):
        word_freqs_obj['increase_count'](w)

word_freqs = word_freqs_obj['sorted']()
for (w, f) in word_freqs[0:25]:
    print(w, ' - ', f)
