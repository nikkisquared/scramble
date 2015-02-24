#!/usr/bin/python
#encoding:utf-8

import scramble
import random, difflib
random.seed(1)

demoScrambler = scramble.Scrambler()
scrambledTexts = []
glitchAmt = 10
text = "This is a demonstration text string that shall be randomly glitched and destroyed."

for x in range(22):
    scrambledTexts.append( demoScrambler.scramble_text(text, glitchAmt) )
    glitchAmt += 10

print ""

output = u"T¥is dog a dshallrat⌐ia trandomly stßing that sallshall b┼ a glitand nd dedingette"

print output
print scrambledTexts[-1]