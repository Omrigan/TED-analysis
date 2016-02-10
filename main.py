from flask import Flask
from stop_words import get_stop_words
from nltk.stem.snowball import RussianStemmer, EnglishStemmer
from nltk.tokenize import RegexpTokenizer
import gensim, re
import requests
from pymongo import MongoClient
import pyquery


from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def getTopics():
    client = MongoClient()
    topics = client.test.topics
    return render_template('topics.html', topics=list(topics.find()))


@app.route("/about")
def about():
    return render_template('about.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)