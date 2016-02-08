from flask import Flask
from stop_words import get_stop_words
from nltk.stem.snowball import RussianStemmer
from nltk.tokenize import RegexpTokenizer
import gensim, re
import requests


def parseData():

    countVideo = 2
    for i in range(1, countVideo+1):
        srt = requests.get("http://www.ted.com/talks/subtitles/id/%s/lang/en/format/srt"%(i,))
        lst = str(srt.text).split('\n\n')
        lst = list(map(lambda s: s.split('\n')[2:], lst))
        text = ""
        for l in lst:
            for s in l:
                text+= s+ "\n"




if __name__ == "__main__":
    parseData()

