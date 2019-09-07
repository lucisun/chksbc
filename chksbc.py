#!/usr/bin/python3
#tlucciano
from netaddr import *
import socket,struct
import math
import glob,os
import re
import sys
#import numpy as np
from datetime import datetime
from collections import defaultdict
#import matplotlib.pyplot as plt
##############################
# import modules for sbcchk
##############################
#import chk_sip_grey_list
from chk_sip_grey_list import check_acmelogs_demotions
from chk_sip_cpu import *
from chk_sipd_ses_st_ct import *


############################################################
# for menu selection - return an integer
############################################################
def enterInt():
    sum = 0;
    try:
        user_input = input("Enter choice as integer: ")
        n = int(user_input)
    except ValueError:
        print("Exiting! ValueError - that was no number: " + user_input) 
        sys.exit(1)
        # implicite remain in while loop
    except UnboundLocalError:
        print("UnboundLocalError - that was no number: " + user_input)
        sys.exit(1)

    return n

##########################################################
# clear the window
##########################################################
def cls():
   os.system(['clear','cls'][os.name == 'linux'])
 
###########################################
# MENU - get user choice
###########################################
def menu():
    cls()
    mydir = os.getcwd()
    myInt = -1;
    count = 0;
    print("\n")
    timenow = strftime("%Y%m%d%H%M%S", gmtime())
    yearnow = strftime("%Y",gmtime())
    
    while (myInt != count):
        print("1.Check acmelog for demotions (note that sbc must have had syslog-on-demote-to-deny and untrusted enabled")
        print("2. Check sipd logs for cpu")
        print("3. Check sipd CT ")
        print("4. Check sipd ST ")
        print("5. Check sipd SES ")
        print("0. Exit")
        myInt = enterInt();
        if (myInt == 1):
            check_acmelogs_demotions(mydir)
        elif (myInt == 2):
            check_sipd_logs_cpu(mydir,timenow,yearnow)
        elif (myInt == 3):
            check_sipd_logs_CT(mydir)
        elif (myInt == 4):
            check_sipd_logs_ST(mydir)
        elif (myInt == 5):
            check_sipd_logs_SES(mydir)
        elif (myInt == 0):
            sys.exit(1)
        else:
            sys.exit(1)

       

    sys.exit(1)

#############################################################
# MAIN main Main
############################################################
def main():
    cls()
    menu()

if __name__=='__main__':
    main()
