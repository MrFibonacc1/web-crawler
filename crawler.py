import time
from binascii import Incomplete
from distutils import dir_util
import fileinput
from genericpath import isdir
from importlib.resources import path
import os
import json
from operator import index
from re import L
from turtle import title
from typing import Counter
import webdev
import matmult
import math

global uniqueList
uniqueList = []
global totalStrings
totalStrings = {}
global check
check = False
global uniquePages
uniquePages = {}
global pageCounter
pageCounter = 0
global incomingLink
incomingLink = ""
global comingLink
comingLink = {}
global matrix
matrix = []
global fileIndex
fileIndex = 0

#Function thats take name/directory and data(A Dictionary) and stores data as json file in directory
def writeToJsonFile(filePath,data):
    with open(filePath,"w") as fp:
        json.dump(data, fp)

#Function that deletes a directory
#Given a directory name, it will first delete all files inside the directory before deleting it
def delete_directory(dir_name):
	if os.path.isdir(dir_name):
		files = os.listdir(dir_name)
		for file in files:
			os.remove(os.path.join(dir_name, file))
		os.rmdir(dir_name)

#This function will take a list of unique values and will calculate the Idf value
#It will add the TdIdf value for each word in each file
def addTdIdf(uniqueList):
    webFiles = os.listdir("Data")
    #Gets all Idf values which is required for TdIdf
    with open("WordsAppeared/IDF.json") as file:
        Idfs = json.load(file)
    #Will access every file in data(every link)
    for file in webFiles:
        file_path = os.path.join("Data", file)
        if os.path.isfile(file_path):
            with open(file_path,"r") as webData:
                data = json.load(webData)
            if "tdIdf" not in data:
                data["tdIdf"] = {}
            #Will calculate tdIdf value for each word in each data file
            for word in uniqueList:
                if word in data["WordCount"]:
                    idf = Idfs[word]
                    tf = data["Tf"][word]
                    calc1 = math.log(1+tf,2)
                    calc2 = calc1 * idf
                    data["tdIdf"][word] = calc2
            #Will update each json file with the tdIdf values
            filePath = os.path.join("Data",file)
            writeToJsonFile(filePath,data)
            
#Thie function will take a dictionary(count of each word) and list
#It will calculate the Idf value of each word and create a json file with all the values
def createIdfFile(dictionary,list):
    idfDictionary = {}
    pagesCrawled = dictionary["PagesCrawled"]
    for word in list:
        bottomCalc = 1 + dictionary[word]
        calc2 = pagesCrawled/bottomCalc
        finalCalc = math.log(calc2,2)
        if word not in idfDictionary:
            idfDictionary[word]= finalCalc
    writeToJsonFile("WordsAppeared/IDF.json",idfDictionary)

#This function takes number of pages crawled and search value
#Using these values will create a matrix an
def createMatrix(pages,directory):
    store = {}
    alpha = 0.1
    counter = 0
    fileNum = 0
    global matrix
    if os.path.isdir(directory):
            webFiles = os.listdir("Data")
            row = []
            #Initializes the matrix by multiplying N x N
            for i in range(pages):
                row = []
                for j in range(pages):
                    row.append(0)
                matrix.append(row)

            for file in webFiles:
                matrixIndex = 0
                filein = open("Data"+"/"+file, "r")
                data = json.load(filein)
                filein.close()
                #Loads data from every json file
                #Gets list of all outgoing links
                linkList = data["outgoingLinks"]
                fileIndex = data["index"]
                if file not in store:
                    store[file] = fileIndex

                #Goes through each link in outgoing links list
                for link in linkList:
                    link = link.replace("/","#")
                    filein = open("Data"+"/"+link+".json", "r")
                    data = json.load(filein)
                    oneIndex = data["index"]
                    #Adds value to matrix
                    matrix[fileIndex][oneIndex] = 1/len(linkList)
                    counter += 1
                    filein.close()
            length = len(matrix[0])
            #Uses matmult.py to use mult scalar and euclidean functions
            dividedMatrix = matmult.mult_scalar(matrix,1-alpha,"*")
            calc = alpha/length
            addMatrix = matmult.mult_scalar(dividedMatrix,calc,"+")
            #Checks if tOne is in locals
            if 'tOne' not in locals():
                tOne = []
                tOneRow = []
                for j in range(length):
                    value = 1/length
                    tOneRow.append(value)
                tOne.append(tOneRow)

            #Will repeat loop until the euclidean is smaller than 0.0001
            #Each loop will use the mult_matrix function and multiply value by the original matrix
            switch = True
            while switch:
                tPrev = tOne
                tOne = matmult.mult_matrix(tOne,addMatrix)
                next = matmult.euclidean_dist(tOne,tPrev)
                if next <= 0.0001:
                    switch = False
            #Will go through each file and add pageRanks value to each file
            for file in webFiles:
                givenIndex = store[file]
                store[file] = tOne[0][givenIndex]
                value = store[file]
                writeToJsonFile("PageRanks/" + file ,store[file])

