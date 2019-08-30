#tlucciano
import glob,os
import re
import sys
from time import gmtime,strftime
import numpy as np
from datetime import datetime
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt

##################################################################
# check_sipd_logs
#  go thru each sipd log in cur dir and search for line with cpu
#  add cpu and date list and then graph
###################################################################
def check_sipd_logs_cpu(currDir,writeDir,currYear):
    gt2count=0
    print(currDir,writeDir)
    #outfile = open(fileToWriteTo,"w")	
    dates = []
    cpus = []
    for file in os.listdir(currDir):
        if file.startswith("log.sipd"):
            print("Checking file %s" % (file))
            currFile = open(file,'r')
            currFileLines = currFile.readlines()
            for line in currFileLines:
                searchObjCPU = re.search(r'\[SIP\] (0) CPU=.*cur=',line)
                #searchObjCPU = re.search(r'\[SIP\].*CPU=.*cur=',line)
                #searchObjCPU = re.search(r'\[SIP\]\s+.0.\s+cur=',line)

                if searchObjCPU:
                    cpuLine = line.split()
                    #print(cpuLine)
                    cpuStrList = cpuLine[6].split('=')
                    #print(cpuStrList)
                    currCPU = cpuStrList[1]
                    if len(currCPU) > 2:
                        gt2count=+1
                        continue
                    else:
                        #print(currCPU)
                        dateTime = cpuLine[0] + " " + cpuLine[1] + " " + cpuLine[2]
                        dateTimeSplit = dateTime.split(".")
                        dateString = str(dateTimeSplit[0])
                        #print("dateString: ",dateString)
                        dateStringII = currYear + " " + dateString
                        #print("dateStringII: ",dateStringII)
                        currDateTime = datetime.strptime(dateStringII,"%Y %b %d %H:%M:%S")
                        #print(currDateTime)
                        currCPU = int(currCPU)
                        #print(type(currCPU))
                        if(currCPU) > 1:
                            cpus.append(currCPU)
                            dates.append(currDateTime)
    zipped = zip(cpus,dates)
    #print(zipped)
    z2 = sorted(zipped, key = lambda x: x[1],reverse=False)
    newlist = list(z2)
    newcpu=[]
    newdate=[]
    for c,d in newlist:
        print(c,d)
        newcpu.append(c)
        newdate.append(d)

    fig,ax = plt.subplots()
    ax.plot(newdate,newcpu,color='red')
    plt.setp(ax.get_xticklabels(), rotation=45)
    ax.set(xlabel="DATE/TIME",ylabel="CPU",title="SIPD LOG CPU");
    plt.show()
    print(len(cpus))
    print(len(dates))
    print("gt2count: ", gt2count)
    #currFile.close()

def main():
    print("module only")
if __name__=='__main__':
    main()
