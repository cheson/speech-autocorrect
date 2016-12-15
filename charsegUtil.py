
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

def make_char_nGrams(path, numChars): 
    ngramCounts = collections.Counter()
    ntotalCounts = collections.Counter()
    VOCAB_SIZE = 600000
    LONG_WORD_THRESHOLD = 5
    LENGTH_DISCOUNT = 0.15

    def ngramWindow(win, numChars):
        
        # if len(win) == 1:
        #     print "len(win) == 1", win
        #     lst = [SENTENCE_BEGIN] 
        #     for i in range(numChars-2):
        #         lst.append(SENTENCE_BEGIN)
        #     lst.append(win[0])
        #     return tuple(lst)
        # else:
        if len(win) == (numChars-1): 
            lst = [SENTENCE_BEGIN]
            for i in range(numChars-1):
                lst.append(win[i])
            return tuple(lst)

        elif len(win) == numChars: 
            # print tuple(win)
            return tuple(win)

        else:
            return None

    for subdir, dirs, files in os.walk(path):
        for filename in files:
            filePath = subdir + '/' + filename
            with open(filePath, 'r') as f:
                for line in f:
                    line = cleanLine(line)
                    words = line.split()
                    for word in words: 
                        ngrams = [ngramWindow(x, numChars) for x in sliding(word, numChars)]
                        # print ngrams
                        ngramCounts.update(ngrams)
                

    
    print ngramCounts

def make_ngramCosts(ngrams): 
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

    return result

    





    # combine all characters 
    # if combination is valid, add to list
            

path = "corpus/"
# make_char_nGrams(path, 3)
corpus = make_corpus(path)
# print corpus, len(corpus)
make_possibleFills('enferma', corpus)





