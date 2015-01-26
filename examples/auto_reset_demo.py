#!/usr/bin/python

# the scrambling loop is based off of the complex_list_demo

# the purpose is to combine the capped effects of the basic list method
# while keeping the same length of the list from the complex method

import scramble

demoScrambler = scramble.Scrambler()
# blocks scrambler from automatically setting scrambleTypes
demoScrambler.autoResetScrambleTypes = False
# each phrase can only have one new word added
demoScrambler.maxWordsAdded = 1
scrambledTexts = []
glitchAmt = 10
text = ["This is a demonstration", "text string that shall", "be randomly glitched", "and destroyed."]

for x in range(22):
    newLine = []
    for phrase in text:
        newLine.append( demoScrambler.scramble_text(phrase, glitchAmt) )
    scrambledTexts.append(newLine)
    glitchAmt += 10
    # this doesn't need to be done the first time since scrambler handles initializing it
    demoScrambler.populate_scramble_types(glitchAmt)

print ""

for scrambledText in scrambledTexts:
    toPrint = scrambledText[0]
    for word in scrambledText[1:]:
        toPrint += " " + word
    print toPrint
