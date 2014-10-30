#!/usr/bin/python

"""a library for scrambling text"""

import random

def get_scramble_types(glitchAmt):
    """generates and returns a list of usable scrambling types"""

    scrambles = []

    # actors that can be manipulated
    actors = ( ("letter", 0), ("word", 100) )

    # different sources for the actors to swap things around from

    # sources ending in a "!" are exclusively for letter actors
    # sources ending in a "?" are exclusively for word actors
    # "ascii" sources mean a specific range of ascii characters
    # "self original" refers to original text, "self scrambled" refers to the already scrambled text
    # "list" refers to a custom made letterList or wordList
    # "delete" means outright delete the current character (!)
    # "space!" means replace the current letter with a space
    # "add bucket?" means put a random word into the list of strings
    # "replace bucket?" means replace a word in the list of strings (!)
    sources = ( ("ascii extended!", 100), ("ascii normal!", 75), ("ascii numbers!", 50), 
                ("ascii letters!", 30), ("self original", 20), ("self scrambled", 80),
                ("list", 60), ("delete!", 120), ("space!", 40), ("bucket add?", 150),
                ("bucket replace?", 75) )

    # creates a crossover list of actors and sources 
    for actor in actors:

        for source in sources:

            # combines the actor name with the source name
            name = actor[0] + " " + source[0]
            # the combined cost
            cost = actor[1] + source[1]

            # randomly increases cost- may be it will not be allowed!
            cost += random.randint(0, int(glitchAmt / 5))

            # lets more destructive glitches become more likely
            if cost < 100 and cost < glitchAmt / 2: continue

            # no combinations that start with 'letter' and end in an ? are allowed
            # + no combinations that start with 'word' and end in an ! are allowed
            if (actor[0] == "letter" and source[0][-1] != "?") or (actor[0] == "word" and source[0][-1] != "!"):

                # reduces the cost significantly for otherwise too-expensive ones
                if cost > 120: cost = int(cost * .80)

                if cost <= glitchAmt:
                    # name, baseChance, currChance
                    scrambles.append([name, cost, cost])

    return scrambles


def to_text_list(text, textType=None):
    """converts text into a list and returns it"""

    if textType == None:
        textType = type(text)

    # converts string to a text
    if textType == str:
        textList = [text]
    # points textList to the given list
    elif textType == list or textType == tuple:
        textList = text
    # breaks apart the dict into original text
    elif textType == dict:
        textList = text.values()
    # creates a default for non-valid given items
    else:
        textList = [" "]

    return textList


def fuck_with_scramble_types(scrambleTypes, chanceChangeAmt, letterIndex):
    """fucks with scramble types"""

    glitchHit = None

    for sType in scrambleTypes:
        if not glitchHit:

            # reduces the current chance of the glitch occuring
            sType[2] -= chanceChangeAmt

            if sType[2] > 0:
                # random roll to try to force the glitch on early letters
                if letterIndex < 4 and random.randint(0, int(sType[2])) == 0:
                    sType[2] = 0
                # uses a different formula after the first few letters
                else:
                    roll = random.randint(0, sType[1] * 5)
                    # requires the roll to end up between currChance and baseChance
                    if roll < sType[1] and roll >= sType[2]:
                        sType[2] = 0

            if sType[2] <= 0:
                # sets currChance back to the baseChance
                sType[2] = sType[1]
                # splits up the name of the glitch
                glitchHit = sType[0].split(' ')

    return glitchHit


