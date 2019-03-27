import csv
import re
import string
import unicodedata
import nltk
import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import time

sample = "don't"
tags = []
ats = []

stop_words = [' ', 'a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an', 'and', 'any', 'are', 'aren', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'couldn', "couldn't", 'd', 'did', 'didn', "didn't", 'do', 'does', 'doesn', "doesn't", 'doing', 'don', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn', "hadn't", 'has', 'hasn', "hasn't", 'have', 'haven', "haven't", 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'isn', "isn't", 'it', "it's", 'its', 'itself', 'just', 'll', 'm', 'ma', 'me', 'mightn', "mightn't", 'more', 'most', 'mustn', "mustn't", 'my', 'myself',
              'needn', "needn't", 'no', 'nor', 'not', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 're', 's', 'same', 'shan', "shan't", 'she', "she's", 'should', "should've", 'shouldn', "shouldn't", 'so', 'some', 'such', 't', 'than', 'that', "that'll", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was', 'wasn', "wasn't", 'we', 'were', 'weren', "weren't", 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'won', "won't", 'wouldn', "wouldn't", 'y', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']


def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)


def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode(
            'ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words


def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words


def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words


def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []

    for word in words:
        if word.lower() not in stop_words:
            new_words.append(word)
        # if word not in stopwords.words('english'):
        #     new_words.append(word)
    return new_words


# def stem_words(words):
#     """Stem words in list of tokenized words"""
#     stemmer = LancasterStemmer()
#     stems = []
#     for word in words:
#         stem = stemmer.stem(word)
#         stems.append(stem)
#     return stems


# def lemmatize_verbs(words):
#     """Lemmatize verbs in list of tokenized words"""
#     lemmatizer = WordNetLemmatizer()
#     lemmas = []
#     for word in words:
#         lemma = lemmatizer.lemmatize(word, pos='v')
#         lemmas.append(lemma)
#     return lemmas


def find(string):
    # findall() has been used
    # with valid conditions for urls in string
    url = re.findall(
        'http[s]?://[ ]?[www. [ ]?(?:[a-zA-Z]|[0-9]|[ ]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|pic.twitter(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|@(?:[a-zA-Z]|[0-9])+|@ (?:[a-zA-Z]|[0-9])+|#(?:[a-zA-Z]|[0-9])+|# (?:[a-zA-Z]|[0-9])+', string)
    # url2 = re.findall(
    #     'pic.twitter(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    # url3 = re.findall(
    #     '@(?:[a-zA-Z]|[0-9])+|@ (?:[a-zA-Z]|[0-9])+|#(?:[a-zA-Z]|[0-9])+|# (?:[a-zA-Z]|[0-9])+', string)
    # url4 = re.findall('#(?:[a-zA-Z]|[0-9])+|# (?:[a-zA-Z]|[0-9])+', string)
    # print(url)
    # url = url1 + url3
    # print(string + "--------------")

    if url:
        for i in url:
            if len(i) > 0:
                if i[0] == '#':
                    tags.append(i)
                elif i[0] == '@':
                    ats.append(i)
                string = string.replace(i.strip(), "")
    # print(string)
    return string.strip()


def normalize(words):
    words = remove_stopwords(words)  # solo-17.23
    words = remove_punctuation(words)  # solo-0.38
    words = remove_non_ascii(words)  # solo-0.30
    words = replace_numbers(words)  # solo-0.300
    # words = to_lowercase(words)  # solo-0.279

    return words
    # p = inflect.engine()
    # new_words = []
    # for word in words:
    #     # stop word
    #     if punc_word not in stopwords.words('english'):
    #         new_words.append(punc_word)
    #     # removeascii
    #     ascii_word = unicodedata.normalize('NFKD', low_word).encode(
    #         'ascii', 'ignore').decode('utf-8', 'ignore')
    #     # remove punctuation
    #     punc_word = re.sub(r'[^\w\s]', '', ascii_word)
    #     # replace numbers
    #     if punc_word.isdigit():
    #         punc_word = p.number_to_words(punc_word)

    #     # lower case
    #     low_word = word.lower()

    # return new_words


# def replace_abv(string):
#     slang = [['afk', 'away from keyboard'], ['asap', 'as soon as possible'], ['atk', 'at the keyboard'], ['atm', 'at the moment'], ['bak', 'back at keyboard'], ['b4n', 'bye for now'], ['brb', 'be right back'], ['brt', 'be right there'], ['btw', 'by the way'], ['b4', 'before'], ['b4n', 'bye for now'], ['cu', 'see you'], ['cul8r', 'see you later'], ['cya', 'see you'], ['faq', 'frequently asked questions'], ['fc', 'fingers crossed'], ['fwiw', 'for what it is worth'], ['fyi', 'for your information'], ['gal', 'get a life'], ['gg', 'good game'], ['gmta', 'great minds think alike'], ['gr8', 'great'], ['g9', 'genius'], ['ic', 'i see'], ['ily', 'i love you'], ['imho', 'in my honest/humble opinion'], ['iow', 'in other words'], ['irl', 'in real life'], ['ldr', 'long distance relationship'], ['lmao', 'laugh my ass off'], ['lol', 'laughing out loud'], ['ltns', 'long time no see'], ['l8r', 'later'], ['mte', 'my thoughts exactly'], ['m8', 'mate'], ['nrn', 'no reply necessary'], ['oic', 'oh i see'], ['prt', 'party'], ['prw', 'parents are watching'], ['rofl', 'rolling on the floor laughing'], ['roflol', 'rolling on the floor laughing out loud'], ['rotflmao',
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             'rolling on the floor laughing my ass off'], ['sk8', 'skate'], ['asl', 'age, sex, location'], ['thx', 'thank you'], ['ttfn', 'ta'], ['ttyl', 'talk to you later'], ['u', 'you'], ['u2', 'you too'], ['u4e', 'yours for ever'], ['wb', 'welcome back'], ['wtf', 'what the fuck'], ['wtg', 'way to go!'], ['wuf', 'where are you from'], ['w8', 'wait...'], ['idc', 'i do not care'], ['idm', 'i do not mind'], ['idr', 'i do not remember'], ['idrm', 'i do not really mind'], ['rly', 'really'], ['rlly', 'really'], ['wth', 'what the heck'], ['lmfao', 'laughing my fucking ass off'], ['kys', 'kill your self'], ['kms', 'kill my self'], ['plz', 'please'], ['pls', 'please'], ['yea', 'yeh'], ['ye', 'yes'], ['bf', 'boyfriend'], ['gf', 'girlfriend'], ['smh', 'shaking my head'], ['cuz', 'because'], ['cuz', 'because'], ['cos', 'because'], ['omg', 'oh my god'], ['oml', 'oh my lord'], ['pic', 'picture'], ['wyd', 'what you doing'], ['wywd', 'what you want to do'], ['tb', 'text back'], ['bro', 'brother'], ['nm', 'nothing much'], ['nvm', 'never mind'], ['dm', 'direct message'], ['tbh', 'to be honest'], ['prob', 'probably'], ['probs', 'probably'], ['ly', 'love you']]
#     string = string.split(" ")
#     j = 0
#     for _str in string:
#         if len(_str) <= 5:
#             _str = re.sub('[^a-zA-Z0-9-_.]', '', _str)
#             for s in slang:
#                 if _str.lower() == s[0]:
#                     string[j] = s[1]
#                     break
#             j = j+1
#     return ' '.join(string)

