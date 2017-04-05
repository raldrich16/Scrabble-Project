

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 15

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}



WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    
    inFile = open(WORDLIST_FILENAME, 'r')
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print("  ", len(wordList), "words loaded.")
    return wordList

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    
    total = 0
    for letter in word[:]:
        total += SCRABBLE_LETTER_VALUES[letter]
    total *= len(word)    
    if len(word) == n:
        total += 50
    return total
        

    



def displayHand(hand):
    """
    Displays the letters currently in the hand.

    
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter,end=" ")       
    print()                             

def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    numVowels = n // 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand


def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    updated_hand = hand.copy()
    for letter in word:
        updated_hand[letter] -= 1
    return updated_hand
    




def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    if word not in wordList: return False
    myhand = hand.copy()
    for letter in word:
        if letter in myhand:
            if myhand[letter]==0:
                return False
            else:
                myhand[letter]-=1
        else:
            return False
    return True



def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    total = 0
    for letter in hand:
        total += hand[letter]
    return total



def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      wordList: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)
      
    """
    total_score = 0
    while calculateHandlen(hand) != 0:
    
        print('Current hand: ', end = "") 
        displayHand(hand)
        inp = input('Enter word, or a "." to indicate that you are finished: ')
        if inp == '.':
            break
        else:
            if isValidWord(inp, hand, wordList) == False:
                print('Invalid word, please try again.')
                print()
                continue
            else:
                total_score += getWordScore(inp, n)
                print('" ' + inp + ' "' + ' earned ' + str(getWordScore(inp, n)) + ' points. Total: ' + str(total_score) + ' points'  )
                print()
                hand = updateHand(hand, inp)
                

    if calculateHandlen(hand) == 0:
        print('Run out of letters. Total score: ' + str(total_score) + ' points.')
    else:
        print('Goodbye! Total score: ' + str(total_score) + ' points.')


def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', the user will play a new hand.
      * If the user inputs 'r',the user will play the last hand again.
      * If the user inputs 'e', the game is exited.
      * If the user inputs anything else, the input is invalid.
 
    2) When done playing the hand, repeat from step 1    
    """
   
    
    while True:
        i = input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if i not in 'nre':
            print('Invalid command.')
            continue
        if i == 'n':
            myhand = dealHand(HAND_SIZE)
            playHand(myhand, wordList, HAND_SIZE)
        if i == 'r':
            try:
                playHand(myhand, wordList, HAND_SIZE)
            except:
                print('You have not played a hand yet. Please play a new hand first!')
                continue
        if i == 'e':
            break
        
            




if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)
