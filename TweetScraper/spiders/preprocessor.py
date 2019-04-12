import csv
import re
import string
import unicodedata
import nltk
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import time

tags = []
ats = []

stop_words = [' ', 'a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an', 'and', 'any', 'are', 'aren', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'couldn', "couldn't", 'd', 'did', 'didn', "didn't", 'do', 'does', 'doesn', "doesn't", 'doing', 'don', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn', "hadn't", 'has', 'hasn', "hasn't", 'have', 'haven', "haven't", 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'isn', "isn't", 'it', "it's", 'its', 'itself', 'just', 'll', 'm', 'ma', 'me', 'mightn', "mightn't", 'more', 'most', 'mustn', "mustn't", 'my', 'myself',
              'needn', "needn't", 'no', 'nor', 'not', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 're', 's', 'same', 'shan', "shan't", 'she', "she's", 'should', "should've", 'shouldn', "shouldn't", 'so', 'some', 'such', 't', 'than', 'that', "that'll", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was', 'wasn', "wasn't", 'we', 'were', 'weren', "weren't", 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'won', "won't", 'wouldn', "wouldn't", 'y', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']


def find(string):
    # findall() has been used
    # with valid conditions for urls in string                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        'rolling on the floor laughing my ass off'], ['sk8', 'skate'], ['asl', 'age, sex, location'], ['thx', 'thank you'], ['ttfn', 'ta'], ['ttyl', 'talk to you later'], ['u', 'you'], ['u2', 'you too'], ['u4e', 'yours for ever'], ['wb', 'welcome back'], ['wtf', 'what the fuck'], ['wtg', 'way to go!'], ['wuf', 'where are you from'], ['w8', 'wait...'], ['idc', 'i do not care'], ['idm', 'i do not mind'], ['idr', 'i do not remember'], ['idrm', 'i do not really mind'], ['rly', 'really'], ['rlly', 'really'], ['wth', 'what the heck'], ['lmfao', 'laughing my fucking ass off'], ['kys', 'kill your self'], ['kms', 'kill my self'], ['plz', 'please'], ['pls', 'please'], ['yea', 'yeh'], ['ye', 'yes'], ['bf', 'boyfriend'], ['gf', 'girlfriend'], ['smh', 'shaking my head'], ['cuz', 'because'], ['cuz', 'because'], ['cos', 'because'], ['omg', 'oh my god'], ['oml', 'oh my lord'], ['pic', 'picture'], ['wyd', 'what you doing'], ['wywd', 'what you want to do'], ['tb', 'text back'], ['bro', 'brother'], ['nm', 'nothing much'], ['nvm', 'never mind'], ['dm', 'direct message'], ['tbh', 'to be honest'], ['prob', 'probably'], ['probs', 'probably'], ['ly', 'love you']]
    url = re.findall(
        'http[s]?://[ ]?[www. [ ]?(?:[a-zA-Z]|[0-9]|[ ]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|pic.twitter(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|@(?:[a-zA-Z]|[0-9]|[_])+|@ (?:[a-zA-Z]|[0-9]|[_])+|#(?:[a-zA-Z]|[0-9])+|# (?:[a-zA-Z]|[0-9])+', string)
    if url:
        for i in url:
            if len(i) > 0:
                if i[0] == '#':
                    tags.append(i)
                elif i[0] == '@':
                    ats.append(i)
                string = string.replace(i.strip(), "")
    string = unicodedata.normalize('NFKD', string).encode(
        'ascii', 'ignore').decode('utf-8', 'ignore')
    string = re.sub(r'[^\w\s]', '', string)
    string = string.strip()
    if string != '' and len(string) != 0:
        return string
    return ""


def normalize(words):
    p = inflect.engine()
    new_words = []
    for word in words:

        if word.lower() not in stop_words:
            # if word != '':
            if word.isdigit():
                word = p.number_to_words(word)
                # print("final: " + word)
            if word != '':
                new_words.append(word.lower())

    return new_words


