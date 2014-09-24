#!/usr/bin/python

# MASSIVE program for scrambling text
# requires an amount of glitchiness, and a string or an array or dict with only strings

import random

def get_scramble_types(glitchAmt):
    # generates and returns a list of usable scrambling types

    scrambles = []

    # actors that can be manipulated
    actor = ( ("letter", 0), ("word", 100) )

    # different sources for the actor to swap things around from

    # random * sources mean a specific set of ascii characters
    # "self original" refers to original text, "self scrambled" refers to the already scrambled text
    # "list" refers to a custom made letterList
    # "delete" means outright delete the current character (!)
    # "space!" means replace the current letter with a space
    # "add to strings?" means put a random word into the list of strings
    # "replace in strings?" means replace a word in the list of strings (!)
    source = ( ("random extended!", 100), ("random normal!", 75), ("random numbers!", 50), 
                ("random letters!", 30), ("self original", 20), ("self scrambled", 80),
                ("list", 60), ("delete!", 120), ("space!", 40), ("add strings?", 150),
                ("replace strings?", 75) )


    # creates a crossover list of actors and sources 
    for x in actor:

        for y in source:

            # combines the actor name with the source name
            name = x[0] + " " + y[0]
            # the combined cost
            cost = x[1] + y[1]

            # lets more destructive glitches become more likely
            if cost < 100 and cost < glitchAmt / 2: continue

            # randomly increases cost- may be it will not be allowed!
            cost += random.randint(0, int(glitchAmt / 5))

            # no combinations that start with 'letter' and end in an ? are allowed
            # + no combinations that start with 'word' and end in an ! are allowed
            if (x[0] == "letter" and y[0][-1] != "?") or (x[0] == "word" and y[0][-1] != "!"):

                # reduces the cost significantly for otherwise too-expensive ones
                if cost > 120: cost = int(cost * .80)

                if cost <= glitchAmt:
                    # name, base chance, current chance
                    scrambles.append([name, cost, cost])

    return scrambles


