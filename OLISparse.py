from bs4 import BeautifulSoup
import urllib2
import csv

def newlinefile(input_file1):
	input1 = open(input_file1, 'r')
	input1 = input1.read()
	input1 = input1.split("\n")
	return input1

billslist2 = "billslist.txt"
billing = newlinefile(billslist2)

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
		billwriter = csv.writer(csvfile, delimiter=',')
		billwriter.writerow(billinfo)
	
