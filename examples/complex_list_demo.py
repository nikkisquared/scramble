#!/usr/bin/python

import scramble

# shows how lists can keep the same length after using scrambler
# this causes the overall result to be lengthened, but the auto_reset_demo shows a method to get around this

demoScrambler = scramble.Scrambler()
basicList = []
complexList = []
glitchAmt = 200
text = ["This is a demonstration", "text string that shall", "be randomly glitched", "and destroyed."]

basicList = demoScrambler.scramble_text(text, glitchAmt)

for x in range(5):
    newLine = []
    for phrase in text:
        newLine.append( demoScrambler.scramble_text(phrase, glitchAmt) )
    complexList.append(newLine)
    glitchAmt += 10

print ""
print "The starting text length is %s strings." % len(text)
print "On this run, the basic method gives a list with %s strings." % len(basicList)
print "However, the complex method gives a list with %s strings." % len(complexList[0])
print "But using the complex method can easily make the results significantly longer than usual, as shown below:"
print ""

for scrambledText in complexList:
    toPrint = scrambledText[0]
    for word in scrambledText[1:]:
        toPrint += " " + word
    print toPrint