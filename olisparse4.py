from bs4 import BeautifulSoup
import urllib2
import csv
import time
from datetime import date
import datetime
from time import sleep

#Define some functions
def newlinefile(input_file1):
	input1 = open(input_file1, 'r')
	input1 = input1.read()
	input1 = input1.split("\n")
	return input1

def datemaker(dateinput):
	datemonth = dateinput.month	
	if len(str(datemonth)) == 1:
		datemonth = "0" + str(datemonth)
	dateday = dateinput.day
	if len(str(dateday)) == 1:
		dateday = "0" + str(dateday)
	dateyear = str(dateinput.year)
	datestring = datemonth + "%2F" + dateday + "%2F" + dateyear
	return datestring

def URLmaker(body,datestring):
	if body == "H":
		return "https://olis.leg.state.or.us/liz/2017R1/SessionDay/HouseFirstReadings?sessionDate=" + datestring + "%2000%3A00%3A00"
	if body == "S":
		return "https://olis.leg.state.or.us/liz/2017R1/SessionDay/SenateFirstReadings?sessionDate=" + datestring + "%2000%3A00%3A00"

def getsoup(theURL):
	web_page = urllib2.urlopen(theURL)
	return BeautifulSoup(web_page, "lxml")

def getbills(billslist,soup):
	newbills = soup.find_all("a")
	billslist.extend(newbills)
	return billslist

#Part 1: Set the date range. Probably should be modified to include UI piece.
startdate = date(2017, 02, 01)
enddate = date(2017, 02, 02)
daterange = int(str(enddate - startdate).split()[0]) + 1

#Part 2: Build a list of bills from the dates.
fullbillslist = []

for i in range(0,daterange):
	lookupdate = startdate + datetime.timedelta(days=i)
	stringeddate = datemaker(lookupdate)
	myURL = URLmaker("H",stringeddate)
	thesoup = getsoup(myURL)
	fullbillslist = getbills(fullbillslist,thesoup)
	time.sleep(1)
	
	myURL = URLmaker("S",stringeddate)
	thesoup = getsoup(myURL)
	fullbillslist = getbills(fullbillslist,thesoup)
	time.sleep(1)
	
billnumsnospacesfull = []

for i in range(0,len(fullbillslist)):
	nospace = fullbillslist[i].string
	nospace = nospace.replace(" ","")
	billnumsnospacesfull.append(nospace)

#Part 3: Grab the bill information itself.
for j in range(0,len(billnumsnospacesfull)):
	#put billnumber in its own variable.
	billnum = billnumsnospacesfull[j]
	
	#build the OLIS URL from the bill number, and run it through Beautiful Soup.
	billURL = "https://olis.leg.state.or.us/liz/2017R1/Measures/Overview/" + billnum
	thesoup = getsoup(billURL)

	#break apart soup into table rows.
	billtr = thesoup.find_all("tr")
	#row 1 has the bill sponsor. Check if there is one, and grab it.
	if billtr[1].find_all("td")[1].find("a") is not None:
		billsponsor = billtr[1].find_all("td")[1].find("a").string
	else: billsponsor = "None"
	
	#row 3 has the bill title.
	billtitle = billtr[3].find_all("td")[1].string
	
	#row 4 has the catchline and expanded summary. grab those both.
	billcatchline = billtr[4].find("span", attrs={'id':'catchline'}).string
	if billexpanded = billtr[4].find("div", attrs={'class':'collapse', 'id':'collapseMeasureSummary'}) is not None:
		billexpanded = billtr[4].find("div", attrs={'class':'collapse', 'id':'collapseMeasureSummary'}).string
	else: billexpanded = ""

	#clean up variables.
	billsponsor = billsponsor.lstrip()
	billtitle = billtitle.lstrip()
	billcatchline = billcatchline.lstrip()
	billexpanded = billexpanded.lstrip()
	billexpanded = billexpanded.rstrip()
	billsummary = '"' + billcatchline + " " + billexpanded + '"'
	
	#append everything into its own list.
	billinfo = []

	billinfo.append(str(billnum))
	billinfo.append('"' + str(billsponsor) + '"')
	billinfo.append('"' + str(billtitle) + '"')
	billinfo.append('"' + str(billsummary) + '"')
	billinfo.append(billURL)

	#add the list to a CSV file.
	with open('billsbillsbills2.csv', 'a') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',')
		spamwriter.writerow(billinfo)
	
	time.sleep(1)

#Problems to solve, still:
#1. Putting on the web as an app.
#2. Importing BeautifulSoup and other libraries into Heroku.
#3. Exporting the product from Heroku as a CSV.
#4. UI for date input.
