from bs4 import BeautifulSoup
import urllib2
import csv
import time
from datetime import date
import datetime
from time import sleep


def newlinefile(input_file1):
    input1 = open(input_file1, 'r')
    input1 = input1.read()
    input1 = input1.split("\n")
    return input1


def newlinenospacesfile(input_file1):
    input1 = open(input_file1, 'r')
    input1 = input1.read()
    input1 = input1.replace(" ", "")
    input1 = input1.split("\n")
    return input1


def datemaker(dateinput):
    datemonth = str(dateinput.month)
    if len(str(datemonth)) == 1:
        datemonth = "0" + str(datemonth)
    dateday = str(dateinput.day)
    if len(str(dateday)) == 1:
        dateday = "0" + str(dateday)
    dateyear = str(dateinput.year)
    datestring = datemonth + "%2F" + dateday + "%2F" + dateyear
    return datestring


def getsoup(theURL):
    web_page = urllib2.urlopen(theURL)
    return BeautifulSoup(web_page, "lxml")


def getbills(billslist, soup):
    newbills = soup.find_all("a")
    billslist.extend(newbills)
    return billslist


class Amendment:
    billnumber = ""
    amendmentnumber = ""
    amendmentURL = ""
    committee = ""
    postdate = ""
    modifydate = ""
    mostrecentchange = ""


#import the tracked bills.
tbills = 'trackedbills.txt'

tbillslist = newlinenospacesfile(tbills)

if "" in tbillslist:
    tbillslist.remove("")

#import amendment dataset.
r = csv.reader(open('amendmentdataset.csv'))
amendmentdataset = [l for l in r]

#create blank list for amendmentnames
amendmentlist = []
amendment_dict = {}

#generate the list of amendments and the dictionary.
for i in range(1, len(amendmentdataset)):
    amendmentname = str(amendmentdataset[i][0]) + str(amendmentdataset[i][1])
    amendmentlist.append(amendmentname)
    amendment_dict[amendmentname] = Amendment()
    amendment_dict[amendmentname].billnumber = amendmentdataset[i][0]
    amendment_dict[amendmentname].amendmentnumber = amendmentdataset[i][1]
    amendment_dict[amendmentname].committee = amendmentdataset[i][2]
    amendment_dict[amendmentname].status = amendmentdataset[i][3]
    amendment_dict[amendmentname].postdate = amendmentdataset[i][4]
    amendment_dict[amendmentname].modifydate = amendmentdataset[i][5]
    amendment_dict[amendmentname].mostrecentchange = amendmentdataset[i][6]
    amendment_dict[amendmentname].amendmentURL = amendmentdataset[i][7]

#billnum = "HB2204"
#billHTML = open('sampleHTML.html','r')
#thesoup = BeautifulSoup(billHTML,"lxml")

#print soup.prettify()

for i in range(0, len(tbillslist)):
    time.sleep(1)

    billnum = tbillslist[i]
    billURL = "https://olis.leg.state.or.us/liz/2017R1/Measures/ProposedAmendments/" + billnum

    thesoup = getsoup(billURL)

    billtr = thesoup.find_all("tr")

    if len(billtr) > 0:

        for j in range(1, len(billtr)):

            billtr[j].i.decompose()
            billtd = billtr[j].find_all("td")

            amendmentnum = billtd[0].find("a").string
            amendmentURL = billtd[0].find("a").get('href')
            committee = billtd[2].find("a").string
            amendmentstatus = billtd[3].string
            postdate = billtd[4].string
            testname = str(billnum) + str(amendmentnum)
            x = 0

            if testname not in amendmentlist:
                amendment_dict[testname] = Amendment()
                amendment_dict[testname].billnumber = billnum
                amendment_dict[testname].amendmentnumber = amendmentnum
                amendment_dict[testname].committee = '"' + committee + '"'
                amendment_dict[testname].status = amendmentstatus
                amendment_dict[testname].postdate = postdate
                amendment_dict[testname].modifydate = time.strftime("%m/%d/%Y")
                amendment_dict[testname].mostrecentchange = "New Amendment"
                amendment_dict[testname].amendmentURL = amendmentURL
                x = 1
            else:
                if amendmentstatus != amendment_dict[testname].status:
                    amendment_dict[testname].modifydate = time.strftime("%m/%d/%Y")
                    amendment_dict[testname].status = amendmentstatus
                    amendment_dict[testname].mostrecentchange = "Change in Status"
                    x = 1

            if x == 1:
                amendmentline = []

                amendmentline.append(amendment_dict[testname].billnumber)
                amendmentline.append(amendment_dict[testname].amendmentnumber)
                amendmentline.append(amendment_dict[testname].committee)
                amendmentline.append(amendment_dict[testname].status)
                amendmentline.append(amendment_dict[testname].postdate)
                amendmentline.append(amendment_dict[testname].modifydate)
                amendmentline.append(amendment_dict[testname].mostrecentchange)
                amendmentline.append(amendment_dict[testname].amendmentURL)

                #write that list to the CSV file.
                with open('amendmentdataset.csv', 'a') as csvfile:
                    amendmentlinewriter = csv.writer(csvfile, delimiter=',')
                    amendmentlinewriter.writerow(amendmentline)
