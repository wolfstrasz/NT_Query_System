# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen
# Revised November 2016 by Adam Lopez

# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self):
        self.lexicon = {}
        self.lexicon['P'] = []
        self.lexicon['N'] = []
        self.lexicon['A'] = []
        self.lexicon['I'] = []
        self.lexicon['T'] = []

    def add(self, stem, cat):
        # Adding a word from a category
        if cat in self.lexicon.keys():
            if not stem in self.lexicon[cat]:
                self.lexicon[cat].append(stem)
	
    def getAll(self, cat):
        if cat in self.lexicon.keys():
            return self.lexicon[cat]


class FactBase:
    def __init__(self):
        self.unaries = {}
        self.binaries = {}

    def addUnary(self, pred, e1):
        if pred not in self.unaries.keys():
            self.unaries[pred] = []
        self.unaries[pred].append(e1)

    def addBinary(self, pred, e1, e2):
        if pred not in self.binaries.keys():
            self.binaries[pred] = []
        self.binaries[pred].append((e1,e2))

    def queryUnary(self, pred, e1):
        if pred in self.unaries.keys():
            return e1 in self.unaries[pred]
        else:
            return False

    def queryBinary(self, pred, e1, e2):
        if pred in self.binaries.keys():
            return (e1, e2) in self.binaries[pred]
        else:
            return False

import re
from nltk.corpus import brown
# btw =  set of all brown tagged words
# used to load the tagged words once
# instead of loading them everytime when checking
btw = set(brown.tagged_words())
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""

    if(re.match(r'\w*([^aeiousxyzh]|(^ch)|(^sh))s$', s)):
        stem = s[:-1]
    elif(re.match(r'\w*[aeiou]ys$', s)):
        stem = s[:-1]
    elif(re.match(r'\w+[^aeiou]ies$', s)):
        stem = s[:-3] + 'y'
    elif(re.match(r'[^aeiou]ies$', s)):
        stem = s[:-1]
    elif(re.match(r'\w*(o|x|ch|sh|ss|zz)es$', s)):
        stem = s[:-2]
    elif(re.match(r'\w*(([^s]se)|([^z]ze))s$', s)):
        stem = s[:-1]
    elif(s == "has"):
        stem = "have"
    elif(re.match(r'\w*([^iosxz]|(^ch)|(^sh))es$', s)):
        stem = s[:-1]
    else:
        stem = ''

    if(re.match(r'(has)|(does)|(are)$', s)):
        return stem
    elif((stem, "VB") in btw or (s, "VBZ") in btw):
        return stem
    elif(not s == stem):
        return stem
    else:
        return ''
def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg

# End of PART A.
