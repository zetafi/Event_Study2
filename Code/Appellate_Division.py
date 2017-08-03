import csv
import sys
import re
import os.path

import datetime



# ALL APPELLATE DATA
## Extract items with a court abbreviation that is "CAFC" and has a terminated date.
## COL2 is "Court Abbreviation". COL26 is "Date Terminated
## File saved in data/Appellate/appellate_all.csv   Total : 1567 items
def all_appellate_data():
    # filings are too long, add this line to avoid error when reading the csv
    csv.field_size_limit(sys.maxsize)

    with open('../Data/step9_file.csv', 'rb') as csvfile:
        fulldata = csv.reader(csvfile)
        header = fulldata.next()

        count = 0

        # put the result file in to "data/Trial" directory
        if not os.path.isdir("../Data/Appellate"):
            os.mkdir("../Data/Appellate")

        with open("../Data/Appellate/appellate_all.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(header)

            for row in fulldata:
                if row[1] == "CAFC":
                    if row[25] != "":
                        count += 1
                        writer.writerow(row)

        print ["All appellate data : ", count]



# division
petitioner = ["PLAINTIFF", "APPELLANT", "PETITIONER", "PLAINTIFF-APPELLANT", "PLAINTIFF-APPELLANT, PLAINTIFF-APPELLANT", "APPELLANT, CROSS-APPELLANT"]
respondent= ["RESPONDENT", "THIRDPARTYDEFENDANT-APPELLEE, THIRDPARTYDEFENDANT", "DEFENDANT-APPELLEE", "DEFENDANT",
			"THIRDPARTYDEFENDANT", "DEFENDANT, DEFENDANT-APPELLEE", "APPELLEE", "DEFENDANT, SECONDARYENTITY"]

other= ["SANCTIONEDPARTY", "SECONDARYENTITY", "DEFENDANT-PETITIONER", "INTERVENOR-APPELLANT", "THIRDPARTYDEFENDANT-APPELLEE",
		"NONPARTY-APPELLANT", "AMICUSCURIAE", "AMICUS CURIAE, AMICUSCURIAE", "AMICUS CURIAE", "INTERVENOR", "MOVANT-APPELLEE"]

cross= ["COUNTERCLAIMDEFENDANT","COUNTERCLAIMDEFENDANT-APPELLEE", "PLAINTIFF/COUNTERCLAIMDEFENDANT-APPELLANT",
		"PLAINTIFF-APPELLEE, INTERESTEDPARTY-SECONDARYENTITY",
		"PLAINTIFF-APPELLEE, PLAINTIFF-APPELLEE","PLAINTIFF/COUNTERCLAIMDEFENDANT-APPELLEE",
		"APPELLEE, APPELLANT", "DEFENDANT/COUNTERCLAIMANT-APPELLEE", "DEFENDANT, DEFENDANT-APPELLEE, DEFENDANT-CROSS-APPELLANT",
		"DEFENDANT/CROSS APPELLANT, DEFENDANT-CROSS-APPELLANT", "DEFENDANT-APPELLANT, DEFENDANT-CROSS-APPELLANT",
		"DEFENDANT-APPELLANT, DEFENDANT-CROSS-APPELLANT", "CROSS-APPELLANT", "DEFENDANT/COUNTERCLAIMANT-APPELLANT",
		"DEFENDANT-APPELLANT, DEFENDANT-APPELLEE, DEFENDANT-CROSS-APPELLANT", "PLAINTIFF-APPELLANT, PLAINTIFF-APPELLEE",
		"APPELLEE, CROSS-APPELLANT", "COUNTERCLAIM DEFENDANT-APPELLEE", "DEFENDANT/COUNTERCLAIMANT-CROSS APPELLANT, DEFENDANT/COUNTERCLAIMANT-CROSS-APPELLANT",
		"DEFENDANT/COUNTERCLAIMANT-CROSS-APPELLANT", "PLAINTIFF-APPELLEE, PLAINTIFF/COUNTERCLAIMDEFENDANT-APPELLEE",
		"PLAINTIFF-APPELLEE, PLAINTIFF-CROSS-APPELLANT", "DEFENDANT/COUNTERCLAIMANT-CROSS APPELLANT",
		"PLAINTIFF, PLAINTIFF-APPELLEE, DEFENDANT-APPELLEE", "DEFENDANT-CROSS-APPELLANT", "PLAINTIFF-CROSS-APPELLANT",
		"COUNTERCLAIMDEFENDANT, COUNTERCLAIMDEFENDANT-APPELLEE", "PLAINTIFF-CROSS APPELLANT, PLAINTIFF-CROSS-APPELLANT",
		"DEFENDANT/CROSS APPELLANT, DEFENDANT/THIRDPARTYPLAINTIFF/COUNTERCLAIMANT-CROSS-APPELLANT",
		"DEFENDANT-APPELLANT", "DEFENDANT-APPELLEE, DEFENDANT-CROSS-APPELLANT", "DEFENDANT, DEFENDANT-APPELLANT, DEFENDANT-CROSS-APPELLANT",
		"PLAINTIFF-APPELLEE", "DEFENDANT, DEFENDANT-APPELLANT"]


#415 affirmed
#249 nonaffirmed
#10 in between
#674 total
def appellate_division():
    # filings are too long, add this line to avoid error when reading the csv
    csv.field_size_limit(sys.maxsize)

    with open('../Data/Appellate/appellate_all.csv', 'rb') as csvfile:
        apdata = csv.reader(csvfile)
        header = apdata.next()

        #resultaffirm = []
        #resultnonaffirm = []
        
        result_win = []
        result_lose = []
        result_other = []

        keyword = "The judgment or decision is: "

        for row in apdata:
            tdate = datetime.datetime.strptime(row[25], "%m/%d/%Y").date().strftime("%B %-d, %Y")

            fdates = re.split("[\'\"],\su[\'\"]", row[27])
            fdates[0] = fdates[0].replace("[u\'", "")
            fdates[-1] = fdates[-1].replace("\']", "")

            filings = re.split("[\'\"],\su[\'\"]", row[28])
            filings[0] = filings[0].replace("[u\'", "")
            filings[-1] = filings[-1].replace("\']", "")


            if "OPINION and JUDGMENT filed" in row[28]:
                for ind in range(len(filings)):

                    filings[ind] = filings[ind].replace("The j decision is:", "The judgment or decision is:")

                    # 1 exception for judgment or decision
                    # 1 exception for entry was made in error
                    cond = ("OPINION and JUDGMENT filed" in filings[ind]) \
                           and ("The judgment or decision is:" in filings[ind]) \
                           and not ("This entry was made in error" in filings[ind])

                    cond2 = fdates[ind] == tdate

                    if cond and cond2:
                        judgement = filings[ind]
                        findindex = judgement.find(keyword)
                        resbegin = findindex + len(keyword)
                        resend = judgement.find(".", resbegin, resbegin + 240)
                        judgresult = judgement[int(resbegin):int(resend)]

                        lastind = ind -1
                        lastfiling = (datetime.datetime.strptime(fdates[ind], "%B %d, %Y").date() - datetime.datetime.strptime(fdates[lastind], "%B %d, %Y").date()).days
                        while lastfiling == 0:
                            lastind -= 1
                            lastfiling = (datetime.datetime.strptime(fdates[ind], "%B %d, %Y").date() - datetime.datetime.strptime(fdates[lastind], "%B %d, %Y").date()).days

                        if judgresult == "Affirmed" or judgresult == "affirmed":
                            if row[5] in petitioner:
                                result_lose.append([row[8] + "@" + fdates[ind], str(lastfiling)])
                            elif row[5] in respondent:
                                result_win.append([row[8] + "@" + fdates[ind], str(lastfiling)])
                            else:
                                result_other.append([row[8] + "@" + fdates[ind], str(lastfiling)])
                        else:
                            if row[5] in petitioner:
                                result_win.append([row[8] + "@" + fdates[ind], str(lastfiling)])
                            elif row[5] in respondent:
                                result_lose.append([row[8] + "@" + fdates[ind], str(lastfiling)])
                            else:
                                result_other.append([row[8] + "@" + fdates[ind], str(lastfiling)])

        res_win_dict = {}
        for item in result_win:
            if res_win_dict.has_key(item[0]):
                res_win_dict[item[0]].append(item[1])
            else:
                res_win_dict[item[0]] = [item[1]]

        res_lose_dict = {}
        for item in result_lose:
            if res_lose_dict.has_key(item[0]):
                res_lose_dict[item[0]].append(item[1])
            else:
                res_lose_dict[item[0]] = [item[1]]

        res_middle_dict = {}
        for key, value in res_win_dict.iteritems():
            if res_lose_dict.has_key(key):
                res_middle_dict[key] = value + res_lose_dict[key]

        for key in res_middle_dict.iterkeys():
            del res_win_dict[key]
            del res_lose_dict[key]



        for item in result_other:
            if res_middle_dict.has_key(item[0]):
                res_middle_dict[item[0]].append(item[1])
            else:
                res_middle_dict[item[0]] = [item[1]]


        for key in res_win_dict.iterkeys():
            res_win_dict[key] = set(res_win_dict[key])

        for key in res_lose_dict.iterkeys():
            res_lose_dict[key] = set(res_lose_dict[key])

        for key in res_middle_dict.iterkeys():
            res_middle_dict[key] = set(res_middle_dict[key])



        with open("../Data/Appellate/Appellate_TDC.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(["Stock_Ticker", "Decision_Date", "Last_Filing_Days","Category"])

            for key, value in res_win_dict.iteritems():
                writer.writerow(key.split("@") + ["|".join(value), "A1"])

            for key, value in res_lose_dict.iteritems():
                writer.writerow(key.split("@") + ["|".join(value), "A2"])
            for key, value in res_middle_dict.iteritems():
                writer.writerow(key.split("@") + ["|".join(value), "A3"])

        print ["All appellate data : ", len(res_win_dict) + len(res_middle_dict) + len(res_lose_dict)]
        print ["Category A1 : Appellate with a win : ", len(res_win_dict)]
        print ["Category A2 : Appellate with a lose : ", len(res_lose_dict)]
        print ["Category A3 : Appellate with not clear : ", len(res_middle_dict)]



appellate_division()

def main_appellate():
    all_appellate_data()
    appellate_division()




