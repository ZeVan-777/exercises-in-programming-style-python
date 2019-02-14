import sys, re, string

class WordFrequencyFramework:
    _load_event_handlers = []
    _dowork_event_handlers = []
    _end_event_handlers = []

    def register_for_load_event(self, handler):
        self._load_event_handlers.append(handler)        
    
    def register_for_dowork_event(self, handler):
        self._dowork_event_handlers.append(handler)        
    
    def register_for_end_event(self, handler):
        self._end_event_handlers.append(handler)
        
    def run(self, path_to_file):
        for h in self._load_event_handlers:
            h(path_to_file)
        for h in self._dowork_event_handlers:
            h()
        for h in self._end_event_handlers:
            h()


class StopWordFilter:
    _stop_words = []
    
    def __init__(self, wfapp):
        wfapp.register_for_load_event(self.__load)
    
    def __load(self, ignore):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, word):
        return word in self._stop_words
 
class DataStorage:
    _data = ''
    _stop_word_filter = None
    _word_event_handlers = []

    def __init__(self, wfapp, stop_word_filter):
        self._stop_word_filter = stop_word_filter
        wfapp.register_for_load_event(self.__load)
        wfapp.register_for_dowork_event(self.__produce_words)
    
    def __load(self, path_to_file):
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile(r'[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()
    
    def __produce_words(self):
        for w in ''.join(self._data).split():
            if not self._stop_word_filter.is_stop_word(w):
                for h in self._word_event_handlers:
                    h(w)
    
    def register_for_work_event(self, handler):
        self._word_event_handlers.append(handler)

class WordFrequencyCounter:
    word_freqs = {}

    def __init__(self, wfapp, data_storage):
        data_storage.register_for_work_event(self.__increase_count)
    
    def __increase_count(self, word):
        if word in self.word_freqs:
            self.word_freqs[word] += 1
        else:
            self.word_freqs[word] = 1

class SortedPrinter:
    _word_freq_counter = None
    _rank_list = []

    def __init__(self, wfapp, word_freqs_counter):        
        self._word_freq_counter = word_freqs_counter

        wfapp.register_for_dowork_event(self.__sorted)
        wfapp.register_for_end_event(self.__print_freqs)

    def __sorted(self):
        self._rank_list = sorted(self._word_freq_counter.word_freqs.items(), key=lambda wf: wf[1], reverse=True)

    def __print_freqs(self):
        for (w, f) in self._rank_list[0:25]:
            print(w, ' - ', f)

wfapp = WordFrequencyFramework()
stop_word_filter = StopWordFilter(wfapp)
data_storage = DataStorage(wfapp, stop_word_filter)
word_freqs_counter = WordFrequencyCounter(wfapp, data_storage)
sorted_printer = SortedPrinter(wfapp, word_freqs_counter)

wfapp.run(sys.argv[1])
