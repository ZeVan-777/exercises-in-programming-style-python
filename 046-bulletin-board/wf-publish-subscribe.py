import sys, re, string

class EventManager:
    _subscriptions = {}

    def subscribe(self, event_type, handler):
        if event_type in self._subscriptions:
            self._subscriptions[event_type].append(handler)
        else:
            self._subscriptions[event_type] = [handler]
    
    def publish(self, *event):
        event_type = event[0]
        if event_type in self._subscriptions:
            for h in self._subscriptions[event_type]:
                h(*event[1:])

class DataStorage:
    _data = ''
    _event_manager = None

    def __init__(self, event_manager):
        self._event_manager = event_manager
        self._event_manager.subscribe('load', self.load)
        self._event_manager.subscribe('start', self.produce_words)
    
    def load(self, path_to_file):
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile(r'[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()

    def produce_words(self):
        for w in ''.join(self._data).split():
            self._event_manager.publish('word', w)
        self._event_manager.publish('eof')

class StopWordFilter:
    _stop_words = []
    _event_manager = None

    def __init__(self, event_manager):
        self._event_manager = event_manager
        self._event_manager.subscribe('load', self.load)
        self._event_manager.subscribe('word', self.is_stop_word)
    
    def load(self, ignore):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))
    
    def is_stop_word(self, w):
        if w not in self._stop_words:
            self._event_manager.publish('valid_word', w)

class WordFrequencyCounter:
    _word_freqs = {}
    _event_manager = None

    def __init__(self, event_manager):
        self._event_manager = event_manager
        self._event_manager.subscribe('valid_word', self.increase_count)
        self._event_manager.subscribe('print', self.sorted_print)

    def increase_count(self, w):
        if w in self._word_freqs:
            self._word_freqs[w] += 1
        else:
            self._word_freqs[w] = 1
    
    def sorted_print(self, n):
        rank_list = sorted(self._word_freqs.items(), key=lambda wf: wf[1], reverse=True)

        for (w, f) in rank_list[0:n]:
            print(w, ' - ', f)

class WordFrequencyApplication:
    _event_manager = None

    def __init__(self, event_manager):
        self._event_manager = event_manager
        self._event_manager.subscribe('run', self.run)
        self._event_manager.subscribe('eof', self.stop)

    def run(self, path_to_file):
        self._event_manager.publish('load', path_to_file)
        self._event_manager.publish('start')
    
    def stop(self):
        self._event_manager.publish('print', 25)
        
        

em = EventManager()
DataStorage(em), StopWordFilter(em), WordFrequencyCounter(em)
WordFrequencyApplication(em)

em.publish('run', sys.argv[1])
