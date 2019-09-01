#!/usr/bin/python3
import os
import re

##########################################################
# Function: check_acmelogs_demotions
# check all acmelog log files for demotions
# create a dictionary of counts
# Note that the below 2 paramaters in media-manager must be 
# set to enabled for data to be present 
# syslog-on-demote-to-deny
# syslog-on-demote-to-untrusted
# (can also enable as traps)
# NOTE that demotion count (any dictionary count output is
# divided by 2 as in acmelog, the relevant message is 
# output 2 times
############################################################

def check_acmelogs_demotions(currDir):
    demAcmeGreyDict = {}
    demAcmeBlackDict = {}
    exceedErrorDict = {}
    exceedMessageDict = {}
    highCountDict = {}
    permitCount = 0
    demDenyCount = 0
    demotionsCount = 0
    demCount = 0
    print(f"currDir: {currDir}")
    acmeloglist = list()
    for file in os.listdir(currDir):
        if file.startswith("acmelog"):
            acmeloglist.append(file)
    for file in acmeloglist:
        print("FILE: %s" % (file))
        currFile = open(file,'r')
        currFileLines = currFile.readlines()
        for line in currFileLines:
            line = line.rstrip()
            #print(line)
            if "Demoted" in line:
                #print(line)
                if "Grey-List" in line:
                    ipDemPattern = re.findall(r'[0-9]+(?:\.[0-9]+){3}.*]', line)
                    #print(ipDemPattern)
                    #print(line)
                    if ipDemPattern[0] in demAcmeGreyDict:
                        demAcmeGreyDict[ipDemPattern[0]] += 1
                    else:
                        demAcmeGreyDict[ipDemPattern[0]] = 1
                if "Black-List" in line:
                    #print(line) 
                    ipDemPattern = re.findall(r'[0-9]+(?:\.[0-9]+){3}.*]', line)
                    #print(ipDemPattern)
                    #print(line)
                    if ipDemPattern[0] in demAcmeBlackDict:
                        demAcmeBlackDict[ipDemPattern[0]] += 1
                    else:
                        demAcmeBlackDict[ipDemPattern[0]] = 1
                if "exceeded error threshold" in line:
                    ipExceedPattern = re.findall(r'[0-9]+(?:\.[0-9]+){3}.*]', line )
                    if ipExceedPattern[0] in exceedErrorDict:
                        exceedErrorDict[ipExceedPattern[0]] += 1
                    else:
                        exceedErrorDict[ipExceedPattern[0]] = 1
                if "exceeded message threshold" in line:
                    ipExceedMsgPattern = re.findall(r'[0-9]+(?:\.[0-9]+){3}.*]', line )
                    if ipExceedMsgPattern[0] in exceedMessageDict:
                        exceedMessageDict[ipExceedMsgPattern[0]] += 1
                    else:
                        exceedMessageDict[ipExceedMsgPattern[0]] = 1

    #print(demAcmeBlackDict)
    print("BLACK LIST")
    for k,v in enumerate(demAcmeBlackDict):
        print(k,v)
    print("EXCEED ERROR")
    for k,v in enumerate(exceedErrorDict):
        print(k,v)
    print("EXCEED MSG THRES")
    for k,v in enumerate(exceedMessageDict):
        print(k,v)

    #print(demAcmeGreyDict)
    print("GREY LIST")
    #for k,v in enumerate(demAcmeGreyDict):
    #    print(k,v)
    for key,val in sorted(demAcmeGreyDict.items()):
        #print("%s: %s " % (key, demAcmeGreyDict[key])),
        print("%s  -> %s " % (key,(val/2)))
        #print(demAcmeGreyDict[key])
        demotionsCount = demotionsCount + int(demAcmeGreyDict[key])
        if int(demAcmeGreyDict[key]) > 20:
            highCountDict[key]=demAcmeGreyDict[key]
            print("\t\t%s: %s " % (key,demAcmeGreyDict[key])),
        demCount = demCount + 1
        if "DENY" in key:
            print(key,demAcmeGreyDict[key])
            demDenyCount = demDenyCount + 1
        if "PERMIT" in key:
            permitCount += 1
    if demDenyCount > 0 or permitCount > 0:
        print("Number of ip:port addresses listed  %d " % (demCount))
        print("demotionsCount: %s " % (demotionsCount)) 
        #print("Number of ip addresses listed with Deny: %d " % (demDenyCount))
        #print("Number of ip addresses listed with PERMIT: %d " % (permitCount))
        print("endpoint will first move from trusted to untrusted state which is known as 'demotion to grey' list and when it goes from untrusted to deny state it will be logged as 'demotion to black list'")
        print("The message 'Too many nones' occur whenever there is a demotion event")
        print("The nones means that there was no behavior based reason for the demotion")
        print("If a endpoint is promoted this lasts just for 10 minutes, starting with the last SIP message seen");
        print("If within 10 minutes there are no new messages, the endpoint falls back grey list (is demoted)");
        #for k,v in sorted(highCountDict.values.iteritems()):
        print("\n SORTED: acmelog High Counts of Demote to Grey List - to untrusted")
        for k in sorted(highCountDict, key=highCountDict.get, reverse=True):
            #print(k,v)
            print(k,(highCountDict[k]/2))
    else:
            print("Nothing Recorded")

