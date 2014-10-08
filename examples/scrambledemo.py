from scramble import *

scrambledTexts = []
glitchAmt = 10
text = "This is a demonstration text string that shall be randomly glitched and destroyed."

for x in range(22):
    scrambledTexts.append( scramble_text(glitchAmt, text) )
    glitchAmt += 10

print ""

for x in range(len(scrambledTexts)):
    print scrambledTexts[x]


print get_scramble_types(30)
