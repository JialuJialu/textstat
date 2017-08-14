from __future__ import print_function
import pkg_resources
import string
import math
import operator

_all_ = [readability_scores,list_implemented_scores,char_count,syllable_count,sentence_count,avg_sentence_length,avg_syllables_per_word,avg_letter_per_word,polysyllabcount]

exclude = list(string.punctuation)
easy_word_set = set([ln.strip() for ln in pkg_resources.resource_stream('textstat', 'easy_words.txt')])

def char_count(txt, ignore_spaces=True):
    """
    Function to return total character counts in a text, pass the following parameter
    ignore_spaces = False
    to ignore whitespaces
    """
    if ignore_spaces:
        text = txt.replace(" ", "")
        return len(text)
    else:
        return len(txt)
    

def syllable_count(txt_given):
    """
    Function to calculate syllable words in a text.
    I/P - a text
    O/P - number of syllable words
    """
    count = 0
    vowels = 'aeiou'
    extendedvowels = 'aeiouy'
    text = txt_given.lower()
    text = "".join(x for x in text if x not in exclude)

    if text is None:
        return 0
    elif len(text) == 0:
        return 0
    else:
        if text[0] in vowels:
            count += 1
        for index in range(1, len(text)):
            if text[index] in extendedvowels and text[index-1] not in vowels:
                count += 1
#             if text.endswith('e') and (text[-2] != "l" or (text[-3] in vowels)):
        if text.endswith('e') and (not text.endswith("le")):
            #discard trailing "e", except where ending is "le", but include words like pale, male, mole
            count -= 1
        if count == 0:
            count += 1
        return count

def sentence_count(txt):
    """
    Sentence count of a text
    """
    ignoreCount = 0
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', txt)
    for sentence in sentences:
        if lexicon_count(sentence) <= 2:
            ignoreCount = ignoreCount + 1
    return max(1, len(sentences) - ignoreCount)

    
def avg_sentence_length(lc,sc):
    try:
        ASL = float(lc)/sc
        return round(ASL, 2)
    except:
        print("Error(ASL): Sentence Count is Zero, Cannot Divide")
        return

def avg_syllables_per_word(syllable_c,lc):
    try:
        ASPW = float(syllable_c)/float(lc)
        return round(ASPW, 2)
    except:
        print("Error(ASyPW): Number of words are zero, cannot divide")
        return

def avg_letter_per_word(char_c,lc):
    try:
        ALPW = float(char_c)/float(lc)
        return round(ALPW, 2)
    except:
        print("Error(ALPW): Number of words are zero, cannot divide")
        return

    
def polysyllabcount(wordlist):
    count = 0
    for word in wordlist:
        wrds = syllable_count(word)
        if wrds >= 3:
            count += 1
    return count

    
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

def automated_readability_index(char_c,lc,sc):
    try:
        a = float(char_c)/lc
        b = float(char_c)/sc
        ARI = (4.71 * round(a, 2)) + (0.5*round(b, 2)) - 21.43
        return round(ARI, 2)
    except Exception as E:
        print("Error(ARI) : Sentence count is zero, cannot divide")
        return None

def linsear_write_formula(wordlist,sc,lc):
    easy_word = []
    difficult_word = []

    Number = 0
    for value in wordlist:
        try:
            if syllable_count(value) < 3:
                easy_word.append(value)
            elif syllable_count(value) > 3:
                difficult_word.append(value)
            Number = float((len(easy_word)*1 + len(difficult_word)*3)/float(sc)*100/float(lc))
            if Number > 20:
                Number /= 2
            else:
                Number = (Number-2)/2
        except Exception as E:
            print("Error (LWF): ", E)
    return float(Number)

def difficult_words(wordlist):
    diff_words_set = set()
    for value in wordlist:
        if value not in easy_word_set:
            if syllable_count(value) > 1:
                if value not in diff_words_set:
                    diff_words_set.add(value)
    return len(diff_words_set)

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
        per_diff_words = (float(dw_c)/lc*100) + 5
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

def list_implemented_scores:
	print(default_list_of_scores)
        
def readability_scores(text,default_scores=default_list_of_scores):
	wordlist_ = [ch for ch in txt if ch not in exclude]
	lc = float(len(wordlist_))
	sc = float(sentence_count(text))
	syllable_c = float(syllable_count(text))
	char_c = float(char_count(text))
	
	ASL = float(avg_sentence_length(ls,sc))
	ASW = float(avg_syllables_per_word(syllable_c,lc))
	ALW = float(avg_letter_per_word(char_c,lc))
	poly_syllab = polysyllabcount(wordlist_)
	dw_c = difficult_words(text)
	
	score_dict = {}
	if "flesch reading ease" in default_scores:
		score_dict["flesch reading ease"] = flesch_reading_ease(ASL,ASW)
	if "smog index" in default_scores:
		score_dict["smog index"] = smog_index(poly_syllab,sc)
	if "flesch reading grade" in default_scores:
		score_dict["flesch reading grade"] = flesch_reading_ease(ASL,ASW)
	if "coleman liau index" in default_scores:
		score_dict["coleman liau index"] = coleman_liau_index(ALW, ASL)
	if "linsear write formula" in default_scores:
		score_dict["linsear write formula"] = linsear_write_formula(wordlist_,sc,lc)
	if "lix" in default_scores:
		score_dict["lix"] = lix(wordlist_,ASL,lc)
	if "gunning fog" in default_scores:
		score_dict["gunning fog index"] = gunning_fog(dw_c,lc,ASL)
	if "dale chall" in default_scores:
		score_dict["dale chall"] = dale_chall_readability_score(lc,dw_c,ASL)
	if "automated" in default_scores:
		score_dict["automated"] =  automated_readability_index(char_c,lc,sc)
	
	return score_dict
	
	
	
	