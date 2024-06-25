from ast import Num
from genericpath import isdir
import os
import json

#Function get_outgoing_links will go in the Data directory and access the json for the URL given
#It will then load each json file and extract list of outgoing links
def get_outgoing_links(URL):
    #Formatted means to format the url given in order to access each json file in Data
    formatedURL = URL.replace("/","#")
    formatedURL += ".json"
    dirPath = os.path.join("Data",formatedURL)
    if os.path.isfile(dirPath):
        with open(dirPath,"r") as file:
            data = json.load(file)
        return(data["outgoingLinks"])
    else:
        return None

#Function getOugoingLinks will go into Calculations directory and load one json file
#This json file will have all URL's incoming links
def get_incoming_links(URL):
    dirPath = os.path.join("IncomingLinksFile","incomingLinksList.json")
    if os.path.isfile(dirPath):
        with open(dirPath,"r") as file:
            data = json.load(file)
        if URL not in data:
            return None
        return data[URL]
    else:
        return None


#Function getPageRank will access PageRanks dir and access given url's file to return the pageRank value
def get_page_rank(URL):
    formatedURL = URL.replace("/","#")
    formatedURL += ".json"
    pagePath = os.path.join("PageRanks",formatedURL)
    if os.path.isfile(pagePath):
        with open(pagePath,"r") as file:
            data = json.load(file)
        return data
    else:
        return -1

#Function getIdf will access WordsAppeared Dir and load the json file of all idfs
#It will then get the Idf from the dictionary
def get_idf(word):
    if os.path.isdir("WordsAppeared"):
        path = os.path.join("WordsAppeared","IDF.json")
        if os.path.isfile(path):
            with open(path,"r") as file:
                data = json.load(file)
            if word in data:
                return data[word]
            else:
                return 0
        else:
            return 0
    else:
        return 0

#Function getTf will go in Data dir and go to desired file using given URL
#It will get access the file and return the words pre-calculated Tf value from the dictionary
def get_tf(URL,word):
    formatedURL = URL.replace("/","#")
    formatedURL += ".json"
    path = os.path.join("Data",formatedURL)
    if os.path.isfile(path):
        with open(path,"r") as file:
            data = json.load(file)
        if word not in data["Tf"]:
            return 0
        else:
            return data["Tf"][word]
    else:
        return 0

#Function getTfIdf will go in Data dir and go to desired file using given URL
#It will get access the file and return the given words pre-calculated tfidf value from the dictionary
def get_tf_idf(URL,word):
    formatedURL = URL.replace("/","#")
    formatedURL += ".json"
    path = os.path.join("Data",formatedURL)
    if os.path.isfile(path):
        with open(path,"r") as file:
            data = json.load(file)
            if word in data["tdIdf"]:
                return data["tdIdf"][word]
            else:
                return 0
    else:
        return 0
