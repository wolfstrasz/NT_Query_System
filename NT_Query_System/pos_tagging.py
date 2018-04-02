# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen
# Revised November 2016 by Adam Lopez

# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'),
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    allNouns = {}
    unchangingPlurals = []
    with open("sentences.txt", "r") as f:
        for line in f:
            singleword = line.split(' ')
            for pair in singleword:
                (word,cat) = pair.split("|")

                if(cat == "NN"):
                    if(allNouns.get(word) == "NNS"):
                        if(unchangingPlurals.count(word) == 0):
                            unchangingPlurals.append(word)
                    else:
                        allNouns[word] = "NN"

                elif(cat == "NNS"):
                    if(allNouns.get(word) == "NN"):
                        if(unchangingPlurals.count(word) == 0):
                            unchangingPlurals.append(word)
                    else:
                        allNouns[word] = "NNS"
    
    return unchangingPlurals

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""
    if(s in unchanging_plurals_list):
        return s
    elif(re.match(r'\w*ves', s)):
        return s[:-3] + 'f'
    elif(re.match(r'\w*([^aeiousxyzh]|(^ch)|(^sh))s$', s)):
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
    return stem
    #? Check piazza if we need to check the brown corpus

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    wordTags = []
    if(wd in function_words):
        for word_tag in function_words_tags:
            if(word_tag[0] == wd):
                wordTags.append(word_tag[1])

    if(wd in lx.getAll('P')):
        wordTags.append('P')

    if(wd in lx.getAll('N')):
       wordTags.append("Ns")
    if(noun_stem(wd) in lx.getAll('N')):
        wordTags.append("Np")

    if(wd in lx.getAll('A')):
        wordTags.append('A')

    if(wd in lx.getAll('I')):
       wordTags.append("Ip")
    if(verb_stem(wd) in lx.getAll('I')):
        wordTags.append("Is")

    if(wd in lx.getAll('T')):
        wordTags.append("Tp")
    if(verb_stem(wd) in lx.getAll('T')):
        wordTags.append("Ts")

    return wordTags

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