def scramble_text(glitchAmt, text, debug=False):
    # scrambles a string based on the glitch amount


    # there is a rare chance of the entire string being deleted
    delete = glitchAmt >= 180 and random.randint(0, 50) == 0


    # breaks apart the dict into original text
    if type(text) == dict:

        # saves references for keys
        keys = text.keys()
        textList = text.values()

    # converts string to a text
    elif type(text) == str:
        textList = [text]

    # points textList to the given list
    elif type(text) == list:
        textList = text

    # creates a default for non-valid given items
    else: textList = [" "]


    # a copy of the original text
    origText = ""
    # list of strings to run glitches on
    strings = []

    for t in textList:

        origText += t

        for s in t.split(" "):

            # puts in nothing if blank text should be returned
            if delete: strings.append("")
            else: strings.append(s)


    # a custom made list of ascii characters
    letterList = "\\MRBAbOo*queEr<3)butTs_in{=]UR^gRilL$"

    # easier reference for non-standard characters
    chrs = (146, 153, 164, 168, 178, 186, 216, 236)
    # converts above into characters
    for x in chrs: letterList += chr(x)


    # a custom made list of words to randomly insert
    wordList = ["Mr", "Babbo", "babbon", "BABOON", "MN", "NO", "cow", "level",
                "explo", "lODe", "bbAb", "mrba", "boon", "destructive", "inside",
                "ouTsi", "side", "StEP", "hi  ", "blat", "thEE", "ieef", "burg",
                "diNGgo", "ding", "dingette", ",,,", "IT", "you", "mIss", "RGb",
                "scoRRe", "wordList" "dog", "pet", "__-__", "(8)", "==+==", "YOU",
                "+%s" % random.randint(1, 100), "-%s" % random.randint(1, 100),
                "this", "hu", "rts", "minRange", "glitchAmt", "scrambleTypes",
                "IndexError: string", "index out of range", "SyntaxError: Non-ASCII",
                "character '\xe2'", "This is a ", "demonstration", "string", "that",
                "shall be", "randomly", "glitched", "and destroy", "ed.", "ENDLINE",
                "in file", "game.py on line %s" % random.randint(403, 940), 
                "but no encoding declared;"]


    # adds some random ascii words to wordList
    for x in range(2, 10):

        word = ""

        for y in range(0, int(x/2) + 1):
            word += chr(random.randint(128, 255))

        wordList.append(word)


    scrambleTypes = get_scramble_types(glitchAmt)

    # rate slowly increases
    rate = glitchAmt * 0.025

    # calculates the total difference in 
    minRange = 14 - (glitchAmt / 12)
    maxRange = 17 - int(glitchAmt / 22)

    # negative values might cause an error
    if minRange < 0: minRange = 0
    # max range should be kept to a minimum!
    if maxRange < 0: maxRange = 3

    # give up on the range deal... glitch EVERYTHING
    if glitchAmt > 900:
        minRange = maxRange = 0


    # DEBUG! running total of glitches hit
    glitches = 0
    # array of scrambled strings
    scrambledText = [""]

    # starts off at 0, so there is a chance of characters below minRange being hit
    nextGlitch = 0
    # whether or not a glitch has been hit
    glitchHit = False

    # current word from strings to glitch
    currWord = 0
    # the current letter of the current word
    currLetter = 0


    # an easy reference for valid sources to pull words from
    wordSources = (strings, wordList, scrambledText)

    # how many words have been added to strings
    wordsAdded = 0
    # how many words can be added in total
    newWordsCap = 3

    while currWord < len(strings) and not delete:

        # grabs the current letter
        letter = strings[currWord][currLetter]

        # the next string to be added to the scrambled text
        nextInsert = letter

        # makes it more likely for a glitch to occur
        nextGlitch -= 1

        # forces glitchHit to false, even if one was hit
        glitchHit = False

        for s in scrambleTypes:

            if not glitchHit:

                # reduces the current chance of the glitch occuring
                s[2] -= rate

                if s[2] > 0:

                    # random roll to try to force the glitch on early letters
                    if currLetter < 4 and random.randint(0, int(s[2])) == 0:
                        s[2] = 0
                    # uses a different formula after the first few letters
                    else:

                        roll = random.randint(0, s[1] * 5)
                        # requires the roll to end up between the current chance
                        # and the base chance, after a high roll
                        if roll >= s[2] and roll < s[1]:
                            s[2] = 0

                if s[2] <= 0:

                    # sets the current chance back to the base chance
                    s[2] = s[1]
                    # saves the names
                    glitchHit = s[0].split(' ')

                    nextGlitch -= 1


        if glitchHit and nextGlitch <= 0:

            # randomly determines when the next glitch can happen
            nextGlitch = random.randint(minRange, maxRange)
            # DEBUG! running total of glitches
            glitches += 1


            # delete the current character
            if glitchHit[1] == "delete!":
                nextInsert = ""

            # replace the current character with a space
            elif glitchHit[1] == "space!":
                nextInsert = " "

            # add/replace words in strings
            elif glitchHit[-1] == "strings?":

                # word to add to strings
                word = ""

                # keeps trying to get a word until a valid one is pulled
                while len(word) == 0:

                    # pulls a random source to take a word from
                    wordSource = wordSources[random.randint(0, len(wordSources) - 1)]
                    word = wordSource[random.randint(0, len(wordSource) - 1)]

                # where to insert the word 
                insertPoint = random.randint(currWord + 1, len(strings))

                # adds the word to the end of strings
                if insertPoint == len(strings) and wordsAdded < newWordsCap:
                    strings.append(word)
                    wordsAdded += 1

                # puts the word in the middle, somewhere, of strings
                else: 
                    # adds the new word after an existing one
                    if glitchHit[1] == "add" and wordsAdded < newWordsCap:
                        strings = strings[:insertPoint] + [word] + strings[insertPoint:]
                        wordsAdded += 1
                    # replaces an existing word
                    elif glitchHit[1] == "replace":
                        strings = strings[:insertPoint] + [word] + strings[insertPoint + 1:]


            # choose a letter from the base text
            elif glitchHit[1] in ("self", "list"):

                source = []

                # choose from a pre-defined list
                if glitchHit[1] == "list":

                    if glitchHit[0] == "letter": source = letterList
                    elif glitchHit[0] == "word": source = wordList

                elif glitchHit[2] == "original":

                    if glitchHit[0] == "letter": source = origText
                    elif glitchHit[0] == "word": source = strings

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
            elif glitchHit[1] == "random":

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

        # updates currLetter
        currLetter += 1

        # bumps up currLetter, so the total length of text isn't too huge
        if glitchHit and glitchHit[0] == "word":
            currLetter += (len(nextInsert))

        # resets currLetter and updates currWord if needed
        if currLetter >= len(strings[currWord]):

            currLetter = 0
            currWord += 1

            # keeps increasing the currWord if a string is empty
            while currWord < len(strings) and len(strings[currWord]) == 0:
                currWord += 1

            # adds the start of a new word to the scrambled strings
            scrambledText.append("")


    toReturn = None

    # compiles the scrambled text back into a string
    if type(text) == str:

        toReturn = ""

        for x in range(len(scrambledText)):
            toReturn += scrambledText[x] + " "

    elif type(text) == dict:

        toReturn = {}
        
        for x in range(len(scrambledText)):
            toReturn[keys[x]] = scrambledText[x]

    elif type(text) == list:
        toReturn = scrambledText


    if debug:

        chars = 0
        for x in range(len(scrambledText)):
            chars += len(scrambledText[x]) + 1

        print "glitch amt: %s, range: %s-%s, rate: %s, glitched: %s/%s - %s%%, scramble types: %s, words: %s" % \
                (glitchAmt, minRange, maxRange, rate, glitches, chars, 
                int( ( (glitches * 1.0) / chars ) * 100), len(scrambleTypes), len(scrambledText) )


    return toReturn
