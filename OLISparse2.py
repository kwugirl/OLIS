from bs4 import BeautifulSoup
import urllib2
import csv
import time

#part 1: look at all the bills that dropped on a certain date.
#put numbers into list.
web_string = "https://olis.leg.state.or.us/liz/2017R1/Measures/PublishedOn/2017-01-08"

web_page = urllib2.urlopen(web_string)
soup = BeautifulSoup(web_page,"lxml")

sum1 = soup.find_all("a")

billing = []

for i in range(0,len(sum1)-1):
	tester = sum1[i].string
	if tester is not None:
		tester = tester.replace(" ","")
		if tester[len(tester) - 1:len(tester)].isdigit() == True:
			billing.append(tester)

i = 0
j = 0

#part 2: look at bill pages in OLIS. grab short summary and long summary.
#put bill number, short summary, and long summary into billsbillsbills.csv.
for i in range(0,len(billing)-1):
	web_string = "https://olis.leg.state.or.us/liz/2017R1/Measures/Overview/" + billing[i]
	web_page = urllib2.urlopen(web_string)
	soup = BeautifulSoup(web_page, "lxml")

	shortsum = soup.find("span", attrs={'id':'catchline'})
	part1 = shortsum.string

	longsum = soup.find("div", attrs={'class':'collapse', 'id':'collapseMeasureSummary'})
	part2 = longsum.string
	
	billinfo = []
	
	billinfo.append(billing[i])
	billinfo.append(part1)
	billinfo.append(part2)
	
	with open('billsbillsbills.csv', 'a') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',')
		spamwriter.writerow(billinfo)


#print soup.prettify()

#for i in range(0,20):

	#sum1 = soup.find_next("article", attrs={'class':'results-group'})

	#if sum1 != None:
		#print sum1.string

#print sum1.find("td", attrs={'class':'results-percentage'})

#shortsum = soup.find("span", attrs={'id':'catchline'})
#part1 = shortsum.string

#longsum = soup.find("div", attrs={'class':'collapse', 'id':'collapseMeasureSummary'})
#part2 = longsum.string

#billinfo = []
#billinfo.append(billing[i])
#billinfo.append(part1)
#billinfo.append(part2)

#with open('billsbillsbills.csv', 'a') as csvfile:
#billwriter = csv.writer(csvfile, delimiter=',')
#billwriter.writerow(billinfo)
