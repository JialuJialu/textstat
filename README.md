textstat
========

Python package to calculate statistics from text, which helps to decide readability, complexity and grade level of a particular corpus.

(Still Testing)
-------

Difference between this Fork and its Master
-------
In short, this version greatly optimized the time efficiency, especially in the case that the user need several readability scores of a test text. Consequently, it requires a change in the usage.
 
Though there are various readability scores (also called textstat), they are all based on a limited set of measurements of the text, i.e. average sentence length, average syllable count per word, average character per word, etc. In the original version at the master, these results are calculated repeatedly when the user asks for more than one readability scores of a certain text. This version of implemetation calculate them all once and pass them to readability score functions wanted by the user. 

This version also gets rid of some other repetitive calculations and implements syllable count differently. The master version is using the number of possible hyphenizations as the number of syllables in a word, but at least for the project I am working on, it makes more sense to use vowel-based syllable count, so I change it.


Install
-------

You can install textstat either via the Python Package Index (PyPI) or from source.

To install using pip:

```python
	$ pip install textstat
```	

To install using easy_install:

```python	
	$ easy_install textstat
```

Downloading and installing from source

Download the latest version of textstat from http://pypi.python.org/pypi/textstat/

You can install it by doing the following,:

```python
    $ tar xfz textstat-*.tar.gz
   
    $ cd textstat-*/
   
    $ python setup.py build
   
    $ python setup.py install # as root
```
List of Functions
----
### Character Count

function name - char_count(txt, ignorespaces=True):

Function to return total character counts in a text, pass the following parameter

    ignorespaces = False
to ignore whitespaces
    
### Syllable Count

function name - syllable_count(text)

returns - the number of syllables present in the given text.

### Lexicon Count

function name - lexicon_count(wordlist, TRUE/FALSE)

wordlist is supposed to be the the list of all words in the test text. It can be obtained by 

	wordlist = [ch for ch in txt if ch not in exclude]

Calculates the number of words present in the text.
TRUE/FALSE specifies whether we need to take in account in punctuation symbols while counting lexicons or not.
Default value is TRUE, which removes the punctuation before counting lexicons.

### Sentence Count

function name - sentence_count(text)

returns the number of sentences present in the given text.

### Readability Scores

function name - readability_scores(text,defaultscores)

If not specified

	defaultscores = ["flesch_ease","smog","flesch_grade","coleman_liau","automated",
          "dale_chall","linsear_write","lix","gunning_fog"]

returns a dictionary of requested scores:

	example_return_dict = {"flesch_ease":10,"smog":10,"flesch_grade":10,"coleman_liau":10,"automated":10,
          "dale_chall":10,"linsear_write":10,"lix":10,"gunning_fog":10}

### Average Sentence Length
function name - avg\_sentence\_length (lexicon count,sentence count)

### Average Syllables per word

function name - avg\_syllables\_per_word(syllable_count,lexicon_count)

### Average Letters Per word

function name - avg\_letter\_per\_word(character count,lexicon count)

### Polysyllble words count

function name - polysyllabcount(wordlist)

returns the number of words that have more than two syllables


Usage
----------
```python
from textstat.textstat import textstat
if __name__ == '__main__':
		test_data = """Playing games has always been thought to be important to the development of well-balanced and creative children; however, what part, if any, they should play in the lives of adults has never been researched that deeply. I believe that playing games is every bit as important for adults as for children. Not only is taking time out to play games with our children and other adults valuable to building interpersonal relationships but is also a wonderful way to release built up tension."""

	print readability_scores(test_data,list_of_scores_wanted)
	
```







