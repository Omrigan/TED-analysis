#!/usr/bin/python3.4
from pymongo import MongoClient
import pyquery
import secret_settings

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def getTopics():
    client = MongoClient(secret_settings.address)
    topics = client.test.topics
    return render_template('topics.html', topics=list(topics.find()))


@app.route("/about")
def about():
    return render_template('about.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)