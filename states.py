import searchProblem, wordsegUtil

############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost

class VowelInsertionProblem(searchProblem.SearchProblem):

    # queryWords is passed in as a list [w1, w2, w3, ... ]
    # bigramCost is a dict 
    # possibleFills is a sorted list (in alphabetical order)
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills
    '''
    State: (prevWord, index of currWord)
    State recognizes possibleFills based on where the * positions are (where the vowels are)
    '''
    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return ('-BEGIN', 0)
        #raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        length = len(self.queryWords)
        return state[1] == length
        #raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (our solution is 9 lines of code, but don't worry if you deviate from this)
        prevWord, currIndex = state 
        results = []
        currUnfilled = self.queryWords[currIndex]
        possFills = findPossibleFills(currUnfilled, self.possibleFills)
        
        '''
        TODO: Update costs to include unigram costs
        '''

        if currIndex == 0: 
            if len(possFills) == 0: 
                results.append((currUnfilled, (currUnfilled, currIndex+1), self.bigramCost('-BEGIN-', currUnfilled)))
            else:
                for possWord in possFills:
                    results.append((possWord, (possWord, currIndex+1), self.bigramCost('-BEGIN-', possWord)))

        else:
            if len(possFills) == 0: 
                results.append((currUnfilled, (currUnfilled, currIndex+1), self.bigramCost(prevWord, currUnfilled)))
            else:
                for possWord in possFills:
                    results.append((possWord, (possWord, currIndex+1), self.bigramCost(prevWord, possWord)))
        
        #print currUnfilled, results
        return results
        #raise Exception("Not implemented yet")
        # END_YOUR_CODE

def findPossibleFills(query, possibleFills): 
    key = query.find('*')
    possibleFills = []
    if key == -1: 
        return None
    else:
        char = query[key]
        for word in possibleFills[str(key)][char]: 
            if removeVowels(word) == query:
                possibleFills.add(word)

    return possibleFills

def removeVowels(word): 
    return word.translate('aeiouy')

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    ucs = searchProblem.UniformCostSearch(verbose=1)
    ucs.solve(VowelInsertionProblem(queryWords, bigramCost, possibleFills))
    #print ' '.join(ucs.actions)
    return ucs.actions
    #raise Exception("Not implemented yet")
    # END_YOUR_CODE


############################################################

if __name__ == '__main__':
    shell.main()
