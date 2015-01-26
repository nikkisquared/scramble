#!/usr/bin/python

"""a library for scrambling text"""

import random

class Scrambler(object):

    def __init__(self):

        # the additional costs of each type of actor
        self.actorCosts = {"letter": 0, "word": 100}

        # different sources for the actors to interact with
        self.sources = [
            # "ascii" means specific ranges of ascii characters to insert
            {"name": "ascii", "actors": ["letter"],
            "modifiers": [
                {"name": "letters", "cost": 30},
                {"name": "numbers", "cost": 50},
                {"name": "normal", "cost": 75},
                {"name": "extended", "cost": 100}
            ]},
            {"name": "self", "actors": ["letter", "word"],
            "modifiers": [
                # "original" inserts a word from the original text
                {"name": "original", "cost": 20},
                # "scrambled" inserts a word from the already scrambled text
                {"name": "scrambled", "cost": 80}
            ]},
            {"name": "bucket", "actors": ["word"],
            "modifiers": [
                # "add" means put a random word into origWords
                {"name": "add", "cost": 50},
                # "replace" means replace a random word in origWords
                {"name": "replace", "cost": 75}
            ]},
            # "list" refers to a custom made letterList or wordList
            {"name": "list", "actors": ["letter", "word"],
            "modifiers": [
                {"name": "default", "cost": 75}
            ]},
            # "space" means replace the current letter with a space
            {"name": "space", "actors": ["letter"],
            "modifiers": [
                {"name": "default", "cost": 40}
            ]},
            # "delete" means outright delete the current letter
            {"name": "delete", "actors": ["letter"],
            "modifiers": [
                {"name": "default", "cost": 110}
            ]}
        ]

        # how many words can be added in total
        self.maxWordsAdded = 4

        # a custom made list of ASCII characters
        self.letterList = "QwR$(8)_ -GXMo0!~|Psz"
        # ASCII codes for non-standard characters
        self.extendedCharCodes = (146, 153, 164, 168, 178, 186, 216, 222, 236)

        # a custom made list of words to randomly insert
        self.wordList = ["MNO", "cows", "explo", "lode", "boon", "side", "STEP",
                    "hi  ", "blat", "thee", "burg", "dingo", "ding", "dingette",
                    "", '"', ",", ",,,", "IT", "you", "YOU", "miss", "RGB", "SCORE",
                    "dog", "pet", "__-__", "(8)", "==+==", "this", "scrambleTypes",
                    "+%s" % random.randint(1, 100), "-%s" % random.randint(1, 100),
                    "minRange", "glitchAmt", "wordList", "character '\xe2'",
                    "ENDLINE","IndexError: string", "index out of range", 
                    "This is a ", "demonstration", "string", "that", "shall be",
                    "randomly", "glitched", "and destroy", "ed.", "in file",
                    "game.py on line %s" % random.randint(403, 940),
                    "but no encoding declared;", "SyntaxError: Non-ASCII"]
        # whether or not to add random ASCII words to wordList later
        self.randomASCIIWords = True


    def format_input_text(self, text, textType=None):
        """formats the input text into a single string and a list of individual words, and returns both"""

        if not textType:
            textType = type(text)
        
        # points textList to the given list
        if textType == list:
            textList = text
        # converts string to a text
        else:
            textList = [text]

        # a copy of the original text, as a flattened string
        origTextAsString = ""
        # the original text split into individual words, to run glitches on
        origWords = []

        for chunk in textList:
            origTextAsString += chunk
            if chunk.isspace():
                origWords.append(" ")
            else:
                for word in chunk.split(" "):
                    origWords.append(word)

        return origTextAsString, origWords


    def get_scramble_types(self, glitchAmt):
        """generates and returns a list of usable scrambling types"""

        # creates a crossover list of actors and sources
        scrambleTypes = []

        for source in self.sources:
            for actor in source["actors"]:
                for modifier in source["modifiers"]:

                    cost = self.actorCosts[actor] + modifier["cost"]
                    # randomly increases cost slightly
                    if glitchAmt > 50:
                        cost += random.randint(0, int(glitchAmt / 5))

                    # blocks less destructive glitches
                    if cost < 100 and cost < glitchAmt / 2:
                        continue

                    # reduces the cost significantly for otherwise too-expensive ones
                    if cost > 120: cost = int(cost * .80)

                    if cost <= glitchAmt:
                        scrambleTypes.append(
                            {"actor": actor, "source": source["name"],
                            "modifier": modifier["name"],
                            "baseChance": cost, "currChance": int(cost/2.5)}
                        )

        return scrambleTypes


    def iterate_scramble_types(self, scrambleTypes, chanceChangeAmt, letterIndex):
        """
        goes through every type of glitch available and attempts to randomly return one,
        based on their weighted probabilities
        """

        glitchHit = None

        # iterate through every scramble in scrambleTypes
        for scramble in scrambleTypes:

            # increases the chance of the glitch occuring
            scramble["currChance"] -= chanceChangeAmt

            # if the scramble has not been guaranteed to occur
            if scramble["currChance"] > 0:
                roll = random.randint(0, scramble["baseChance"] * 5)
                if roll >= scramble["currChance"] and roll < scramble["baseChance"]:
                    scramble["currChance"] = 0

            if scramble["currChance"] <= 0:
                # sets currChance back to the baseChance
                scramble["currChance"] = scramble["baseChance"]
                # saves a pointer to the glitch
                glitchHit = scramble
                break

        return glitchHit


    def get_random_word(self, wordSources):
        """gets a valid word from one of the sources given"""

        possible = False
        for wordSource in wordSources:
            if wordSource:
                possible = True
        if not possible:
            return ""

        word = ""
        wordSource = []
        # keeps trying to get a word until a real word is pulled
        while not word:
            while not wordSource:
                wordSource = wordSources[random.randint(0, len(wordSources) - 1)]
            word = wordSource[random.randint(0, len(wordSource) - 1)]

        return word


    def add_to_origWords(self, origWords, modifier, wordIndex, wordSources, newWord=None):
        """adds to or replaces a word in origWords"""

        if not newWord:
            newWord = self.get_random_word(wordSources)

        endPoint = len(origWords)
        # the replace glitch cannot select the end of the list
        if modifier == "replace":
            endPoint -= 1
        insertPoint = random.randint(wordIndex + 1, endPoint)

        if insertPoint == len(origWords):
            origWords.append(newWord)
        else:
            origWords = origWords[:insertPoint] + [newWord] + \
                origWords[insertPoint + (modifier == "replace"):]

        return origWords


    def random_ASCII_character(self, chrRange):
        """returns a random ASCII character based on the given range signifier"""

        if chrRange == "letters":
            roll = random.randint(1, 101)
            if roll > 75: rng = (65, 91)
            else: rng = (97, 123)
        elif chrRange == 'numbers':
            rng = (48, 57)
        elif chrRange == 'normal':
            rng = (32, 128)
        elif chrRange == 'extended':
            rng = (128, 255)

        return chr(random.randint(rng[0], rng[1]))


    def scramble_text(self, text, glitchAmt, DEBUG=False):
        """scrambles the text based on the glitchiness amount"""

        textType = type(text)
        # removes empty strings so they don't cause error
        if textType == list:
            text = filter(None, text)

        # sends back blank strings if the input text is blank, but also there is  
        # a rare chance of the entire text being replaced by blank strings
        if not text or glitchAmt >= 180 and random.randint(0, 50) == 0:
            if textType == list:
                text = [""] * len(text)
            else:
                text = ""
            return text

        origTextAsString, origWords = self.format_input_text(text, textType)
        # how many words have been added to origWords
        wordsAdded = 0

        localLetterList = self.letterList[:]
        for charCode in self.extendedCharCodes:
            localLetterList += chr(charCode)

        localWordList = self.wordList[:]
        # randomly generates some extended ASCII words and adds them to wordList
        if self.randomASCIIWords:
            for i in range(2, 10):
                word = ""
                for j in range(0, int(i/2) + 1):
                    word += chr(random.randint(128, 255))
                localWordList.append(word)

        # finds the minimum and maximum ranges for glitches occuring on letters
        if glitchAmt <= 900:
            minRange = max(14 - (glitchAmt / 12), 0)
            maxRange = max(17 - int(glitchAmt / 22), 0)
            #minRange, maxRange = self.glitchRanges(glitchAmt)
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
        glitchHit = None
        # current word from origWords to glitch
        wordIndex = 0
        # the current letter of the current word
        letterIndex = 0

        # list of glitches that can occur
        scrambleTypes = self.get_scramble_types(glitchAmt)
        # output of scrambling the inputted text
        scrambledText = []
        # the next word to be put into scrambledText
        nextWord = ""

        # an easy reference for valid sources to pull words from
        wordSources = (origWords, localWordList, scrambledText)

        # running total of glitches applied to the text
        numGlitches = 0

        while wordIndex < len(origWords):

            # grabs the current letter
            letter = origWords[wordIndex][letterIndex]
            # the next string to be added to the scrambled text
            # by default it is the original letter, but may be replaced by a glitch
            nextSubstring = letter
            # try to load a glitch for use, even if one was saved already
            glitchHit = self.iterate_scramble_types(scrambleTypes, chanceChangeAmt, letterIndex)
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
                if glitchHit["source"] == "delete":
                    nextSubstring = ""
                # replace the current character with a space
                elif glitchHit["source"] == "space":
                    nextSubstring = " "
                # choose a random character from the defined set
                elif glitchHit["source"] == "ascii":
                    nextSubstring = self.random_ASCII_character(glitchHit["modifier"])

                # add new words into, or replace existing words in, origWords
                # it won't bother trying to add a new word if the cap has been reached
                # and it won't try to replace a word if it won't come up for glitching
                elif (glitchHit["source"] == "bucket"
                        and not (glitchHit["modifier"] == "add" and wordsAdded >= self.maxWordsAdded)
                        and not (glitchHit["modifier"] == "replace" and wordIndex + 1 == len(origWords)) ):
                    origWords = self.add_to_origWords(origWords, glitchHit["modifier"], wordIndex, wordSources)
                    if glitchHit["modifier"] == "add":
                        wordsAdded += 1

                # choose a letter or word from the base text, or a defined list
                elif glitchHit["source"] in ("self", "list"):
                    source = []

                    # choose from a pre-defined list
                    if glitchHit["source"] == "list":
                        if glitchHit["actor"] == "letter": source = localLetterList
                        elif glitchHit["actor"] == "word": source = localWordList
                    # choose from the original text
                    elif glitchHit["modifier"] == "original":
                        if glitchHit["actor"] == "letter": source = origTextAsString
                        elif glitchHit["actor"] == "word": source = origWords
                    # choose a possibly-scrambled letter/word
                    elif glitchHit["modifier"] == "scrambled":
                        if glitchHit["actor"] == "letter" and len(scrambledText) > 0:
                            roll = random.randint(0, len(scrambledText) - 1)
                            source = scrambledText[roll]
                        elif glitchHit["actor"] == "word":
                            source = scrambledText

                    # makes sure there is something usable in the source
                    if len(source) > 0:
                        roll = random.randint(0, len(source) - 1)
                        nextSubstring = source[roll]
                        if glitchHit["actor"] == "word":
                            # bumps up letterIndex, so the total length of text isn't too huge
                            letterIndex += (len(nextSubstring))
                            wordsAdded += 1
                    # defaults to the original letter if there's nothing in the source
                    else:
                        nextSubstring = letter

                # 10% chance of putting in the original letter before the nextSubstring
                if random.randint(0, 99) > 90 and glitchHit["source"] != "delete":
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