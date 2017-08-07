import csv
import sys
import re
import os.path

# ALL TRIAL DATA
## Extract items with a non null remedy value. COL37 is "remedies_amount".
## All items that has a remedy value are trial court cases
## File saved in data/Trial/all_complete_trial.csv   Total : 1061 items
def all_complete_trial_data():
    # filings are too long, add this line to avoid error when reading the csv
    csv.field_size_limit(sys.maxsize)

    with open('../Data/step9_file.csv', 'rb') as csvfile:
        fulldata = csv.reader(csvfile)
        header = fulldata.next()

        count = 0

        # put the result file in to "data/Trial" directory
        if not os.path.isdir("../Data/Trial"):
            os.mkdir("../Data/Trial")

        with open("../Data/Trial/all_complete_trial.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(header)

            for row in fulldata:
                if row[36] != "":
                    count += 1
                    writer.writerow(row)

            print ["All full trial data : ", count]



def exception_cases():
    ## jury judge for all trial case
    url_full = "https://www.docketnavigator.com/detail/summary/case/"
    ids_full = ["13906", "4738", "4116", "29907", "31069", "33239"]
    urls_full = []
    for id in ids_full:
        urls_full.append(url_full + id)

    exceptjury_full = []
    exceptbench_full = []

    ## jury case 4738
    exceptjury_full += [["HPQ@October 5, 2010","1-05-cv-00064"], ["INTC@October 5, 2010","1-05-cv-00064"], ["IBM@October 5, 2010","1-05-cv-00064"]]

    ## jury case 4116
    exceptjury_full += [["BXS@March 26, 2010","2-06-cv-00072"], ["BBT@March 26, 2010","2-06-cv-00072"], ["CFG@March 26, 2010","2-06-cv-00072"],
                        ["CMA@March 26, 2010","2-06-cv-00072"], ["CFR@March 26, 2010","2-06-cv-00072"], ["FDC@March 26, 2010","2-06-cv-00072"],
                        ["KEY@March 26, 2010","2-06-cv-00072"], ["MTB@March 26, 2010","2-06-cv-00072"], ["STI@March 26, 2010","2-06-cv-00072"],
                        ["USB@March 26, 2010","2-06-cv-00072"], ["WFC@March 26, 2010","2-06-cv-00072"], ["ZION@March 26, 2010","2-06-cv-00072"]]

    ## jury case 29907
    exceptjury_full += [["AAPL@November 21, 2013","5-11-cv-01846"], ["INTC@November 21, 2013","5-11-cv-01846"], ["IBM@November 21, 2013","5-11-cv-01846"],
                        ["PHG@November 21, 2013","5-11-cv-01846"],
                        ["MSFT@November 21, 2013","5-11-cv-01846"], ["NOK@November 21, 2013","5-11-cv-01846"]]

    ## jury case 33239
    exceptjury_full += [["AAPL@May 2, 2014","5-12-cv-00630"], ["AAPL@May 5, 2014","5-12-cv-00630"], ["INTC@May 2, 2014","5-12-cv-00630"], ["INTC@May 5, 2014","5-12-cv-00630"],
                        ["IBM@May 2, 2014","5-12-cv-00630"], ["IBM@May 5, 2014","5-12-cv-00630"], ["MSFT@May 2, 2014","5-12-cv-00630"], ["MSFT@May 5, 2014","5-12-cv-00630"]]

    ## bench case 13906
    exceptbench_full += [["MU@May 8, 2013","5-00-cv-20905"], ["MU@March 21, 2012","5-00-cv-20905"], ["MU@January 11, 2012","5-00-cv-20905"], ["MU@March 8, 2010","5-00-cv-20905"],
                         ["MU@March 10, 2009","5-00-cv-20905"]]
    exceptbench_full += [["NVDA@May 8, 2013","5-00-cv-20905"], ["NVDA@March 21, 2012","5-00-cv-20905"], ["NVDA@January 11, 2012","5-00-cv-20905"], ["NVDA@March 8, 2010","5-00-cv-20905"],
                         ["NVDA@March 10, 2009","5-00-cv-20905"]]
    exceptbench_full += [["RMBS@May 8, 2013","5-00-cv-20905"], ["RMBS@March 21, 2012","5-00-cv-20905"], ["RMBS@January 11, 2012","5-00-cv-20905"], ["RMBS@March 8, 2010","5-00-cv-20905"],
                         ["RMBS@March 10, 2009","5-00-cv-20905"]]

    ## bench case 4738
    exceptbench_full += [["HPQ@November 7, 2013","1-05-cv-00064"], ["INTC@November 7, 2013","1-05-cv-00064"], ["IBM@November 7, 2013","1-05-cv-00064"]]

    ## bench case 4116
    exceptbench_full += [["BXS@August 2, 2011","2-06-cv-00072"], ["BXS@August 3, 2011","2-06-cv-00072"], ["BXS@September 27, 2010","2-06-cv-00072"], ["BXS@September 11, 2009","2-06-cv-00072"]]
    exceptbench_full += [["BAC@August 2, 2011","2-06-cv-00072"], ["BAC@August 3, 2011","2-06-cv-00072"], ["BAC@September 27, 2010","2-06-cv-00072"], ["BAC@March 26, 2010","2-06-cv-00072"],
                         ["BAC@September 11, 2009","2-06-cv-00072"]]
    exceptbench_full += [["BBT@August 2, 2011","2-06-cv-00072"], ["BXS@August 3, 2011","2-06-cv-00072"], ["BBT@September 27, 2010","2-06-cv-00072"], ["BBT@September 11, 2009","2-06-cv-00072"]]
    exceptbench_full += [["CFG@August 2, 2011","2-06-cv-00072"], ["CFG@August 3, 2011","2-06-cv-00072"], ["CFG@September 27, 2010","2-06-cv-00072"], ["CFG@September 11, 2009","2-06-cv-00072"]]
    exceptbench_full += [["CMA@August 2, 2011","2-06-cv-00072"], ["CMA@August 3, 2011","2-06-cv-00072"], ["CMA@September 27, 2010","2-06-cv-00072"], ["BXS@September 11, 2009","2-06-cv-00072"]]
    exceptbench_full += [["CFR@August 2, 2011","2-06-cv-00072"], ["CFR@August 3, 2011","2-06-cv-00072"], ["CFR@September 27, 2010","2-06-cv-00072"], ["CFR@September 11, 2009","2-06-cv-00072"]]
    exceptbench_full += [["FDC@August 2, 2011","2-06-cv-00072"], ["FDC@August 3, 2011","2-06-cv-00072"], ["FDC@September 27, 2010","2-06-cv-00072"], ["FDC@September 11, 2009","2-06-cv-00072"]]
    exceptbench_full += [["KEY@August 2, 2011","2-06-cv-00072"], ["KEY@August 3, 2011","2-06-cv-00072"], ["KEY@September 27, 2010","2-06-cv-00072"], ["KEY@September 11, 2009","2-06-cv-00072"]]
    exceptbench_full += [["MTB@August 2, 2011","2-06-cv-00072"], ["MTB@August 3, 2011","2-06-cv-00072"], ["MTB@September 27, 2010","2-06-cv-00072"], ["MTB@September 11, 2009","2-06-cv-00072"]]
    exceptbench_full += [["STI@August 2, 2011","2-06-cv-00072"], ["STI@August 3, 2011","2-06-cv-00072"], ["STI@September 27, 2010","2-06-cv-00072"], ["STI@September 11, 2009","2-06-cv-00072"]]
    exceptbench_full += [["USB@August 2, 2011","2-06-cv-00072"], ["USB@August 3, 2011","2-06-cv-00072"], ["USB@September 27, 2010","2-06-cv-00072"], ["USB@September 11, 2009","2-06-cv-00072"]]
    exceptbench_full += [["WFC@August 2, 2011","2-06-cv-00072"], ["WFC@August 3, 2011","2-06-cv-00072"], ["WFC@September 27, 2010","2-06-cv-00072"], ["WFC@September 11, 2009","2-06-cv-00072"]]
    exceptbench_full += [["ZION@August 2, 2011","2-06-cv-00072"], ["ZION@August 3, 2011","2-06-cv-00072"], ["ZION@September 27, 2010","2-06-cv-00072"],
                         ["ZION@September 11, 2009","2-06-cv-00072"]]

    ## bench case 29907
    exceptbench_full += [["AAPL@September 18, 2015","5-11-cv-01846"], ["AAPL@September 19, 2014","5-11-cv-01846"], ["AAPL@June 20, 2014","5-11-cv-01846"],
                         ["AAPL@March 6, 2014","5-11-cv-01846"]]
    exceptbench_full += [["AAPL@March 1, 2013","5-11-cv-01846"], ["AAPL@November 7, 2012","5-11-cv-01846"], ["AAPL@August 24, 2012","5-11-cv-01846"], ["AAPL@June 26, 2012","5-11-cv-01846"]]
    exceptbench_full += [["INTC@September 18, 2015","5-11-cv-01846"], ["INTC@September 19, 2014","5-11-cv-01846"], ["INTC@June 20, 2014","5-11-cv-01846"],
                         ["INTC@March 6, 2014","5-11-cv-01846"]]
    exceptbench_full += [["INTC@March 1, 2013","5-11-cv-01846"], ["INTC@November 7, 2012","5-11-cv-01846"], ["INTC@August 24, 2012","5-11-cv-01846"], ["INTC@June 26, 2012","5-11-cv-01846"]]
    exceptbench_full += [["IBM@September 18, 2015","5-11-cv-01846"], ["IBM@September 19, 2014","5-11-cv-01846"], ["IBM@June 20, 2014", "IBM@March 6, 2014","5-11-cv-01846"]]
    exceptbench_full += [["IBM@March 1, 2013","5-11-cv-01846"], ["IBM@November 7, 2012","5-11-cv-01846"], ["IBM@August 24, 2012", "IBM@June 26, 2012","5-11-cv-01846"]]
    exceptbench_full += [["PHGL@September 18, 2015","5-11-cv-01846"], ["PHG@September 19, 2014","5-11-cv-01846"], ["PHG@June 20, 2014", "PHG@March 6, 2014","5-11-cv-01846"]]
    exceptbench_full += [["PHG@March 1, 2013","5-11-cv-01846"], ["PHG@November 7, 2012","5-11-cv-01846"], ["PHG@August 24, 2012", "PHG@June 26, 2012","5-11-cv-01846"]]
    exceptbench_full += [["MSFT@September 18, 2015","5-11-cv-01846"], ["MSFT@September 19, 2014","5-11-cv-01846"], ["MSFT@June 20, 2014","5-11-cv-01846"],
                         ["MSFT@March 6, 2014","5-11-cv-01846"]]
    exceptbench_full += [["MSFT@March 1, 2013","5-11-cv-01846"], ["MSFT@November 7, 2012","5-11-cv-01846"], ["MSFT@August 24, 2012","5-11-cv-01846"], ["MSFT@June 26, 2012","5-11-cv-01846"]]
    exceptbench_full += [["NOK@September 18, 2015","5-11-cv-01846"], ["NOK@September 19, 2014","5-11-cv-01846"], ["NOK@June 20, 2014","5-11-cv-01846"], ["NOK@March 6, 2014","5-11-cv-01846"]]
    exceptbench_full += [["NOK@March 1, 2013","5-11-cv-01846"], ["NOK@November 7, 2012","5-11-cv-01846"], ["NOK@August 24, 2012","5-11-cv-01846"], ["NOK@June 26, 2012","5-11-cv-01846"]]

    ## bench case 31069
    exceptbench_full += [["AMPH@May 9, 2016","1-11-cv-11681"], ["AMPH@October 28, 2011","1-11-cv-11681"], ["AMPH@October 21, 2011","1-11-cv-11681"], ["AMPH@October 7, 2011","1-11-cv-11681"]]
    exceptbench_full += [["MNTA@May 9, 2016","1-11-cv-11681"], ["MNTA@October 28, 2011","1-11-cv-11681"], ["MNTA@October 21, 2011","1-11-cv-11681"], ["MNTA@October 7, 2011","1-11-cv-11681"]]

    ## bench case 33239
    exceptbench_full += [["AAPL@June 23, 2017","5-12-cv-00630"], ["AAPL@January 18, 2016","5-12-cv-00630"], ["AAPL@August 20, 2015","5-12-cv-00630"],
                         ["AAPL@November 25, 2014","5-12-cv-00630"]]
    exceptbench_full += [["INTC@June 23, 2017","5-12-cv-00630"], ["INTC@January 18, 2016","5-12-cv-00630"], ["INTC@August 20, 2015","5-12-cv-00630"],
                         ["INTC@November 25, 2014","5-12-cv-00630"]]
    exceptbench_full += [["IBM@June 23, 2017","5-12-cv-00630"], ["IBM@January 18, 2016","5-12-cv-00630"], ["IBM@August 20, 2015","5-12-cv-00630"], ["IBM@November 25, 2014","5-12-cv-00630"]]
    exceptbench_full += [["MSFT@June 23, 2017","5-12-cv-00630"], ["MSFT@January 18, 2016","5-12-cv-00630"], ["MSFT@August 20, 2015","5-12-cv-00630"],
                         ["MSFT@November 25, 2014","5-12-cv-00630"]]
    ######## exception cases

    url_v = "https://www.docketnavigator.com/detail/summary/case/"
    ids_v = ["13906", "29907", "31069", "33239"]
    urls_v = []
    for id in ids_v:
        urls_v.append(url_v + id)

    exceptjury_v = []
    exceptbench_v = []

    ## jury case 29907
    exceptjury_v += [["AAPL@November 21, 2013","5-11-cv-01846"], ["NOK@November 21, 2013","5-11-cv-01846"]]

    ## jury case 33239
    exceptjury_v += [["AAPL@May 2, 2014","5-12-cv-00630"], ["AAPL@May 5, 2014","5-12-cv-00630"]]

    ### bench case 13906
    exceptbench_v += [["RMBS@May 8, 2013","5-00-cv-20905"], ["RMBS@March 21, 2012","5-00-cv-20905"], ["RMBS@January 11, 2012","5-00-cv-20905"], ["RMBS@March 8, 2010","5-00-cv-20905"],
                      ["RMBS@March 10, 2009","5-00-cv-20905"]]

    ### bench case 29907
    exceptbench_v += [["AAPL@September 18, 2015","5-11-cv-01846"], ["AAPL@September 19, 2014","5-11-cv-01846"], ["AAPL@June 20, 2014","5-11-cv-01846"],
                      ["AAPL@March 6, 2014","5-11-cv-01846"]]
    exceptbench_v += [["AAPL@March 1, 2013","5-11-cv-01846"], ["AAPL@November 7, 2012","5-11-cv-01846"], ["AAPL@August 24, 2012","5-11-cv-01846"], ["AAPL@June 26, 2012","5-11-cv-01846"]]
    exceptbench_v += [["NOK@September 18, 2015","5-11-cv-01846"], ["NOK@September 19, 2014","5-11-cv-01846"], ["NOK@June 20, 2014","5-11-cv-01846"], ["NOK@March 6, 2014","5-11-cv-01846"]]
    exceptbench_v += [["NOK@March 1, 2013","5-11-cv-01846"], ["NOK@November 7, 2012","5-11-cv-01846"], ["NOK@August 24, 2012","5-11-cv-01846"], ["NOK@June 26, 2012","5-11-cv-01846"]]

    ## bench case 31069
    exceptbench_v += [["AMPH@May 9, 2016","1-11-cv-11681"], ["AMPH@October 28, 2011","1-11-cv-11681"], ["AMPH@October 21, 2011","1-11-cv-11681"], ["AMPH@October 7, 2011","1-11-cv-11681"]]
    exceptbench_v += [["MNTA@May 9, 2016","1-11-cv-11681"], ["MNTA@October 28, 2011","1-11-cv-11681"], ["MNTA@October 21, 2011","1-11-cv-11681"], ["MNTA@October 7, 2011","1-11-cv-11681"]]

    ## bench case 33239
    exceptbench_v += [["AAPL@June 23, 2017","5-12-cv-00630"], ["AAPL@January 18, 2016","5-12-cv-00630"], ["AAPL@August 20, 2015","5-12-cv-00630"], ["AAPL@November 25, 2014","5-12-cv-00630"]]
    ######## exception

    return [[urls_full,exceptjury_full,exceptbench_full],[urls_v,exceptjury_v,exceptjury_v]]




def trial_division():
    csv.field_size_limit(sys.maxsize)
    with open('../Data/Trial/all_complete_trial.csv', 'rb') as csvfile:
        fulltrdata = csv.reader(csvfile)
        header = fulltrdata.next()

        juryresult = []
        benchresult = []
        amount_100thd = []

        valid_jury = []
        valid_bench = []
        res_vjb = []

        valid_benfit = []
        valid_against = []
        res_vba = []
        valid_amount_100thd = []

        ## Exceptions
        exceptions = exception_cases()
        urls_full = exceptions[0][0]
        urls_v = exceptions[1][0]
        juryresult += exceptions[0][1]
        valid_jury += exceptions[1][1]
        benchresult += exceptions[0][2]
        valid_bench += exceptions[1][2]

        for row in fulltrdata:
            if row[26] in urls_full and row[26] in urls_v:
                continue

            fdates = re.split("[\'\"],\su[\'\"]", row[27])
            fdates[0] = fdates[0].replace("[u\'", "")
            fdates[-1] = fdates[-1].replace("\']", "")

            filings = re.split("[\'\"],\su[\'\"]", row[28])
            filings[0] = filings[0].replace("[u\'", "")
            filings[-1] = filings[-1].replace("\']", "")

            rdates = row[37].split("\', u\'")
            rdates[0] = rdates[0].replace("[u\'", "")
            rdates[-1] = rdates[-1].replace("\']", "")

            amounts = row[36].split("\', u\'")
            amounts[0] = amounts[0].replace("[u\'", "")
            amounts[-1] = amounts[-1].replace("\']", "")

            for ind in range(len(amounts)):
                if amounts[ind] != "N/A":
                    amounts[ind] = amounts[ind].replace("$", "")
                    amounts[ind] = amounts[ind].replace(",", "")
                    amounts[ind] = int(float(amounts[ind]))
                else:
                    amounts[ind] = 0

            ## For all trial data, jury&bench + >100thd division
            for ind in range(len(rdates)):
                if amounts[ind] > 100000:
                    amount_100thd.append([row[8] + "@" + rdates[ind], row[2]])

            if row[26] not in urls_full:
                for remi in range(len(rdates)):
                    evtfilings = ""
                    for f_ind in range(len(filings)):
                        if fdates[f_ind] == rdates[remi]:
                            evtfilings += filings[f_ind] + " | "

                    cond = ("JURY VERDICT" in evtfilings) or ("JURY'S VERDICT" in evtfilings) \
                           or ("JUDGMENT BY JURY" in evtfilings) or ("JURY Verdict" in evtfilings) \
                           or ("Jury polled" in evtfilings) or ("JURY SPECIAL VERDICT" in evtfilings) \
                           or ("VERDICT OF THE JURY" in evtfilings) or ("(JURY) VERDICT" in evtfilings) \
                           or ("Jury Trial Proceedings" in evtfilings) or ("Jury Verdict -" in evtfilings) \
                           or ("Jury returns verdict" in evtfilings) or ("Jury's Special Verdict" in evtfilings) \
                           or ("Jury Notes" in evtfilings) or ("Judgment on the Jury's Verdict" in evtfilings)

                    if cond:
                        juryresult.append([row[8] + "@" + rdates[remi], row[2]])
                    else:
                        benchresult.append([row[8] + "@" + rdates[remi], row[2]])


            ## Benefit Valid case division
            benes = re.split("[\'\"],\su[\'\"]", row[34])
            ## remove the extra char from the first one and the last one
            benes[0] = benes[0].replace("[u\'", "")
            benes[-1] = benes[-1].replace("\']", "")

            nonbenes = re.split("[\'\"],\su[\'\"]", row[33])
            nonbenes[0] = nonbenes[0].replace("[u\'", "")
            nonbenes[-1] = nonbenes[-1].replace("\']", "")

            for i in range(0, len(rdates)):
                if benes[i] == row[9] or nonbenes[i] == row[9]:
                    if benes[i] == row[9]:
                        valid_benfit.append([row[8] + "@" + rdates[i], row[2]])
                    if nonbenes[i] == row[9]:
                        valid_against.append([row[8] + "@" + rdates[i], row[2]])

                    if amounts[i] > 100000:
                        valid_amount_100thd.append([row[8] + "@" + rdates[i], row[2]])

                    evtfilings = ""
                    for f_ind in range(len(filings)):
                        if fdates[f_ind] == rdates[i]:
                            evtfilings += filings[f_ind] + " | "

                    cond2 = ("JURY VERDICT" in evtfilings) or ("JURY'S VERDICT" in evtfilings) \
                        or ("JUDGMENT BY JURY" in evtfilings) or ("JURY Verdict" in evtfilings) \
                        or ("Jury polled" in evtfilings) or ("JURY SPECIAL VERDICT" in evtfilings) \
                        or ("VERDICT OF THE JURY" in evtfilings) or ("(JURY) VERDICT" in evtfilings) \
                        or ("Jury Trial Proceedings" in evtfilings) or ("Jury Verdict -" in evtfilings) \
                        or ("Jury returns verdict" in evtfilings) or ("Jury's Special Verdict" in evtfilings) \
                        or ("Jury Note" in evtfilings) or ("Judgment on the Jury's Verdict" in evtfilings)

                    if cond2 and row[26] not in urls_v:
                        valid_jury.append([row[8] + "@" + rdates[i], row[2]])
                    elif row[26] not in urls_v:
                        valid_bench.append([row[8] + "@" + rdates[i], row[2]])








        res_tjury_dict = {}
        for item in juryresult:
            if res_tjury_dict.has_key(item[0]):
                res_tjury_dict[item[0]].append(item[1])
            else:
                res_tjury_dict[item[0]] = [item[1]]

        res_tbench_dict = {}
        for item in benchresult:
            if res_tbench_dict.has_key(item[0]):
                res_tbench_dict[item[0]].append(item[1])
            else:
                res_tbench_dict[item[0]] = [item[1]]

        res_tjb_dict = {}
        for key, value in res_tjury_dict.iteritems():
            if res_tbench_dict.has_key(key):
                res_tjb_dict[key] = value + res_tbench_dict[key]

        for key in res_tjb_dict.iterkeys():
            del res_tjury_dict[key]
            del res_tbench_dict[key]

        res_t100thd_dict = {}
        for item in amount_100thd:
            if res_t100thd_dict.has_key(item[0]):
                res_t100thd_dict[item[0]].append(item[1])
            else:
                res_t100thd_dict[item[0]] = [item[1]]




        res_tvj_dict = {}
        for item in valid_jury:
            if res_tvj_dict.has_key(item[0]):
                res_tvj_dict[item[0]].append(item[1])
            else:
                res_tvj_dict[item[0]] = [item[1]]

        res_tvb_dict = {}
        for item in valid_bench:
            if res_tvb_dict.has_key(item[0]):
                res_tvb_dict[item[0]].append(item[1])
            else:
                res_tvb_dict[item[0]] = [item[1]]

        res_tvjb_dict = {}
        for key, value in res_tvj_dict.iteritems():
            if res_tvb_dict.has_key(key):
                res_tvjb_dict[key] = value + res_tvb_dict[key]

        for key in res_tvjb_dict.iterkeys():
            del res_tvj_dict[key]
            del res_tvb_dict[key]

        res_tv100thd_dict = {}
        for item in valid_amount_100thd:
            if res_tv100thd_dict.has_key(item[0]):
                res_tv100thd_dict[item[0]].append(item[1])
            else:
                res_tv100thd_dict[item[0]] = [item[1]]




        res_tvbf_dict = {}
        for item in valid_benfit:
            if res_tvbf_dict.has_key(item[0]):
                res_tvbf_dict[item[0]].append(item[1])
            else:
                res_tvbf_dict[item[0]] = [item[1]]

        res_tva_dict = {}
        for item in valid_against:
            if res_tva_dict.has_key(item[0]):
                res_tva_dict[item[0]].append(item[1])
            else:
                res_tva_dict[item[0]] = [item[1]]

        res_tvbfa_dict = {}
        for key, value in res_tvbf_dict.iteritems():
            if res_tva_dict.has_key(key):
                res_tvbfa_dict[key] = value + res_tva_dict[key]


        for key in res_tvbfa_dict.iterkeys():
            del res_tvbf_dict[key]
            del res_tva_dict[key]



        for key in res_tjury_dict.iterkeys():
            res_tjury_dict[key] = set(res_tjury_dict[key])

        for key in res_tbench_dict.iterkeys():
            res_tbench_dict[key] = set(res_tbench_dict[key])

        for key in res_tjb_dict.iterkeys():
            res_tjb_dict[key] = set(res_tjb_dict[key])

        for key in res_t100thd_dict.iterkeys():
            res_t100thd_dict[key] = set(res_t100thd_dict[key])

        for key in res_tvj_dict.iterkeys():
            res_tvj_dict[key] = set(res_tvj_dict[key])

        for key in res_tvb_dict.iterkeys():
            res_tvb_dict[key] = set(res_tvb_dict[key])
        for key in res_tvjb_dict.iterkeys():
            res_tvjb_dict[key] = set(res_tvjb_dict[key])

        for key in res_tv100thd_dict.iterkeys():
            res_tv100thd_dict[key] = set(res_tv100thd_dict[key])

        for key in res_tva_dict.iterkeys():
            res_tva_dict[key] = set(res_tva_dict[key])
        for key in res_tvbf_dict.iterkeys():
            res_tvbf_dict[key] = set(res_tvbf_dict[key])




        with open("../Data/Trial/Trial_TDC.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(["Stock_Ticker", "Decision_Date", "Category", "Case_Number"])

            for key, value in res_tjury_dict.iteritems():
                cate = "TJ"
                if key in res_t100thd_dict.iterkeys():
                    cate += "|T100"
                if key in res_tvbf_dict.iterkeys():
                    cate += "|TVBF"
                if key in res_tva_dict.iterkeys():
                    cate += "|TVA"
                if key in res_tvbfa_dict.iterkeys():
                    cate += "|TVBFA"
                if key in res_tvj_dict.iterkeys():
                    cate += "|TVJ"
                if key in res_tvb_dict.iterkeys():
                    cate += "|TVB"
                if key in res_tvjb_dict.iterkeys():
                    cate += "|TVJB"
                if key in res_tv100thd_dict.iterkeys():
                    cate += "|TV100"
                writer.writerow(key.split("@") + [cate,"|".join(value)])

            for key, value in res_tbench_dict.iteritems():
                cate = "TB"
                if key in res_t100thd_dict.iterkeys():
                    cate += "|T100"
                if key in res_tvbf_dict.iterkeys():
                    cate += "|TVBF"
                if key in res_tva_dict.iterkeys():
                    cate += "|TVA"
                if key in res_tvbfa_dict.iterkeys():
                    cate += "|TVBFA"
                if key in res_tvj_dict.iterkeys():
                    cate += "|TVJ"
                if key in res_tvb_dict.iterkeys():
                    cate += "|TVB"
                if key in res_tvjb_dict.iterkeys():
                    cate += "|TVJB"
                if key in res_tv100thd_dict.iterkeys():
                    cate += "|TV100"
                writer.writerow(key.split("@") + [cate, "|".join(value)])

            for key, value in res_tjb_dict.iteritems():
                cate = "TJB"
                if key in res_t100thd_dict.iterkeys():
                    cate += "|T100"
                if key in res_tvbf_dict.iterkeys():
                    cate += "|TVBF"
                if key in res_tva_dict.iterkeys():
                    cate += "|TVA"
                if key in res_tvbfa_dict.iterkeys():
                    cate += "|TVBFA"
                if key in res_tvj_dict.iterkeys():
                    cate += "|TVJ"
                if key in res_tvb_dict.iterkeys():
                    cate += "|TVB"
                if key in res_tvjb_dict.iterkeys():
                    cate += "|TVJB"
                if key in res_tv100thd_dict.iterkeys():
                    cate += "|TV100"
                writer.writerow(key.split("@") + [cate, "|".join(value)])

        print ["All appellate data : ", len(res_tjury_dict.keys()) + len(res_tbench_dict.keys()) + len(res_tjb_dict.keys())]
        print ["Category TJ : Trial with jury decision : ", len(res_tjury_dict.keys())]
        print ["Category TB : Trial with bench decision : ", len(res_tbench_dict.keys())]
        print ["Category TJB : Trial with both jury&bench decision : ", len(res_tjb_dict.keys())]
        print ["Category T100 : Trial with remedy amount larger than $100,000 : ", len(res_t100thd_dict.keys())]
        print ["Category TVJ : Trial benefit valided with jury decision : ", len(res_tvj_dict.keys())]
        print ["Category TVB : Trial benefit valided with bench decision : ", len(res_tvb_dict.keys())]
        print ["Category TVJB : Trial benefit valided with with both jury&bench decision : ", len(res_tvjb_dict.keys())]
        print ["Category TVBF : Trial benefit valided and is beneficiary party in the remedy : ", len(res_tvbf_dict.keys())]
        print ["Category TVA : Trial benefit valided and is against party in the remedy : ", len(res_tva_dict.keys())]
        print ["Category TVBFA : Trial benefit valided and is both beneficiary&agianst party in the remedy : ", len(res_tvbfa_dict.keys())]
        print ["Category TV100 : Trial benefit valided with remedy amount larger than $100,000 : ", len(res_tv100thd_dict.keys())]


trial_division()