def scramble_text(glitchAmt, text, DEBUG=False):
    """scrambles a string based on the glitch amount"""

    textType = type(text)
    # there is a rare chance of the entire text being replaced by blank strings
    if glitchAmt >= 180 and random.randint(0, 50) == 0:
        # return blank strings
        if textType == tuple:
            text = ("",) * len(text)
        elif textType == list:
            text = [""] * len(text)
        elif textType == dict:
            for key in text:
                text[key] = ""
        else:
            text = ""
        return text

    # a copy of the original text, as a flattened string
    origTextAsString = ""
    # the original text split into individual words, to run glitches on
    origWords = []
    # how many words have been added to origWords
    wordsAdded = 0
    # how many words can be added in total
    maxWordsAdded = 3

    for chunk in to_text_list(text, textType):
        origTextAsString += chunk
        for word in chunk.split(" "):
            origWords.append(word)

    # a custom made list of ASCII characters
    letterList = "QwR$(8)_ -GXMo0!~|Psz"
    # ASCII codes for non-standard characters
    extendedCharCodes = (146, 153, 164, 168, 178, 186, 216, 236)
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
    # whether or not a glitch has been hit
    glitchHit = False
    # current word from origWords to glitch
    wordIndex = 0
    # the current letter of the current word
    letterIndex = 0

    # dict of glitches that can occur
    scrambleTypes = get_scramble_types(glitchAmt)
    # output of scrambling the inputted text
    scrambledText = [""]

    # an easy reference for valid sources to pull words from
    wordSources = (origWords, wordList, scrambledText)

    # DEBUG ONLY! running total of glitches hit
    numGlitches = 0

    while wordIndex < len(origWords):

        # grabs the current letter
        letter = origWords[wordIndex][letterIndex]
        # the next string to be added to the scrambled text
        # by default it is the original letter, but may be replaced by a glitch
        nextInsert = letter
        stepsUntilGlitch -= 1

        if not glitchHit:
            glitchHit = fuck_with_scramble_types(scrambleTypes, chanceChangeAmt, letterIndex)
        if glitchHit:
            stepsUntilGlitch -= random.randint(0, 2) % 2

        if glitchHit and stepsUntilGlitch <= 0:

            # randomly determines when the next glitch can happen
            stepsUntilGlitch = random.randint(minRange, maxRange)
            # DEBUG! running total of glitches
            numGlitches += 1

            # delete the current character
            if glitchHit[1] == "delete!":
                nextInsert = ""
            # replace the current character with a space
            elif glitchHit[1] == "space!":
                nextInsert = " "
            # add/replace words in origWords
            elif glitchHit[1] == "bucket":

                # word to add to origWords
                word = ""

                # keeps trying to get a word until a valid one is pulled
                while len(word) == 0:

                    # pulls a random source to take a word from
                    wordSource = wordSources[random.randint(0, len(wordSources) - 1)]
                    word = wordSource[random.randint(0, len(wordSource) - 1)]

                # where to insert the word 
                insertPoint = random.randint(wordIndex + 1, len(origWords))

                # adds the word to the end of origWords
                if insertPoint == len(origWords) and wordsAdded < maxWordsAdded:
                    origWords.append(word)
                    wordsAdded += 1

                # puts the word in the middle, somewhere, of origWords
                else: 
                    # adds the new word after an existing one
                    if glitchHit[2] == "add?" and wordsAdded < maxWordsAdded:
                        origWords = origWords[:insertPoint] + [word] + origWords[insertPoint:]
                        wordsAdded += 1
                    # replaces an existing word
                    elif glitchHit[2] == "replace?":
                        origWords = origWords[:insertPoint] + [word] + origWords[insertPoint + 1:]


            # choose a letter from the base text
            elif glitchHit[1] in ("self", "list"):

                source = []

                # choose from a pre-defined list
                if glitchHit[1] == "list":

                    if glitchHit[0] == "letter": source = letterList
                    elif glitchHit[0] == "word": source = wordList

                elif glitchHit[2] == "original":

                    if glitchHit[0] == "letter": source = origTextAsString
                    elif glitchHit[0] == "word": source = origWords

                # choose a possibly-scrambled letter
                elif glitchHit[2] == "scrambled!":

                    if glitchHit[0] == "letter":
                        roll = random.randint(0, len(scrambledText) - 1)
                        source = scrambledText[roll]
                    elif glitchHit[0] == "word": source = scrambledText

                # makes sure there is something usable in the source
                if len(source) > 0:
                    roll = random.randint(0, len(source) - 1)
                    nextInsert = source[roll]

                # defaults to the original letter otherwise
                else: nextInsert = letter


            # choose a random character from a set
            elif glitchHit[1] == "ascii":

                if glitchHit[2] == "letters!":
                    roll = random.randint(1, 101)

                    # uppercase letters
                    if roll > 75: rng = (65, 91)
                    # lowercase letters
                    else: rng = (97, 123)

                # just numbers.... clearly
                elif glitchHit[2] == 'numbers!': rng = (48, 57)
                # standard printing characters
                elif glitchHit[2] == 'normal!': rng = (32, 128)
                # large range of unusual ascii
                elif glitchHit[2] == 'extended!': rng = (128, 255)

                nextInsert = chr(random.randint(rng[0], rng[1]))


            # inserts the new letter after the current one
            if random.randint(0, 99) > 90 and glitchHit[1] != "delete!":
                nextInsert = letter + nextInsert


        # adds the new letter to the most recent word
        scrambledText[-1] += nextInsert

        # updates letterIndex
        letterIndex += 1
        # bumps up letterIndex, so the total length of text isn't too huge
        if glitchHit and glitchHit[0] == "word":
            letterIndex += (len(nextInsert))

        # resets letterIndex and updates wordIndex if needed
        if letterIndex >= len(origWords[wordIndex]):

            letterIndex = 0
            wordIndex += 1
            # keeps increasing the wordIndex if a string is empty
            while wordIndex < len(origWords) and len(origWords[wordIndex]) == 0:
                wordIndex += 1
            # adds the start of a new word to the scrambled origWords
            scrambledText.append("")

    # takes off the empty string at the end of the list
    scrambledText = scrambledText[:-1]

    # the next block compiles the scrambled text back into its original format
    toReturn = None
    if textType == str:
        toReturn = scrambledText[0]
        for word in range(1, len(scrambledText)):
            toReturn += " " + scrambledText[word]
    elif textType == tuple:
        toReturn = tuple(scrambledText)
    elif textType == list:
        toReturn = scrambledText
    elif textType == dict:
        toReturn = {}
        keys = text.keys()
        for word in range(len(scrambledText)):
            toReturn[keys[word]] = scrambledText[word]

    if DEBUG:
        chars = 0
        for x in range(len(scrambledText)):
            chars += len(scrambledText[x]) + 1
        print "glitch amt: %s, range: %s-%s, chance change: %s, glitched: %s/%s - %s%%, scramble types: %s, words: %s" % \
                (glitchAmt, minRange, maxRange, chanceChangeAmt, numGlitches, chars, int( ( (numGlitches * 1.0) / chars ) * 100), 
                    len(scrambleTypes), len(scrambledText))

    return toReturn