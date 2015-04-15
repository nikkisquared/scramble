#!/usr/bin/python

"""a library for scrambling text"""

import random
from scrambleText import *

SOURCES = [
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

class Scrambler(object):

    def __init__(self, sources=SOURCES):

        # whether or not to re-populate scramble types automatically
        self.autoResetScrambleTypes = True
        self.scrambleTypes = []

        # the additional costs of each type of actor
        self.actorCosts = {"letter": 0, "word": 100}
        self.sources = sources

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
                        "game.py on line %s" % random.randint(403, 940), "%%s",
                        "but no encoding declared;", "SyntaxError: Non-ASCII"]
        # whether or not to add random ASCII words to wordList later
        self.randomASCIIWords = True


    def scramble_text(self, text, glitchAmt, DEBUG=False):
        """middle function that just calls the real one"""
        return scramble_text(self, text, glitchAmt, DEBUG)


    def populate_scramble_types(self, glitchAmt):
        """populates the list of usable scrambling types"""

        # creates a crossover list of actors and sources
        self.scrambleTypes = []

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
                        self.scrambleTypes.append(
                            {"actor": actor, "source": source["name"],
                            "modifier": modifier["name"],
                            "baseChance": cost, "currChance": cost / 2.5}
                        )


    def set_glitch_ranges(self, glitchAmt):
        """calculates the minimum and maximum ranges for glitches occuring, and returns them"""
        # give up on the ranges at this point
        if glitchAmt >= 900:
            self.minRange = self.maxRange = 0
        else:
            self.minRange = max(14 - int(glitchAmt / 12), 0)
            self.maxRange = max(17 - int(glitchAmt / 22), 0)