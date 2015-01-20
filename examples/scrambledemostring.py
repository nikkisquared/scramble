import scramble

demoScrambler = scramble.Scrambler()
scrambledTexts = []
glitchAmt = 10
text = "This is a demonstration text string that shall be randomly glitched and destroyed."

for x in range(22):
    scrambledTexts.append( demoScrambler.scramble_text(text, glitchAmt) )
    glitchAmt += 10

print ""

for x in range(len(scrambledTexts)):
    print scrambledTexts[x]
