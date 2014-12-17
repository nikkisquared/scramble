#!/usr/bin/python

"""a library for scrambling text"""

import random

def get_scramble_types(glitchAmt):
    """generates and returns a list of usable scrambling types"""

    # actors that can be manipulated
    actors = ( ("letter", 0), ("word", 100) )

    # different sources for the actors to swap things around from
    # the first value is the name, and the second is the additive cost
    # sources ending in a "!" are exclusively for letter actors
    # sources ending in a "?" are exclusively for word actors
    # "ascii" sources mean a specific range of ascii characters
    # "self original" refers to original text, "self scrambled" refers to the already scrambled text
    # "list" refers to a custom made letterList or wordList
    # "delete!" means outright delete the current letter
    # "space!" means replace the current letter with a space
    # "add bucket?" means put a random word into the list of strings
    # "replace bucket?" means replace a word in the list of strings (!)
    sources = ( ("ascii extended!", 100), ("ascii normal!", 75), ("ascii numbers!", 50), 
                ("ascii letters!", 30), ("self original", 20), ("self scrambled", 80),
                ("list", 75), ("delete!", 110), ("space!", 40), ("bucket add?", 50),
                ("bucket replace?", 75) )

    # creates a crossover list of actors and sources
    scrambleTypes = []
    for actor in actors:
        for source in sources:

            # combines the actor name with the source name
            name = actor[0] + " " + source[0]
            # the combined cost
            cost = actor[1] + source[1]

            # randomly increases cost, so that there is a slight variance in glitches used
            if glitchAmt > 50:
                cost += random.randint(0, int(glitchAmt / 5))

            # more destructive glitches become more likely over time
            if cost < 100 and cost < glitchAmt / 2:
                continue

            # no combinations that start with 'letter' and end in an ? are allowed
            # + no combinations that start with 'word' and end in an ! are allowed
            if (actor[0] == "letter" and source[0][-1] != "?") or (actor[0] == "word" and source[0][-1] != "!"):

                # reduces the cost significantly for otherwise too-expensive ones
                if cost > 120: cost = int(cost * .80)

                if cost <= glitchAmt:
                    # name, baseChance, currChance
                    scrambleTypes.append([name, cost, cost/2.5])

    # puts the most costly scrambles in the front of the list
    #scrambleTypes.sort(key = lambda s: s[1], reverse = True)

    return scrambleTypes


def iterate_scramble_types(scrambleTypes, chanceChangeAmt, letterIndex):
    """
    goes through every type of glitch available and attempts to randomly return one,
    based on their weighted probabilities
    """

    glitchHit = []

    for sType in scrambleTypes:
        if not glitchHit:

            # increases the chance of the glitch occuring
            sType[2] -= chanceChangeAmt

            # if the scramble has not been guaranteed to occur
            if sType[2] > 0:
                roll = random.randint(0, sType[1] * 5)
                # requires the roll to end up between currChance and baseChance
                if roll < sType[1] and roll >= sType[2]:
                    sType[2] = 0

            # if the currChance is <= 0, save the current scramble
            if sType[2] <= 0:
                # sets currChance back to the baseChance
                sType[2] = sType[1]
                # splits up the name of the glitch
                glitchHit = sType[0].split(' ')

    return glitchHit


def get_random_word(wordSources):
    """gets a valid word from one of the sources given"""

    word = ""
    wordSource = []
    # keeps trying to get a word until a real word is pulled
    while not word:
        while not wordSource:
            wordSource = wordSources[random.randint(0, len(wordSources) - 1)]
        word = wordSource[random.randint(0, len(wordSource) - 1)]

    return word


def add_to_origWords(origWords, glitchSubType, wordIndex, wordSources, newWord=None):
    """adds to or replaces a word in origWords"""

    if not newWord:
        newWord = get_random_word(wordSources)

    endPoint = len(origWords)
    # the replace glitch cannot select the end of the list
    if glitchSubType == "replace?":
        endPoint -= 1
    insertPoint = random.randint(wordIndex + 1, endPoint)

    if insertPoint == len(origWords):
        origWords.append(newWord)
    else:
        origWords = origWords[:insertPoint] + [newWord] + \
            origWords[insertPoint + (glitchSubType == "replace?"):]

    return origWords