def replace_abv(string):
    slang = [['afk', 'away from keyboard'], ['asap', 'as soon as possible'], ['atk', 'at the keyboard'], ['atm', 'at the moment'], ['bak', 'back at keyboard'], ['b4n', 'bye for now'], ['brb', 'be right back'], ['brt', 'be right there'], ['btw', 'by the way'], ['b4', 'before'], ['b4n', 'bye for now'], ['cu', 'see you'], ['cul8r', 'see you later'], ['cya', 'see you'], ['faq', 'frequently asked questions'], ['fc', 'fingers crossed'], ['fwiw', 'for what it is worth'], ['fyi', 'for your information'], ['gal', 'get a life'], ['gg', 'good game'], ['gmta', 'great minds think alike'], ['gr8', 'great'], ['g9', 'genius'], ['ic', 'i see'], ['ily', 'i love you'], ['imho', 'in my honest/humble opinion'], ['iow', 'in other words'], ['irl', 'in real life'], ['ldr', 'long distance relationship'], ['lmao', 'laugh my ass off'], ['lol', 'laughing out loud'], ['ltns', 'long time no see'], ['l8r', 'later'], ['mte', 'my thoughts exactly'], ['m8', 'mate'], ['nrn', 'no reply necessary'], ['oic', 'oh i see'], ['prt', 'party'], ['prw', 'parents are watching'], ['rofl', 'rolling on the floor laughing'], ['roflol', 'rolling on the floor laughing out loud'], ['rotflmao',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'rolling on the floor laughing my ass off'], ['sk8', 'skate'], ['asl', 'age, sex, location'], ['thx', 'thank you'], ['ttfn', 'ta'], ['ttyl', 'talk to you later'], ['u', 'you'], ['u2', 'you too'], ['u4e', 'yours for ever'], ['wb', 'welcome back'], ['wtf', 'what the fuck'], ['wtg', 'way to go!'], ['wuf', 'where are you from'], ['w8', 'wait...'], ['idc', 'i do not care'], ['idm', 'i do not mind'], ['idr', 'i do not remember'], ['idrm', 'i do not really mind'], ['rly', 'really'], ['rlly', 'really'], ['wth', 'what the heck'], ['lmfao', 'laughing my fucking ass off'], ['kys', 'kill your self'], ['kms', 'kill my self'], ['plz', 'please'], ['pls', 'please'], ['yea', 'yeh'], ['ye', 'yes'], ['bf', 'boyfriend'], ['gf', 'girlfriend'], ['smh', 'shaking my head'], ['cuz', 'because'], ['cuz', 'because'], ['cos', 'because'], ['omg', 'oh my god'], ['oml', 'oh my lord'], ['pic', 'picture'], ['wyd', 'what you doing'], ['wywd', 'what you want to do'], ['tb', 'text back'], ['bro', 'brother'], ['nm', 'nothing much'], ['nvm', 'never mind'], ['dm', 'direct message'], ['tbh', 'to be honest'], ['prob', 'probably'], ['probs', 'probably'], ['ly', 'love you']]

    for s in slang:
        if s[0] in string:
            string.replace(s[0], s[1])

    # for _str in string:
    #     _str = re.sub('[^a-zA-Z0-9-_.]', '', _str)

    return string


