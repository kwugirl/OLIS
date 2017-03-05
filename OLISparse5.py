from bs4 import BeautifulSoup
import urllib2
import csv
import time


def new_line_no_spaces_file(input_file):
    return open(input_file, 'r').read().replace(" ", "").split("\n")


def get_soup(theURL):
    web_page = urllib2.urlopen(theURL)
    return BeautifulSoup(web_page, "lxml")


class Amendment:
    bill_number = ""
    amendment_number = ""
    amendmentURL = ""
    committee = ""
    post_date = ""
    modify_date = ""
    most_recent_change = ""


# import the tracked bills.
tracked_bills = 'trackedbills.txt'
tracked_bills_list = new_line_no_spaces_file(tracked_bills)
if "" in tracked_bills_list:
    tracked_bills_list.remove("")

# import amendment dataset.
r = csv.reader(open('amendment_dataset.csv'))
amendment_dataset = [l for l in r]

amendments = {}
for amendment in amendment_dataset:
    name = str(amendment[0]) + str(amendment[1])
    amendments[name] = Amendment()
    amendments[name].bill_number = amendment[0]
    amendments[name].amendment_number = amendment[1]
    amendments[name].committee = amendment[2]
    amendments[name].status = amendment[3]
    amendments[name].post_date = amendment[4]
    amendments[name].modify_date = amendment[5]
    amendments[name].most_recent_change = amendment[6]
    amendments[name].amendmentURL = amendment[7]

# bill_num = "HB2204"
# billHTML = open('sampleHTML.html','r')
# the_soup = BeautifulSoup(billHTML,"lxml")

# print soup.prettify()

for i in range(0, len(tracked_bills_list)):
    time.sleep(1)

    bill_num = tracked_bills_list[i]
    billURL = "https://olis.leg.state.or.us/liz/2017R1/Measures/ProposedAmendments/" + bill_num

    the_soup = get_soup(billURL)

    bill_tr = the_soup.find_all("tr")

    if len(bill_tr) > 0:

        for j in range(1, len(bill_tr)):

            bill_tr[j].i.decompose()
            bill_td = bill_tr[j].find_all("td")

            amendment_num = bill_td[0].find("a").string
            amendmentURL = bill_td[0].find("a").get('href')
            committee = bill_td[2].find("a").string
            amendment_status = bill_td[3].string
            post_date = bill_td[4].string
            test_name = str(bill_num) + str(amendment_num)
            x = 0

            if test_name not in amendments.keys():
                amendments[test_name] = Amendment()
                amendments[test_name].bill_number = bill_num
                amendments[test_name].amendment_number = amendment_num
                amendments[test_name].committee = '"' + committee + '"'
                amendments[test_name].status = amendment_status
                amendments[test_name].post_date = post_date
                amendments[test_name].modify_date = time.strftime("%m/%d/%Y")
                amendments[test_name].most_recent_change = "New Amendment"
                amendments[test_name].amendmentURL = amendmentURL
                x = 1
            else:
                if amendment_status != amendments[test_name].status:
                    amendments[test_name].modify_date = time.strftime("%m/%d/%Y")
                    amendments[test_name].status = amendment_status
                    amendments[test_name].most_recent_change = "Change in Status"
                    x = 1

            if x == 1:
                amendment_line = []

                amendment_line.append(amendments[test_name].bill_number)
                amendment_line.append(amendments[test_name].amendment_number)
                amendment_line.append(amendments[test_name].committee)
                amendment_line.append(amendments[test_name].status)
                amendment_line.append(amendments[test_name].post_date)
                amendment_line.append(amendments[test_name].modify_date)
                amendment_line.append(amendments[test_name].most_recent_change)
                amendment_line.append(amendments[test_name].amendmentURL)

                # write that list to the CSV file.
                with open('amendment_dataset.csv', 'a') as csvfile:
                    amendment_line_writer = csv.writer(csvfile, delimiter=',')
                    amendment_line_writer.writerow(amendment_line)
