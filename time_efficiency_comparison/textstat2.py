import numpy as np
import re
from collections import defaultdict

easy_word_set = set()
with open("easy_words.txt") as f:
    for wd in f:
        easy_word_set.add(wd.strip())


def char_count(wordlist):
    """
    Function to return total character counts in a text, pass the following parameter
    ignore_spaces = False
    to ignore whitespaces
    """
    mp = map((lambda x: len(x)),wordlist)
    return np.sum(list(mp))

def syllable_count(text):
    """
    Function to calculate syllable words in a text.
    I/P - a text
    O/P - number of syllable words
    the given text should be a single word
    """
    count = 0
    vowels = set(['a','e','i','o','u'])
    extendedvowels = set(['a','e','i','o','u','y'])

    if text == None or text == "":
        return 0
    else:
        if text[0] in vowels:
            count += 1
        for index,lt in enumerate(text[1:]):
            if lt in extendedvowels:
                if text[index] not in vowels:
                    count += 1
        if text[-1]=='e':
            if text[-2:]!="le":
                count -= 1
        if count == 0:
            count = 1
        return count

def sentence_count(txt):
    """
    Sentence count of a text
    """
    ignoreCount = 0
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', txt)
    for sentence in sentences:
        if len(sentence.split()) <= 2:
            ignoreCount = ignoreCount + 1
    return max(1, len(sentences) - ignoreCount)

def avg_sentence_length(lc,sc):
    try:
        ASL = float(lc)/sc
        return round(ASL, 2)
    except:
        print("Error(ASL): Sentence Count is Zero, Cannot Divide")
        return

def avg_syllables_per_word(dc,lc):
    return((np.sum(list(dc.values())))/lc )

def avg_letter_per_word(char_c,lc):
    try:
        ALPW = float(char_c)/float(lc)
        return round(ALPW, 2)
    except:
        print("Error(ALPW): Number of words are zero, cannot divide")
        return


def polysyllabcount(wordlist):
    count = 0
    dict_syllable = defaultdict(int)
    for word in wordlist:
        wrds = syllable_count(word)
        dict_syllable[word] += wrds
        if wrds >= 3:
            count += 1
    return count,dict_syllable


def flesch_reading_ease(ASL,ASW):
    FRE = 206.835 - float(1.015 * ASL) - float(84.6 * ASW)
    return round(FRE, 2)

def flesch_kincaid_grade(ASL,ASW):
    FKRA = float(0.39 * ASL) + float(11.8 * ASW) - 15.59
    return round(FKRA, 2)


def smog_index(poly_syllab,sc):
    if sc >= 3:
        try:
            SMOG = (1.043 * (30*(float(poly_syllab)/sc))**.5) + 3.1291
            return round(SMOG, 2)
        except:
            print("Error(SI): Sentence count is zero, cannot divide")
    else:
        return 0

def coleman_liau_index(ALW, ASL):
    CLI = (0.058 * ALW *100) - (29.6 /float(ASL)) - 15.8
    return round(CLI, 2)

def automated_readability_index(ALW,ASL):
    try:
        ARI = (4.71 * round(ALW, 2)) + (0.5*round(ASL, 2)) - 21.43
        return round(ARI, 2)
    except Exception as E:
        print("Error(ARI) : Sentence count is zero, cannot divide")
        return None

def linsear_write_formula(wordlist,sc,lc,dictionary):
    easy_word = 0
    complex_word = 0

    Number = 0
    try:
        for value in wordlist:
            if dictionary[value] < 3:
                easy_word+=1
            elif value not in easy_word_set:
                complex_word+=1
        difficult_word= lc -easy_word
        Number = float(easy_word + difficult_word*3)/float(sc)*100/float(lc)
        if Number > 20:
            Number /= 2
        else:
            Number = (Number-2)/2
    except Exception as E:
        print("Error (LWF): ", E)
    return float(Number),complex_word


