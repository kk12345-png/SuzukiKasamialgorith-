#!/usr/local/bin/python3

#This script is designed to run with python 3.x version

import queue, sys
from optparse import OptionParser

#Parse options

parser = OptionParser()
parser.add_option("-c", "--sitecount", dest="siteCount", help="Provide Number of Sites in the distributed system")
parser.add_option("-t", "--siteWithToken", dest="siteWithToken", help="Provide site id initially having token")
parser.add_option("--exec", dest="siteExec", action='store_true', help="Indicates that site having token is executing critical section")
parser.add_option("--no-exec", dest="siteExec", action='store_false', help="Indicates that site having token is not executing critical section")
(options, args) = parser.parse_args()

#Enforce Mandatory arguments
if not options.siteCount or not options.siteWithToken:
    print("Not enough mandatory arguments provided. Please check options using -h command")
    sys.exit(1)

siteCount = int(options.siteCount)
siteWithToken = int(options.siteWithToken)

#Class Token template.
#Token holds the token queue of requesting sites and token array.
# When site releases critical section, nth index of the token array (where n is the site id) is updated
class Token:
    def __init__(self):
        self.tokenQueue = queue.Queue()
        self.tokenArray = []

    def initializeTokenArray(self):
        for i in range(siteCount):
            self.tokenArray.append(0)


# Initialize token class and token array
token = Token()
token.initializeTokenArray()

#Site Class
class Site:
    def __init__(self, pid):
        self.pid = pid  # Process ID of Site (Starts with 0)
        self.seqArray = []  #Sequence Array of site maintaining sequence number of its own and other sites in realtime
        self.exec = False  # If True, Site is executing critical section.
        self.isreq = False  # If true, Site is requesting Critical Section
        self.hasToken = False  # If True, Site possesses the token

    #Initialize the Sequence Array when Site class is instantiated
    def initializeseqArray(self):
        for i in range(siteCount):
            self.seqArray.append(0)

    #Method to execute Request received from site requesting access to critical section
    def executeRequest(self, pid, seqNo):
        self.seqArray[pid] = max(self.seqArray[pid], seqNo)
        if self.hasToken:
            if self.exec == False and token.tokenArray[pid] + 1 == self.seqArray[pid]:
                self.hasToken = False
                global tokenHolder
                tokenHolder = pid
            elif self.exec == True and token.tokenArray[pid] + 1 == self.seqArray[pid]:
                token.tokenQueue.put(pid)

#Method called by site to request Critical section
def requestCS(site):
    seqNo = site.seqArray[site.pid] + 1
    if site.isreq:
        print("Site %s is already requesting \n" % (site.pid))
        return
    if site.exec:
        print("Site %s is already executing critical section \n"%(site.pid))
        return
    site.seqArray[site.pid] = seqNo
    site.isreq = True
    #Check if site has the token
    if tokenHolder == site.pid:
        site.isreq = False
        site.exec = True
        print("Site with id %s already has the token and it enters critical section \n"%(site.pid))
        return

    #Sending request to other sites
    if tokenHolder != site.pid:
        for i in range(siteCount):
            if i != site.pid:
                siteList[i].executeRequest(site.pid, seqNo)

    #Checking if site got the token
    if tokenHolder == site.pid:
        site.hasToken = True
        site.exec = True
        site.isreq = False
        print("Site with ID %s gets the token and it enters the critical section \n"%(site.pid))
    else:
        print("Site with ID %s is currently executing the critical section \n Site %s has placed its request \n"%(tokenHolder, site.pid))

#Method called by site to release Critical section
def releaseCS(site):
    if not site.exec:
        print("Site with id %s is currently not executing Critical section \n"%(site.pid))
        return
    token.tokenArray[site.pid] = site.seqArray[site.pid]
    site.exec = False
    print("Site with id %s releases the critical section \n"%(site.pid))
    #Checking if deffered requests are there by checking token queue and passing the token if queue is non empty
    if not token.tokenQueue.empty():
        siteId = token.tokenQueue.get()
        site.hasToken = False
        global tokenHolder
        tokenHolder = siteId
        siteList[siteId].hasToken = True
        siteList[siteId].exec = True
        siteList[siteId].isreq = False
        print("Site with id %s gets the token and enters the critical section \n"%(siteList[siteId].pid))
        return

    print("Site with id %s still has the token \n" % (site.pid))
    return

#Method to get current state of system
def getStateOfSystem(siteList):
    k = 0
    msg = 'TOKEN STATE ==>\n'
    msg += '  TOKEN HOLDER: %s \n'%(tokenHolder)
    msg += '  TOKEN QUEUE: '
    if token.tokenQueue.empty():
        msg += 'EMPTY'
        j = 0
    else:
        j = token.tokenQueue.qsize()
    while k < j:
        i = token.tokenQueue.queue[0]
        token.tokenQueue.get()
        token.tokenQueue.put(i)
        msg += '%s '%(i)
        k += 1
    msg += '\n'
    msg += 'TOKEN SEQ NO ARRAY: '
    for i in range(siteCount):
        msg += '%s '%(token.tokenArray[i])
    msg += '\n'
    msg += 'SITES SEQ NO ARRAY ==> \n'
    for i in range(len(siteList)):
        msg += '  S%s : '%(i)
        for j in range(len(siteList)):
            msg += '%s'%(siteList[i].seqArray[j])
        msg += '\n'
    return msg


#Main method
if __name__ == "__main__":
    str = ''
    siteList = []
    #Initialize all sites
    for i in range(siteCount):
        site = Site(pid=i)
        site.initializeseqArray()
        siteList.append(site)

    #Assign token to site id provided in input
    siteList[int(siteWithToken)].hasToken = True
    if options.siteExec:
        siteList[int(siteWithToken)].exec = True
    tokenHolder = int(siteWithToken)

    initialState = getStateOfSystem(siteList)
    print("Initial state: \n")
    print(initialState)
    print('\n')

    while str != 'OVER':
        str = input("Mention type of Message (REQ/REL/OVER): ")
        if str == 'REQ':
            pid = input("Site ID: ")
            pid = int(pid)
            print("EVENT : %s  %s"%(str, pid))
            requestCS(siteList[pid])
            systemState = getStateOfSystem(siteList)
            print(systemState)
            print('\n')
        elif str == 'REL':
            pid = input("Site ID: ")
            pid = int(pid)
            print("EVENT : %s  %s" % (str, pid))
            releaseCS(siteList[pid])
            systemState = getStateOfSystem(siteList)
            print(systemState)
            print('\n')








