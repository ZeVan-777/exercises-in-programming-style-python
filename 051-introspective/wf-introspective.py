import inspect, string, re, sys

def read_stop_words():
    """ 只能被 extract_words 正常调用 """
    if inspect.stack()[1][3] != 'extract_words':
        return None

    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return stop_words

def extract_words(path_to_file):
    with open(locals()['path_to_file']) as f:
        text = f.read()
    pattern = re.compile(r'[\W_]+')
    word_list = pattern.sub(' ', text).lower().split()
    stop_words = read_stop_words()
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list):
    word_freqs = {}
    for w in locals()['word_list']:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
        
    return word_freqs

def sort(word_freqs):
    return sorted(locals()['word_freqs'].items(), key=lambda wf: wf[1], reverse=True)

def main():
    word_freqs = sort(frequencies(extract_words(sys.argv[1])))
    for (w, f) in word_freqs[:25]:
        print(w, ' - ', f)

if __name__ == "__main__":
    main()