def random_ASCII_character(chrRange):
    """returns a random ASCII character based on the given range signifier"""

    if chrRange == "letters!":
        roll = random.randint(1, 101)
        if roll > 75: rng = (65, 91)
        else: rng = (97, 123)
    elif chrRange == 'numbers!':
        rng = (48, 57)
    elif chrRange == 'normal!':
        rng = (32, 128)
    elif chrRange == 'extended!':
        rng = (128, 255)

    return chr(random.randint(rng[0], rng[1]))


def scramble_text(glitchAmt, text, DEBUG=False):
    """scrambles the text based on the glitchiness amount"""

    textType = type(text)
    # there is a rare chance of the entire text being replaced by blank strings
    if glitchAmt >= 180 and random.randint(0, 50) == 0:
        if textType == list:
            text = [""] * len(text)
        else:
            text = ""
        return text

    # points textList to the given list
    elif textType == list:
        textList = text
    # converts string to a text
    else:
        textList = [text]

    # a copy of the original text, as a flattened string
    origTextAsString = ""
    # the original text split into individual words, to run glitches on
    origWords = []
    # how many words have been added to origWords
    wordsAdded = 0
    # how many words can be added in total
    maxWordsAdded = 4

    for chunk in textList:
        origTextAsString += chunk
        for word in chunk.split(" "):
            origWords.append(word)

    # a custom made list of ASCII characters
    letterList = "QwR$(8)_ -GXMo0!~|Psz"
    # ASCII codes for non-standard characters
    extendedCharCodes = (146, 153, 164, 168, 178, 186, 216, 222, 236)
    for charCode in extendedCharCodes:
        letterList += chr(charCode)

    # a custom made list of words to randomly insert
    wordList = ["Baboon", "MNO", "cows", "explo", "lode", "boon", "destructive",
                "side", "STEP", "hi  ", "blat", "thEE", "burg", "diNGgo", "ding",
                "dingette", ",,,", "IT", "you", "YOU", "miss", "RGB", "SCORE",
                "dog", "pet", "__-__", "(8)", "==+==", "this", "scrambleTypes",
                "+%s" % random.randint(1, 100), "-%s" % random.randint(1, 100),
                "minRange", "glitchAmt", "wordList", "character '\xe2'",
                "ENDLINE","IndexError: string", "index out of range",
                "This is a ", "demonstration", "string", "that", "shall be",
                "randomly", "glitched", "and destroy", "ed.", "in file",
                "game.py on line %s" % random.randint(403, 940), 
                "but no encoding declared;", "SyntaxError: Non-ASCII",]
    # randomly generates some extended ASCII words and adds them to wordList
    for i in range(2, 10):
        word = ""
        for j in range(0, int(i/2) + 1):
            word += chr(random.randint(128, 255))
        wordList.append(word)

    # finds the minimum and maximum ranges for glitches occuring on letters
    if glitchAmt <= 900:
        minRange = max(14 - (glitchAmt / 12), 0)
        maxRange = max(17 - int(glitchAmt / 22), 0)
    # give up on the ranges at this point
    else:
        minRange = maxRange = 0

    # the amount a glitch's chance increases by every step
    chanceChangeAmt = glitchAmt * 0.025

    # the number of steps - letters - until a glitch can happen
    # if it is below 0, it is treated the same as it being equal to 0
    # starts off at 0, so there is a chance of characters below minRange being hit
    stepsUntilGlitch = 0
    # critical information for the last glitch to stored, if one has been 
    glitchHit = []
    # current word from origWords to glitch
    wordIndex = 0
    # the current letter of the current word
    letterIndex = 0

    # list of glitches that can occur
    scrambleTypes = get_scramble_types(glitchAmt)
    # output of scrambling the inputted text
    scrambledText = []
    # the next word to be put into scrambledText
    nextWord = ""

    # an easy reference for valid sources to pull words from
    wordSources = (origWords, wordList, scrambledText)

    # running total of glitches applied to the text
    numGlitches = 0

    while wordIndex < len(origWords):

        # grabs the current letter
        letter = origWords[wordIndex][letterIndex]
        # the next string to be added to the scrambled text
        # by default it is the original letter, but may be replaced by a glitch
        nextSubstring = letter
        # try to load a glitch for use, even if one was saved already
        glitchHit = iterate_scramble_types(scrambleTypes, chanceChangeAmt, letterIndex)
        # if a glitch became ready, it will try to cause it now
        if glitchHit:
             stepsUntilGlitch -= 1
        # the next glitch is always one step closer at least
        stepsUntilGlitch -= 1

        if glitchHit and stepsUntilGlitch <= 0:

            # randomly determines when the next glitch can happen
            stepsUntilGlitch = random.randint(minRange, maxRange)
            numGlitches += 1

            # delete the current character
            if glitchHit[1] == "delete!":
                nextSubstring = ""
            # replace the current character with a space
            elif glitchHit[1] == "space!":
                nextSubstring = " "
            # choose a random character from the defined set
            elif glitchHit[1] == "ascii":
                nextSubstring = random_ASCII_character(glitchHit[2])

            # add new words into, or replace existing words in, origWords
            # it won't bother trying to add a new word if the cap has been reached
            # and it won't try to replace a word if it won't come up for glitching
            elif (glitchHit[1] == "bucket"
                    and not (glitchHit[2] == "add?" and wordsAdded >= maxWordsAdded)
                    and not (glitchHit[2] == "replace?" and wordIndex + 1 == len(origWords)) ):
                origWords = add_to_origWords(origWords, glitchHit[2], wordIndex, wordSources)
                if glitchHit[2] == "add?":
                    wordsAdded += 1

            # choose a letter or word from the base text, or a defined list
            elif glitchHit[1] in ("self", "list"):
                source = []

                # choose from a pre-defined list
                if glitchHit[1] == "list":
                    if glitchHit[0] == "letter": source = letterList
                    elif glitchHit[0] == "word": source = wordList
                # choose from the original text
                elif glitchHit[2] == "original":
                    if glitchHit[0] == "letter": source = origTextAsString
                    elif glitchHit[0] == "word": source = origWords
                # choose a possibly-scrambled letter/word
                elif glitchHit[2] == "scrambled!":
                    if glitchHit[0] == "letter":
                        roll = random.randint(0, len(scrambledText) - 1)
                        source = scrambledText[roll]
                    elif glitchHit[0] == "word":
                        source = scrambledText

                # makes sure there is something usable in the source
                if len(source) > 0:
                    roll = random.randint(0, len(source) - 1)
                    nextSubstring = source[roll]
                    if glitchHit[0] == "word":
                        # bumps up letterIndex, so the total length of text isn't too huge
                        letterIndex += (len(nextSubstring))
                        wordsAdded += 1
                # defaults to the original letter if there's nothing in the source
                else:
                    nextSubstring = letter

            # 10% chance of putting in the original letter before the nextSubstring
            if random.randint(0, 99) > 90 and glitchHit[1] != "delete!":
                nextSubstring = letter + nextSubstring

        # adds the new letter to the most recent word
        nextWord += nextSubstring
        # updates letterIndex
        letterIndex += 1

        # resets letterIndex and updates wordIndex if needed
        if letterIndex >= len(origWords[wordIndex]):
            scrambledText.append(nextWord)
            nextWord = ""
            letterIndex = 0
            wordIndex += 1
            # keeps increasing the wordIndex if a string is empty
            while wordIndex < len(origWords) and len(origWords[wordIndex]) == 0:
                wordIndex += 1

    # the next block compiles the scrambled text back into its original format
    toReturn = None
    if textType == list:
        toReturn = scrambledText
    else:
        toReturn = scrambledText[0]
        for word in range(1, len(scrambledText)):
            toReturn += " " + scrambledText[word]

    # DEBUG ONLY output
    if DEBUG:
        chars = 0
        for x in range(len(scrambledText)):
            chars += len(scrambledText[x]) + 1
        print "glitch amt: %s, range: %s-%s, chance change: %s, glitched: %s/%s - %s%%, scramble types: %s, words: %s" % \
                (glitchAmt, minRange, maxRange, chanceChangeAmt, numGlitches, chars, int( ( (numGlitches * 1.0) / chars ) * 100), 
                    len(scrambleTypes), len(scrambledText))

    return toReturn