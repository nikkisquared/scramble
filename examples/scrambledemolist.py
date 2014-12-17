from scramble import *

scrambledTexts = []
glitchAmt = 10
text = "This is a demonstration text string that shall be randomly glitched and destroyed."
text = text.split()

for x in range(22):
    scrambledTexts.append( scramble_text(glitchAmt, text) )
    glitchAmt += 10

print ""

for scrambledText in scrambledTexts:
    toPrint = scrambledText[0]
    for word in scrambledText[1:]:
        toPrint += " " + word
    print toPrint
