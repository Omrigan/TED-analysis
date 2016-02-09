from flask import Flask
from stop_words import get_stop_words
from nltk.stem.snowball import RussianStemmer, EnglishStemmer
from nltk.tokenize import RegexpTokenizer
import gensim, re
import requests
from pymongo import MongoClient
import pyquery


def parseData():
    client = MongoClient()
    texts = client.test.texts
    texts.remove()
    countVideo = 2400
    for i in range(1, countVideo + 1):
        srt = requests.get("http://www.ted.com/talks/subtitles/id/%s/lang/en/format/srt" % (i,))

        if (srt.status_code == 200 and requests.get('http://www.ted.com/talks/%s' % (i,)).status_code == 200):
            lst = str(srt.text).split('\n\n')
            lst = list(map(lambda s: s.split('\n')[2:], lst))
            text = ""
            for l in lst:
                for s in l:
                    text += s + "\n"

            pq = pyquery.PyQuery(url='http://www.ted.com/talks/%s' % (i,))

            views = pq('div#sharing-count').text()
            comments = pq('.talk-section .h11').text()
            title = pq('#player-hero .player-hero__title__content').text()
            speaker = pq('#player-hero .player-hero__speaker').text()[:-1]
            r = re.compile('\D')
            views = r.sub('', views)
            comments = r.sub('', comments)
            views = int(views)
            comments = int(comments)
            talk = {
                'id': i,
                'title': title,
                'speaker': speaker,
                'text': text,
                'views': views,
                'comments': comments
            }
            texts.insert_one(talk)
            print(i)


global p_stemmer


def stemmer(stemmer, word):
    # return word
    return stemmer.stem(word)


def textToWordList(txt):
    p_stemmer = EnglishStemmer()
    tokenizer = RegexpTokenizer(r'\w+')
    badword = [
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
        'applaus',
        'think',
        'want',
        'make',
        'get',
        'realli'
    ]
    stop_w = [stemmer(p_stemmer, i) for i in get_stop_words('en')]
    badword = [stemmer(p_stemmer, i) for i in badword]
    # r = re.compile('^[а-я]+$')
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
    for talk in texts.find():
        wordLists.append(textToWordList(talk['text']))
    print("WordLists builded")
    dictionary = gensim.corpora.Dictionary(wordLists)
    corpus = [dictionary.doc2bow(text) for text in wordLists]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=15, id2word=dictionary, passes=20)
    ldamodel.save("my_model")
    for topic in ldamodel.print_topics(num_words=7):
        print(topic)


def analysisTalks():
    ldamodel = gensim.models.ldamodel.LdaModel.load("my_model")
    client = MongoClient()
    texts = client.test.texts
    topics = client.test.topics
    topics.remove()
    topics_dict = {}
    for topic in ldamodel.show_topics(num_topics=15, num_words=10):
        topics_dict[topic[0]] = {
            'id': topic[0],
            'keywords': topic[1],
            'simple-name': '',
            'rating': {
                'speak': 0,
                'view': 0,
                'discuss': 0
            }}
    rating_sum = {
        'speak': 0,
        'view': 0,
        'discuss': 0

    }
    for talk in texts.find():
        tokens = textToWordList(talk['text'])
        dictionary = gensim.corpora.Dictionary([tokens, ])
        for topic in ldamodel[dictionary.doc2bow(tokens)]:
            topics_dict[topic[0]]['rating']['speak'] += topic[1]
            topics_dict[topic[0]]['rating']['view'] += topic[1] * talk['views']
            topics_dict[topic[0]]['rating']['discuss'] += topic[1] * talk['comments']
            rating_sum['speak'] += topic[1]
            rating_sum['view'] += topic[1] * talk['views']
            rating_sum['discuss'] += topic[1] * talk['comments']
    for topic in topics_dict.values():
        topic['rating-percent']={}
        for rat in topic['rating']:
            topic['rating-percent'][rat] = topic['rating'][rat]*100/rating_sum[rat]
        print(topic)
        topics.insert(topic)

from flask import Flask
app = Flask(__name__)

@app.route("/")
def getTopics():
    client = MongoClient()
    topics = client.test.topics
    return str(list(topics.find()))







if __name__ == "__main__":
    # parseData()
    # analysis()
    #analysisTalks()
    app.run(debug=True)