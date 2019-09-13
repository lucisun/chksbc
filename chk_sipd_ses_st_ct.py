#!/usr/bin/python3
#tlucciano
import glob,os
import re
import sys
import numpy as np
#from datetime import datetime
from datetime import *
from collections import defaultdict
import matplotlib.pyplot as plt

monthDict = {'Jan': 1, 'Feb':2 , 'Mar':3, 'Apr': 4, 'May':5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec':12 }
monthDictII = { "Jan": "01", "Feb": "02","Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12" }
today = date.today()
year = today.year

##############################################################
# function check_sipd_logs_SES
# check the sipd logs for count of sessions
##############################################################
def check_sipd_logs_SES(currDir):
    sesLines=0
    sesFile = open('SESTRANS.txt','w')
    siplogstring=""
    siploglist=list()
    sesDict = defaultdict(int)
    dateTimeList = []
    sesCountList = []
    newDTList = []
    newSESList = []
    for file in os.listdir(currDir):
        if file.startswith("log.sipd"):
            #print "Checking file %s" % (file)
            currFile = open(file,'r')
            currFileLines = currFile.readlines()
            for line in currFileLines:
                searchObjSES = re.search(r'\[SIP].*SES\[',line)
                if searchObjSES:
                    SESLine=line.split()
                    #print SESLine
                    #stMonth = SESLine[0];
                    stMonth = int(monthDict[SESLine[0]])
                    stDay = int(SESLine[1])
                    timeStr = SESLine[2].split(":")
                    #print(timeStr)
                    stHour = int(timeStr[0])
                    stMin = int(timeStr[1])
                    stSec = timeStr[2].split(".")
                    stSec = int(stSec[0])
                    #if len(stDay) == 1:
                    #    stDay = "0" + stDay
                    dateHour = stMonth + stDay + stHour + stMin
                    datetimeStamp = datetime(year,stMonth,stDay,stHour,stMin,stSec)
                    getSEScount = SESLine[5].split("=")
                    #print(getSEScount)
                    if "/" in getSEScount[1]:
                        sesTransSplit = getSEScount[1].split("/")
                        sesTrans = sesTransSplit[0]
                        sesTrans = int(sesTrans)
                        #print(dateHour),
                        #print(servTrans)
                        sesDict[datetimeStamp] += sesTrans
                        dateTimeList.append(datetimeStamp)
                        sesCountList.append(sesTrans)
                    sesLines+=1

    if sesLines > 0:
        for key in sorted(sesDict.keys()):
            print("SESSIONS AT : %s: %s" % (key,sesDict[key]))
            sesFile.write("Sessions at : %s: %s" % (key,sesDict[key]))
            sesFile.write("\n")
    else:
        print("NO LINES WITH SES FOUND!")
    #    if int(sesDict[key]) > 60:
    #        sesPerMin = int(sesDict[key]) / 60
    #        print("\t sess per min: %d " % (sesPerMin))

    for d,c in (sorted(zip(dateTimeList,sesCountList))):
            #print(d,c)
            newDTList.append(d)
            newSESList.append(c)
    plt.plot(newDTList,newSESList)
    plt.title("Session", fontsize=14)
    plt.xlabel("Time",fontsize=12)
    plt.ylabel("Count",fontsize=12)
    plt.tick_params(axis='both',labelsize=6)
    plt.show()
    sesFile.close()
    print("\nData written to file SESTRANS.txt")


def check_sipd_logs_ST(currDir):
    #monthDict = { "Jan": "01", "Feb": "02","Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12" }
    stFile = open('STRANS.txt','w')
    siplogstring=""
    siploglist=list()
    stDict = defaultdict(int)
    dateTimeList = []
    servCountList = []
    newDTList = []
    newSTList = []
    for file in os.listdir(currDir):
        if file.startswith("log.sipd"):
            #print "Checking file %s" % (file)
            currFile = open(file,'r')
            currFileLines = currFile.readlines()
            for line in currFileLines:
                searchObjST = re.search(r'\[SIP].*ST\[',line)
                if searchObjST:
                    STLine=line.split()
                    #print STLine
                    stMonth = int(monthDict[STLine[0]])
                    stDay = int(STLine[1])
                    timeStr = STLine[2].split(":")
                    #print(timeStr)
                    stHour = int(timeStr[0])
                    stMin = int(timeStr[1])
                    stSec = timeStr[2].split(".")
                    stSec = int(stSec[0])
                    #if len(stDay) == 1:
                    #    stDay = "0" + stDay
                    dateHour = stMonth + stDay + stHour + stMin
                    datetimeStamp = datetime(year,stMonth,stDay,stHour,stMin,stSec)
                    stTime = stHour + stMin + stSec
                    #print(dateHour),
                    getSTcount = STLine[5].split("=")
                    #print(getSTcount)
                    if "/" in getSTcount[1]:
                        servTransSplit = getSTcount[1].split("/")
                        servTrans = servTransSplit[0]
                        #print(servTrans)
                        servTrans = int(servTrans)
                        #print(servTrans)
                        stDict[datetimeStamp] += servTrans
                        #dateTime = STLine[0] + "-" + STLine[1] + " " + STLine[2]
                        #print(dateTime)
                        dateTimeList.append(datetimeStamp)
                        servCountList.append(servTrans)

    for key in sorted(stDict.keys()):
        print("Serv Trans at : %s: %s" % (key,stDict[key]))
        stFile.write("Serv Trans at: %s: %s" % (key,stDict[key]))
        stFile.write("\n")
    #    if int(stDict[key]) > 60:
    #        stPerMin = int(stDict[key]) / 60
    #        print("\t client trans per min: %d " % (stPerMin))

    for d,c in (sorted(zip(dateTimeList,servCountList))):
            #print(d,c)
            newDTList.append(d)
            newSTList.append(c)
    plt.plot(newDTList,newSTList)
    plt.title("Server Transactions at the time", fontsize=14)
    plt.xlabel("Time",fontsize=12)
    plt.ylabel("Count",fontsize=12)
    plt.tick_params(axis='both',labelsize=6)
    plt.show()

    stFile.close()
    print("\nData written to file STRANS.txt")

###########################################################
# function check_sipd_logs_CT
# check the sipd logs for Client transaction count
# at the time
# use current year - year not logged in log, doesn't matter
###########################################################
def check_sipd_logs_CT(currDir):
    today = date.today()
    year = today.year
    ctFile = open('CTRANS.txt','w')
    siplogstring=""
    siploglist=list()
    ctDict = defaultdict(int)
    dateTimeList = []
    clientCountList = []
    newDTList = []
    newCTList = []
    for file in os.listdir(currDir):
        if file.startswith("log.sipd"):
            #print "Checking file %s" % (file)
            currFile = open(file,'r')
            currFileLines = currFile.readlines()
            for line in currFileLines:
                searchObjCT = re.search(r'\[SIP].*CT\[',line)
                if searchObjCT:
                    CTLine=line.split()
                    #print CTLine
                    stMonth = int(monthDict[CTLine[0]])
                    stDay = int(CTLine[1])
                    timeStr = CTLine[2].split(":")
                    #print("timestr: ", timeStr)
                    stHour = int(timeStr[0])
                    stMin = int(timeStr[1])
                    stSec = timeStr[2].split(".")
                    stSec = int(stSec[0])
                    #if len(stDay) == 1:
                    #    stDay = "0" + stDay
                    dateHour = stMonth + stDay + stHour + stMin
                    datetimeStamp = datetime(year,stMonth,stDay,stHour,stMin,stSec)
                    print("datetimeStamp: ")
                    print(datetimeStamp)
                    #print("dateHour: ", dateHour)
                    getCTcount = CTLine[5].split("=")
                    print("getCTcount: ", getCTcount)
                    #print("getCTcount: ",getCTcount)
                    #print("len:",len(getCTcount))
                    #print(getCTcount)
                    if len(getCTcount) > 1:
                        if "/" in getCTcount[1]:
                            clientTransSplit = getCTcount[1].split("/")
                            clientTrans = clientTransSplit[0]
                            clientTrans = int(clientTrans)
                            #print(dateHour),
                            print(clientTrans)
                            ctDict[datetimeStamp] += clientTrans
                            dateTimeList.append(datetimeStamp)
                            clientCountList.append(clientTrans)
                    else:
                        continue

    for key in sorted(ctDict.keys()):
        print("Client trans at MMDDHR: %s: %s" % (key,ctDict[key]))
        ctFile.write("Client Trans at: %s: %s" % (key,ctDict[key]))
        ctFile.write("\n")
    #print("length of dateTimeList: ", len(dateTimeList))
    #print("length of clientCountList: ", len(clientCountList))
    for d,c in (sorted(zip(dateTimeList,clientCountList))):
            #print(d,c)
            newDTList.append(d)
            newCTList.append(c)
    plt.plot(newDTList,newCTList)
    plt.title("Client Transactions at the time", fontsize=14)
    plt.xlabel("Time",fontsize=12)
    plt.ylabel("Count",fontsize=12)
    plt.tick_params(axis='both',labelsize=6)
    plt.show()

    
    #    if int(ctDict[key]) > 60:
    #        ctPerMin = int(ctDict[key]) / 60
    #        print("\t client trans per min: %d " % (ctPerMin))

    ctFile.close()
    print("\nData written to file CTRANS.txt")


def main():
    print("")
    currDir = os.getcwd()
    check_sipd_logs_SES(currDir)
    check_sipd_logs_ST(currDir)
    check_sipd_logs_CT(currDir)

if __name__=='__main__':
    main()
