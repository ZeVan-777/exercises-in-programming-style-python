from abc import ABCMeta, abstractmethod
import sys, re, string

class AcceptTypes():
    def __init__(self, *args):
        self._args = args
    
    def __call__(self, f):
        def wrapped_f(*args):
            for i in range(len(self._args)):
                if self._args[i] == 'primitive' and type(args[i + 1]) in (str, int, float, bool):
                    continue
                if not isinstance(args[i + 1], globals()[self._args[i]]):
                    raise TypeError("Wrong Type")
                
            f(*args)
               
        return wrapped_f


class IDataStorage(metaclass=ABCMeta):
    
    @abstractmethod
    def words(self):
        pass

class IStopWordFilter(metaclass=ABCMeta):
    
    @abstractmethod
    def is_stop_word(self, word):
        pass

class IWordFrequencyCounter(metaclass=ABCMeta):
    
    @abstractmethod
    def increase_count(self, word):
        pass
    
    @abstractmethod
    def sorted(self, word):
        pass
   
class DataStorageManager(IDataStorage):
    _data = ''
    
    @AcceptTypes('primitive', 'IStopWordFilter')
    def __init__(self, path_to_file, word_filter):
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile(r'[\W_]+')        
        self._data = pattern.sub(' ', self._data).lower()
        self._data = ''.join(self._data).split()
        self._stop_word_filter = word_filter
    
    def words(self):
        return [w for w in self._data if not self._stop_word_filter.is_stop_word(w)]

class StopWordManager(IStopWordFilter):
    _stop_words = []
    
    def __init__(self):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))
    
    def is_stop_word(self, word):
        return word in self._stop_words
             

class WordFrequencyManager(IWordFrequencyCounter):
    _word_freqs = {}

    def increase_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1
    
    def sorted(self):
        return sorted(self._word_freqs.items(), key=lambda wf: wf[1], reverse=True)

class WordFrequencyController:
    @AcceptTypes('IDataStorage', 'IWordFrequencyCounter')
    def __init__(self, data_storage, word_freq_counter):
        self._storage = data_storage
        self._word_freq_counter = word_freq_counter

    def run(self):
        for w in self._storage.words():
                self._word_freq_counter.increase_count(w)
        
        word_freqs = self._word_freq_counter.sorted()
        for (w, f) in word_freqs[0: 25]:
            print(w, ' - ', f)

stop_word_manager = StopWordManager()
storage = DataStorageManager(sys.argv[1], stop_word_manager)
word_freq_counter = WordFrequencyManager()
WordFrequencyController(storage, word_freq_counter).run()
