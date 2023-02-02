from django.shortcuts import render

import nltk
from collections import Counter
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation
from heapq import nlargest

# import stop_words
from stop_words import get_stop_words
stopwords = get_stop_words('english')

# Create your views here.

def home(request):
    return render(request, "index.html")

def result(request):
    text = request.GET["text"]
    return render(request, "index.html", {"text":text})

def text_summerization(request):
    if request.method =="POST":
        text = request.POST["text"]
        tokens = word_tokenize(text.lower())
    
    words = []
    for word in tokens:
        if word not in stopwords:
            if word not in punctuation:
                words.append(word)
            
    count = Counter(words)     

    norm = {}
    for word in count:
        norm[word]=count[word]/len(count)
    
    sentence = sent_tokenize(text)

    sent_score = {}
    for sent in sentence:
        for word in word_tokenize(sent):
            if word in norm:
                if sent not in sent_score.keys():
                    sent_score[sent]=0
                else:
                    sent_score[sent]+=norm[word]

    final = []
    for i in nlargest(len(sent_score), sent_score, sent_score.get):
        final.append(i.capitalize())

    return render(request, "index.html", {"text": final})