def difficult_words(wordlist):
    diff_words_set = set()
    for value in wordlist:
        if value not in easy_word_set:
            diff_words_set.add(value)
    return len(diff_words_set)


#     dw_c = difficult_words(self.txt)
def dale_chall_readability_score(lc,dw_c,ASL):
    if lc > 0:
        difficult_words = float(dw_c)/lc*100
    else:
        print("Error(DCRS): Word Count is zero cannot divide")
        return None

    if difficult_words > 5:
        score = (0.1579 * difficult_words) + (0.0496 * ASL) + 3.6365
    else:
        score = (0.1579 * difficult_words) + (0.0496 * ASL)
    return round(score, 2)

def gunning_fog(dw_c,lc,ASL):
    try:
        per_diff_words = (float(dw_c)/lc*100)
        grade = 0.4*(ASL + per_diff_words)
        return grade
    except:
        print("Error(GF): Word Count is Zero, cannot divide")

def lix(wordlist,ASL,lc):
    long_words = len([wrd for wrd in wordlist if len(wrd)>6])
    per_long_words = (long_words) * 100/float(lc)
    lix = ASL + per_long_words
    return lix


default_list_of_scores = ["flesch_reading_ease","smog index","flesch reading grade","coleman liau index","automated",
          "dale chall","linsear write formula","lix","gunning_fog"]

def list_implemented_scores():
	print(default_list_of_scores)

def readability_scores(text_data,interested_scores=default_list_of_scores,displayindex=False):
    wordlist_= re.findall(r'[a-z\'-]+',text_data)
    lc = float(len(wordlist_))
    sc = float(sentence_count(text_data))
    char_c = float(char_count(wordlist_))

    ASL = float(avg_sentence_length(lc,sc))
    ALW = float(avg_letter_per_word(char_c,lc))
    poly_syllab,syllabdict = polysyllabcount(wordlist_)
    ASW = avg_syllables_per_word(syllabdict,lc)
    dw_c = difficult_words(wordlist_)

    if displayindex == True:
        index_dict = {}
        index_dict["word_count"]=lc
        index_dict["sentence_count"]=sc
        index_dict["character_count"]=char_c
        index_dict["avg_syllables_per_word"]=ASW
        index_dict["avg_letter_per_word"]=ALW
        index_dict["avg_sentence_length"]=ASL
        index_dict["percentage of polysyllable words"]=poly_syllab/float(lc)

    score_dict = {}
    complex_word_count = -1
    if "flesch reading ease" in interested_scores:
        score_dict["flesch reading ease"] = flesch_reading_ease(ASL,ASW)
    if "smog index" in interested_scores:
        score_dict["smog index"] = smog_index(poly_syllab,sc)
    if "flesch reading grade" in interested_scores:
        score_dict["flesch reading grade"] = flesch_kincaid_grade(ASL,ASW)
    if "coleman liau index" in interested_scores:
        score_dict["coleman liau index"] = coleman_liau_index(ALW, ASL)
    if "linsear write formula" in interested_scores:
        score_dict["linsear write formula"],complex_word_count = linsear_write_formula(wordlist_,sc,lc,syllabdict)
    if "lix" in interested_scores:
        score_dict["lix"] = lix(wordlist_,ASL,lc)
    if "gunning fog" in interested_scores:
        if complex_word_count == -1:
            complex_word_count = linsear_write_formula(wordlist_,sc,lc,syllabdict)[1]
        score_dict["gunning fog index"] = gunning_fog(complex_word_count,lc,ASL)
    if "dale chall" in interested_scores:
        score_dict["dale chall"] = dale_chall_readability_score(lc,dw_c,ASL)
    if "automated" in interested_scores:
        score_dict["automated"] =  automated_readability_index(ALW,ASL)

    if displayindex == True:
        return score_dict,index_dict
    else:
        return score_dict

_all_ = [readability_scores,list_implemented_scores]