#Main function that does the crawl
def crawlBranch(seed):
    global totalStrings
    global uniqueLink
    global dirPath
    global uniquePages
    global pageCounter
    global incomingLink
    global comingLink
    #Keeps the last part of the URL after the last slash
    URL_base = seed[0:seed.rindex("/")]
    errorFix = seed[seed.rindex("/"):len(seed)]
    global check
    if check == False:
        #Performs this once,deletes all directories and creates new ones
        uniquePages[errorFix] = 1
        pageCounter = 1
        if os.path.isdir("Data"):
            delete_directory("Data")
        if os.path.isdir("IncomingLinksFile"):
            delete_directory("IncomingLinksFile")
        if os.path.isdir("PageRanks"):
            delete_directory("PageRanks")
        if os.path.isdir("WordsAppeared"):
            delete_directory("WordsAppeared")
        recursionList = []
        os.makedirs("Data")
        os.makedirs("IncomingLinksFile")
        os.makedirs("PageRanks")
        os.makedirs("WordsAppeared")
        check = True

    #Gets content of web page
    web = webdev.read_url(seed)
    file_dictionary = {}
    fileTitle = seed.replace("/","#")

    #Gets title and saves into file dictionary
    title = web[web.index("<title>")+7:web.index("</title>")]
    if title not in file_dictionary:
        file_dictionary["Title"] = title

    #Generates unique index for each file
    global fileIndex
    if "index" not in file_dictionary:
        file_dictionary["index"] = fileIndex-1
    fileIndex += 1

    if "WordCount" not in file_dictionary:
        file_dictionary["WordCount"] = {}
    if "Tf" not in file_dictionary:
        file_dictionary["Tf"] = {}

    #Splits all </p> and deletes last index, because it will always be useless
    testCont = web.split("</p>")
    del testCont[len(testCont)-1]
    content = []

    #Go through the list and creates string based on last index of > which allows to get data
    #Gets data even when <p> has attributes inside and gets multiple p tags
    for z in range(len(testCont)):
        string = testCont[z]
        testCont[z] = testCont[z][testCont[z].rindex(">")+1:len(testCont[z])]
        list = testCont[z].split()
        content += list
    wordCounter = len(content)
    #Gets word count and unique list
    for word in content:
        if word not in file_dictionary["WordCount"]:
            if word not in uniqueList:
                uniqueList.append(word)
                totalStrings[word] = 0
            totalStrings[word] += 1
            file_dictionary["WordCount"][word] = 1
        else:
            file_dictionary["WordCount"][word] += 1
        wordFreq = file_dictionary["WordCount"][word]
        file_dictionary["Tf"][word]= wordFreq/wordCounter
    file_dictionary["WordCounter"] = wordCounter
    row = []

    #Gets all links
    webLinks = web[web.index("href="):len(web)-1]
    linksList = webLinks.split("href=")
    del linksList[0]
    if "outgoingLinks" not in file_dictionary:
        file_dictionary["outgoingLinks"] = []

    #Adds all links in web to list and then adds list to file's dictionary
    for item in linksList:
        link = item[item.index(".")+1:item.index(">")-1]
        if (URL_base + link) not in comingLink:
            comingLink[URL_base + link] = []
        if seed not in comingLink[URL_base + link]:
            comingLink[URL_base + link].append(seed)
        if link not in file_dictionary["outgoingLinks"]:
            file_dictionary["outgoingLinks"].append(URL_base+link)

        #Will go through all links and check if it already has been crawled
        #If it hasn't been crawled it will call itself as resursion
        #Will go through each webpage only once
        if link not in uniquePages:
            pageCounter += 1
            uniquePages[link] = 1
            incomingLink = seed
            crawlBranch(URL_base + link)

    #Adds dictionary to each json file for web page
    if os.path.isdir("Data"):
        file_path = os.path.join("Data", fileTitle +  ".json")
        if (os.path.isfile(file_path)) == False:
            writeToJsonFile(file_path,file_dictionary)
    return pageCounter

#Crawl function which has multiple funtions inside and executes them all when crawl is called
def crawl(URL):
    pagesCrawled = crawlBranch(URL)
    createMatrix(pagesCrawled,"PageRanks")
    totalStrings["PagesCrawled"] = pagesCrawled
    createIdfFile(totalStrings,uniqueList)
    addTdIdf(uniqueList)
    writeToJsonFile("IncomingLinksFile/incomingLinksList.json",comingLink)
    return pagesCrawled

