#!/usr/bin/python

import scramble

demoScrambler = scramble.Scrambler()
scrambledTexts = []
glitchAmt = 10
text = "This is a demonstration text string that shall be randomly glitched and destroyed."
text = text.split()

for x in range(22):
    scrambledTexts.append( demoScrambler.scramble_text(text, glitchAmt) )
    glitchAmt += 10

print ""

for scrambledText in scrambledTexts:
    toPrint = scrambledText[0]
    for word in scrambledText[1:]:
        toPrint += " " + word
    print toPrint