def replace_abv(string):
    slang = [['afk', 'away from keyboard'], ['asap', 'as soon as possible'], ['atk', 'at the keyboard'], ['atm', 'at the moment'], ['bak', 'back at keyboard'], ['b4n', 'bye for now'], ['brb', 'be right back'], ['brt', 'be right there'], ['btw', 'by the way'], ['b4', 'before'], ['b4n', 'bye for now'], ['cu', 'see you'], ['cul8r', 'see you later'], ['cya', 'see you'], ['faq', 'frequently asked questions'], ['fc', 'fingers crossed'], ['fwiw', 'for what it is worth'], ['fyi', 'for your information'], ['gal', 'get a life'], ['gg', 'good game'], ['gmta', 'great minds think alike'], ['gr8', 'great'], ['g9', 'genius'], ['ic', 'i see'], ['ily', 'i love you'], ['imho', 'in my honest/humble opinion'], ['iow', 'in other words'], ['irl', 'in real life'], ['ldr', 'long distance relationship'], ['lmao', 'laugh my ass off'], ['lol', 'laughing out loud'], ['ltns', 'long time no see'], ['l8r', 'later'], ['mte', 'my thoughts exactly'], ['m8', 'mate'], ['nrn', 'no reply necessary'], ['oic', 'oh i see'], ['prt', 'party'], ['prw', 'parents are watching'], ['rofl', 'rolling on the floor laughing'], ['roflol', 'rolling on the floor laughing out loud'], ['rotflmao',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            'rolling on the floor laughing my ass off'], ['sk8', 'skate'], ['asl', 'age, sex, location'], ['thx', 'thank you'], ['ttfn', 'ta'], ['ttyl', 'talk to you later'], ['u', 'you'], ['u2', 'you too'], ['u4e', 'yours for ever'], ['wb', 'welcome back'], ['wtf', 'what the fuck'], ['wtg', 'way to go!'], ['wuf', 'where are you from'], ['w8', 'wait...'], ['idc', 'i do not care'], ['idm', 'i do not mind'], ['idr', 'i do not remember'], ['idrm', 'i do not really mind'], ['rly', 'really'], ['rlly', 'really'], ['wth', 'what the heck'], ['lmfao', 'laughing my fucking ass off'], ['kys', 'kill your self'], ['kms', 'kill my self'], ['plz', 'please'], ['pls', 'please'], ['yea', 'yeh'], ['ye', 'yes'], ['bf', 'boyfriend'], ['gf', 'girlfriend'], ['smh', 'shaking my head'], ['cuz', 'because'], ['cuz', 'because'], ['cos', 'because'], ['omg', 'oh my god'], ['oml', 'oh my lord'], ['pic', 'picture'], ['wyd', 'what you doing'], ['wywd', 'what you want to do'], ['tb', 'text back'], ['bro', 'brother'], ['nm', 'nothing much'], ['nvm', 'never mind'], ['dm', 'direct message'], ['tbh', 'to be honest'], ['prob', 'probably'], ['probs', 'probably'], ['ly', 'love you']]
    for s in slang:
        if s[0] in string:
            string.replace(s[0], s[1])
    return string


def testDictionary(line):
    """Applying normalization to files"""
    # f = open(filename, "r")
    # f1 = f.readlines()
    test = {}
    # print("Line: " + line)
    # readf = open(filename2, 'a')
    # f1 = filename
    # for x in f1:

    test = line
    # print(test['text'])
    y = line['text']
    y = find(y)  # solo-0.30
    if y != None:
        y = replace_abv(y)  # solo-0.90 # 5k-10seconds
        y = y.split(" ")  # solo-0.2705 w/-16.83
    if y != None:
        y = normalize(y)  # solo-102.13  #5k-20seconds
    if y != None and len(y) != 0:
        y = " ".join(y)
    # readf.write(y+"\n")
    return y


# start_time = time.time()

# testDictionary(
#     "/Users/ShuaibReeyaz/Documents/GitHub/scrapy-tweets/Tweet PreProcessing/sample100k.txt", "text", "100kouttest2.txt")

# print("Finished TIME: %s " % (time.time() - start_time))
