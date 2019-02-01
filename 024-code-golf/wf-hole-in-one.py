import string, re, sys, collections

stops = open('../stop_words.txt').read().split(',') + list(string.ascii_lowercase)

words = re.findall(r'[a-z]{2,}', open(sys.argv[1]).read().lower())

counts = collections.Counter(w for w in words if w not in stops)

for (w, c) in counts.most_common(25):
    print(w, ' - ', c)
