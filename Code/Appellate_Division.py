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

        resultaffirm = []
        resultnonaffirm = []

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
                            resultaffirm.append([row[8] + "@" + fdates[ind], str(lastfiling)])
                        else:
                            resultnonaffirm.append([row[8] + "@" + fdates[ind], str(lastfiling)])

        res_affirm_dict = {}
        for item in resultaffirm:
            if res_affirm_dict.has_key(item[0]):
                res_affirm_dict[item[0]].append(item[1])
            else:
                res_affirm_dict[item[0]] = [item[1]]

        res_nonaffirm_dict = {}
        for item in resultnonaffirm:
            if res_nonaffirm_dict.has_key(item[0]):
                res_nonaffirm_dict[item[0]].append(item[1])
            else:
                res_nonaffirm_dict[item[0]] = [item[1]]

        res_middle_dict = {}
        for key, value in res_affirm_dict.iteritems():
            if res_nonaffirm_dict.has_key(key):
                res_middle_dict[key] = value + res_nonaffirm_dict[key]

        for key in res_middle_dict.iterkeys():
            del res_affirm_dict[key]
            del res_nonaffirm_dict[key]


        for key in res_affirm_dict.iterkeys():
            res_affirm_dict[key] = set(res_affirm_dict[key])

        for key in res_nonaffirm_dict.iterkeys():
            res_nonaffirm_dict[key] = set(res_nonaffirm_dict[key])

        for key in res_middle_dict.iterkeys():
            res_middle_dict[key] = set(res_middle_dict[key])



        with open("../Data/Appellate/Appellate_TDC.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(["Stock_Ticker", "Decision_Date", "Last_Filing_Days","Category"])

            for key, value in res_affirm_dict.iteritems():
                writer.writerow(key.split("@") + ["|".join(value), "A1"])

            for key, value in res_nonaffirm_dict.iteritems():
                writer.writerow(key.split("@") + ["|".join(value), "A2"])
            for key, value in res_middle_dict.iteritems():
                writer.writerow(key.split("@") + ["|".join(value), "A3"])

        print ["All appellate data : ", len(res_affirm_dict) + len(res_middle_dict) + len(res_nonaffirm_dict)]
        print ["Category A1 : Appellate with affirmed decision : ", len(res_affirm_dict)]
        print ["Category A2 : Appellate with not totally affirmed decision : ", len(res_nonaffirm_dict)]
        print ["Category A3 : Appellate with both decision : ", len(res_middle_dict)]



#appellate_division()

def main_appellate():
    all_appellate_data()
    appellate_division()




