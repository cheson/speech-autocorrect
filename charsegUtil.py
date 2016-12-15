
import collections, os, math, string

SENTENCE_BEGIN = '-BEGIN-'
VOWELS = 'aeiou'

def sliding(xs, windowSize):
    for i in xrange(1, len(xs) + 1):
        yield xs[max(0, i - windowSize):i]


def notNumberOrPunctuation(s):
    s = s.replace('-', ' ')
    s = s.translate(None, string.punctuation)
    s = s.translate(None, string.digits)
    return s

def cleanLine(l):
    return notNumberOrPunctuation(l.strip().lower())


# Creates character n-grams. of form ['a', 'b', 'c', 'd']. and ['BEGIN', 'a', 'b', 'c']
# Note that the other cases (e.g. ['BEGIN', 'BEGIN', 'a', 'b']) are handled by earlier n-grams

def make_nGramCost(path, numChars): 
    ngramCounts = collections.Counter()
    ntotalCounts = collections.Counter()
    VOCAB_SIZE = 600000
    LONG_WORD_THRESHOLD = 5
    LENGTH_DISCOUNT = 0.15

    def ngramWindow(win, numChars):
        
        if len(win) == (numChars-1): 
            lst = [SENTENCE_BEGIN]
            for i in range(numChars-1):
                lst.append(win[i])
            return tuple(lst)

        elif len(win) == numChars: 
            # print tuple(win)
            return tuple(win)

        else:
            return ('\x00', '\x00', '\x00')

    for subdir, dirs, files in os.walk(path):
        for filename in files:
            filePath = subdir + '/' + filename
            with open(filePath, 'r') as f:
                for line in f:
                    line = cleanLine(line)
                    words = line.split()
                    for word in words: 
                        ngrams = [ngramWindow(x, numChars) for x in sliding(word, numChars)]
                        ngramCounts.update(ngrams)
                        ntotalCounts.update([x[0] for x in ngrams])
                

    def ngramModel(word, index):
        assert index < len(word)

        ngrams = [ngramWindow(x, numChars) for x in sliding(word[index-2:index+2], numChars)]
        char = word[index]


        ngramScore = 0
        for item in ngrams: 
            ngramScore += ngramCounts[item]

        return math.log(ntotalCounts[char] + VOCAB_SIZE) / 2 + math.log(ngramScore + 1)


    # do something with ntotal counts 
    return ngramModel


# make bigram
def make_bigramCost(path):
    unigrams = set([])
    totalCounts = 0
    bigramCounts = collections.Counter()
    bitotalCounts = collections.Counter()
    VOCAB_SIZE = 600000
    LONG_WORD_THRESHOLD = 5
    LENGTH_DISCOUNT = 0.15

    def bigramWindow(win):
        assert len(win) in [1, 2]
        if len(win) == 1:
            return (SENTENCE_BEGIN, win[0])
        else:
            return tuple(win)

    # bigramCost = collections.defaultdict(list)

    for subdir, dirs, files in os.walk(path):
        for filename in files:
            filePath = subdir + '/' + filename
            with open(filePath, 'r') as f:
                for l in f:
                    ws = cleanLine(l).split()
                    unigrams.update(x[0] for x in sliding(ws, 1))
                    bigrams = [bigramWindow(x) for x in sliding(ws, 2)]
                    # totalCounts += len(unigrams)
                    # unigramCounts.update(unigrams)
                    bigramCounts.update(bigrams)
                    bitotalCounts.update([x[0] for x in bigrams])


    def bigramModel(a, b):
        return math.log(bitotalCounts[a] + VOCAB_SIZE) - math.log(bigramCounts[(a, b)] + 1)

    return bigramModel

# def make_ngramCosts(ngrams): 
    # to figure out how to cost the ngram

def make_corpus(path):
    corpus = set([])
    for subdir, dirs, files in os.walk(path):
        for filename in files:
            filePath = subdir + '/' + filename
            with open(filePath, 'r') as f:
                for line in f:
                    line = cleanLine(line)
                    words = line.split()
                    for word in words:
                        corpus.add(word)

    return corpus

# takes in a word with ** blanks and returns a list of all valid possible fills based on all possible vowel combinations
# e.g. make_possibleFills(vamos) transforms into '"v*m*s"' and returns ['vamos', 'vemos']
def make_possibleFills(word, corpus): 
    
    def unvowel(word): 
        numVowels = 0
        for ch in word:
            if ch in VOWELS:
                word = word.replace(ch,'*')
                numVowels += 1
        return word, numVowels

    def fillHelper(word, wordIndex, corpus, result):
        if wordIndex == len(word): 
            if word in corpus:
                result.append(word)
            return 
        replIndex = word.find('*')
        if replIndex == -1: 
            if word in corpus:
                result.append(word)
            return 
        else: 
            for ch in VOWELS: 
                newWord = word.replace('*', ch, 1)
                fillHelper(newWord, replIndex, corpus, result)


    result = []
    word, numVowels = unvowel(word)
    fillHelper(word, 0, corpus, result)

    print "possFills: ", result
    return result

### Vowel removal to make inverse dictionary  

def removeAll(s, chars):
    return ''.join(filter(lambda c: c not in chars, s))


def makeInverseRemovalDictionary(corpus, removeChars):
    wordsRemovedToFull = collections.defaultdict(set)

    for word in corpus: 
        wordsRemovedToFull[removeAll(word, removeChars)].add(word)

    wordsRemovedToFull = dict(wordsRemovedToFull)
    empty = set()

    def possibleFills(short):
        return wordsRemovedToFull.get(short, empty)

    return possibleFills


# path = "corpus/"
# ngramCost = make_nGramCost(path, 3)
# print ngramCost("nosotros", 0)
# print ngramCost("nosotros", 1)
# print ngramCost("nosotros", 2)
# print ngramCost("nosotros", 3)
# print ngramCost("nosotros", 4)
# print ngramCost("nosotros", 5)
# print ngramCost("nosotros", 6)
# print ngramCost("nosotros", 7)
# corpus = make_corpus(path)
# print corpus, len(corpus)
# make_possibleFills('enferma', corpus)





