from flask import Flask
from stop_words import get_stop_words
from nltk.stem.snowball import RussianStemmer, EnglishStemmer
from nltk.tokenize import RegexpTokenizer
import gensim, re
import requests
from pymongo import MongoClient




def parseData():
    client = MongoClient()
    texts = client.test.texts
    texts.remove()
    countVideo = 2400
    for i in range(1, countVideo+1):
        srt = requests.get("http://www.ted.com/talks/subtitles/id/%s/lang/en/format/srt"%(i,))
        lst = str(srt.text).split('\n\n')
        lst = list(map(lambda s: s.split('\n')[2:], lst))
        text = ""
        for l in lst:
            for s in l:
                text+= s+ "\n"
        doc = {
            'id': i,
            'text': text
        }
        texts.insert_one(doc)
        print(i)
global p_stemmer
def stemmer(stemmer, word):
    #return word
    return stemmer.stem(word)


def textToWordList(txt):
    p_stemmer = EnglishStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    badword =[
        'so',
        'to',
        're',
        've',
        's',
        't',
        'can',
        'go',
        'one',
        'like',
        'now',
        'see',
        'look',
        'know',
        'm',
        'just',
        'now',
        'thing',
        'applaus'
    ]
    stop_w =  [stemmer(p_stemmer, i) for i in get_stop_words('en')]
    badword = [stemmer(p_stemmer, i) for i in badword]
    #r = re.compile('^[а-я]+$')
    txt = txt.lower()
    tokens = tokenizer.tokenize(txt)
    tokens = [stemmer(p_stemmer, i) for i in tokens]
    tokens = [i for i in tokens if not i in stop_w]
    tokens = [i for i in tokens if not i in badword]
    return tokens


def analysis():
    client = MongoClient()
    texts = client.test.texts
    wordLists = []
    for text in texts.find():
        wordLists.append(textToWordList(text['text']))
    print("WordLists builded")
    dictionary = gensim.corpora.Dictionary(wordLists)
    corpus = [dictionary.doc2bow(text) for text in wordLists]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word = dictionary, passes=20)
    ldamodel.save("my_model.txt")
    for topic in ldamodel.print_topics(num_words=7):
        print(topic)







if __name__ == "__main__":
    #parseData()
    analysis()

