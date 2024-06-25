from genericpath import isdir
from h11 import Data
import math
import os
import json
import random

#Main search Function that will be given boolean(T/F) and phrase and return 10 highest
def search(phrase,boost):

    returningList = []
    #Makes phrase into lower case to match all values
    phrase = phrase.lower()
    #Split list into separate words
    list = phrase.split()
    total = len(list)
    #Loads all IDF values
    path = os.path.join("WordsAppeared","IDF.json")
    if os.path.isfile(path):
        with open(path,"r") as file:
            data = json.load(file)
    else:
        return 0
    queryVector = []
    uniqueDict = {}
    #Sorts all words based on alphabetical order(Will be the order used for vectors)
    list.sort()
    listOrder = []
    for word in list:
        #Will calculate the tfIdf of each word in given phrase
        if word not in uniqueDict:
            listOrder.append(word)
            uniqueDict[word] = 1
            count = list.count(word)
            tF = count/total
            calc1 = math.log(1+tF,2)
            if word not in data:
                idf = 0
            else:
                idf = data[word]
            calc2 = calc1 * idf
            queryVector.append(calc2)
    print(queryVector)
    if os.path.isdir("Data"):
        files = os.listdir("Data")
        #Will go through each file in Data and dir and create vector
        for file in files:
            print(file)
            unformattedUrl = file
            url = file[0:file.rindex(".")]
            url = url.replace("#","/")

            fileDict = {}
            fileVector = []
            path = os.path.join("Data",file)
            if os.path.isfile(path):
                with open(path,"r") as file:
                    data = json.load(file)
                
                for word in listOrder:
                    if word in data["tdIdf"]:
                        fileVector.append(data["tdIdf"][word])
                    else:
                        fileVector.append(0)

                numerator = 0
                leftDenomCalc = 0
                rightDenomCalc = 0
                for index in range(len(listOrder)):
                    #Calculations for cosine similarity
                    calc = fileVector[index]*queryVector[index]
                    calcLeft = queryVector[index] * queryVector[index]
                    calcRight = fileVector[index] * fileVector[index]
                    numerator += calc
                    leftDenomCalc += calcLeft
                    rightDenomCalc +=calcRight
                leftDenom = math.sqrt(leftDenomCalc)
                rightDenom = math.sqrt(rightDenomCalc)
                denominator = leftDenom*rightDenom
                if denominator == 0:
                    cosineSim = 0
                else:
                    cosineSim = numerator/denominator

                overallScore = 0
                #If boost is True, it will load pageRank value and multiply it
                if boost == True:
                    if os.path.isdir("PageRanks"):
                        pageRankPath = os.path.join("PageRanks",unformattedUrl)
                        if os.path.isfile(pageRankPath):
                            with open(pageRankPath, "r") as pageFile:
                                pageValue = json.load(pageFile)
                            overallScore = cosineSim*pageValue
                else:
                    overallScore = cosineSim
                print(overallScore)
                #Adds dictionary of all data will overallScore to list 
                fileDict["url"] = url
                fileDict["title"] = data["Title"]
                fileDict["score"] = overallScore
                returningList.append(fileDict)

    #Will sort list using my function
    sortedList = (sort(returningList))
    newReturnList = []
    #Will return first 10 highest links
    for k in range(10):
        newReturnList.append(sortedList[k])
    return newReturnList

#Function sort uses quickSort ideology
def sort(list):
    if len(list) < 2:
        return list
    low,same,high = [],[],[]
    #Gets random index from list and makes it our pillar value
    randomDict = list[random.randint(0,len(list)-1)]
    pillar = randomDict["score"]

    for item in list:
        if item["score"] < pillar:
            low.append(item)
        elif item["score"] == pillar:
            same.append(item)
        elif item["score"] > pillar:
            high.append(item)

    #Uses recursion and will return highest to lowesr
    return sort(high) + same + sort(low)