def replaceBoolean(filename):
    """Replace all lowecase true and false with True and False"""
    f = open(filename, 'r')
    filedata = f.read()
    f.close()
    newdata = filedata.replace("true", "True")
    newdata = newdata.replace("false", "False")
    f = open(filename, 'w')
    f.write(newdata)
    f.close()


def testDictionary(filename, key, filename2):
    """Applying normalization to files"""
    f = open(filename, "r")
    f1 = f.readlines()
    test = {}
    readf = open(filename2, 'a')
    for x in f1:
        test = eval(x)
        y = test[key]
        # 5k - total 60 seconds

        y = find(y.strip())  # solo-0.30
        # print(y)
        y = replace_abv(y)  # solo-0.90 # 5k-10seconds
        # y = replace_contractions(y)  # solo-1.36
        # print(y)
        # y = nltk.word_tokenize(y)  # solo-1.569
        y = y.split(" ")  # solo-0.2705 w/-16.83
        y = normalize(y)  # solo-102.13  #5k-20seconds
        # print(y)
        if len(y) > 0:
            y = str(y)
            readf.write(y+"\n")
        # readf.write("\n")
        # print(y)


start_time = time.time()

testDictionary("sample1mil.txt", "text", "1milout3.txt")

print("Finished TIME: %s " % (time.time() - start_time))

# def testDictionary(filename):

#     """Applying normalization to files"""
#     f=open(filename,"r")
#     f1=f.readlines()
#     test={}
#     i=0
#     ftext = str(f1)


#     # ftext = find(ftext)
#     # print("URL TIME: %s " % (time.time()- start_time))
#     # ftext = replace_abv(ftext)
#     # print("Abv TIME: %s " % (time.time()- start_time))
#     # print(f1)
#     for x in f1:
#         # test=eval(x)
#         # y=test[key]

#         y = x
#         y = find(y)
#         y = replace_abv(y)
#         y = replace_contractions(y)
#         y = nltk.word_tokenize(y)
#         y = normalize(y)
#         y = remove_non_ascii(y)
#         readf= open("100out.txt",'a')
#         y=str(y)
#         readf.write(y)
#         readf.write("\n")
#         i = i+1
#         print(i)
#         if ((time.time()- start_time) // 120):
#             print("Update TIME: %s " % (time.time()- start_time))


# # testDictionary("@Adele.txt","text","@Adele3.txt")
# start_time = time.time()

# testDictionary("sample100.txt")

# print("TIME: %s " % (time.time()- start_time))

# words = "sanhttps:// motherofalllists.com/2018/08/13/pos tpartum-psychosis/ \u00a0 \u2026 pic.twitter.com/hLmmKaTkOa amazing vied"
# words = replace_contractions(words)
# words = nltk.word_tokenize(words)
# words = normalize(words)
# words = remove_non_ascii(words)

# print(words)
