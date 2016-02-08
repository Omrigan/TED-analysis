from flask import Flask
from stop_words import get_stop_words
from nltk.stem.snowball import RussianStemmer
from nltk.tokenize import RegexpTokenizer
import gensim, re
import requests
from pymongo import MongoClient




def parseData():
    client = MongoClient()
    texts = client.test.texts
    texts.remove()
    countVideo = 10
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

def textToWordList(txt):
    p_stemmer = RussianStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    badword =[
        'so',
        'to'
    ]
    stop_w =  [p_stemmer.stem(i) for i in get_stop_words('en')]
    badword = [p_stemmer.stem(i) for i in badword(txt)]
    #r = re.compile('^[а-я]+$')
    txt = txt.lower()
    tokens = [p_stemmer.stem(i) for i in tokenizer.tokenize(txt)]
    tokens = [i for i in tokens if not i in stop_w]
    tokens = [i for i in tokens if not i in badword]
    return tokens


def analysis():
    client = MongoClient()
    texts = client.test.texts
    wordLists = []
    for text in texts.find():
        wordLists.append(textToWordList(text['text']))

    dictionary = gensim.corpora.Dictionary(wordLists)
    corpus = [dictionary.doc2bow(text) for text in wordLists]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=6, id2word = dictionary, passes=20)
    ldamodel.save("my_model.txt")
    for topic in ldamodel.print_topics(num_words=7):
        print(topic)







if __name__ == "__main__":
    # parseData()
    analysis()

