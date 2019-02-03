import sys, re, string

class DataStorageManager():
    def __init__(self, path_to_file):
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile(r'[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()
    
    def words(self):
        return self._data.split()

class StopWordManager():
    def __init__(self):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, word):
        return word in self._stop_words

class WordFrequencyManager():
    def __init__(self):
        self._word_freqs = {}
    
    def increase_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1
    
    def sort(self):
        return sorted(self._word_freqs.items(), key=lambda wf: wf[1], reverse=True)


class WordFrequencyController():
    def __init__(self, path_to_file):
        self._storage_manager = DataStorageManager(path_to_file)
        self._stop_word_manager = StopWordManager()
        self._word_freq_manager = WordFrequencyManager()
    
    def run(self):
        for w in self._storage_manager.words():
            if not self._stop_word_manager.is_stop_word(w):
                self._word_freq_manager.increase_count(w)
        
        word_freqs = self._word_freq_manager.sort()
        for (w, f) in word_freqs[0:25]:
            print(w, ' - ', f)

WordFrequencyController(sys.argv[1]).run()
