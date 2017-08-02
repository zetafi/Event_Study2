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
    exceptjury_full += ["HPQ@October 5, 2010", "INTC@October 5, 2010", "IBM@October 5, 2010"]

    ## jury case 4116
    exceptjury_full += ["BXS@March 26, 2010", "BBT@March 26, 2010", "CFG@March 26, 2010",
                        "CMA@March 26, 2010", "CFR@March 26, 2010", "FDC@March 26, 2010",
                        "KEY@March 26, 2010", "MTB@March 26, 2010", "STI@March 26, 2010",
                        "USB@March 26, 2010", "WFC@March 26, 2010", "ZION@March 26, 2010"]

    ## jury case 29907
    exceptjury_full += ["AAPL@November 21, 2013", "INTC@November 21, 2013", "IBM@November 21, 2013",
                        "PHG@November 21, 2013",
                        "MSFT@November 21, 2013", "NOK@November 21, 2013"]

    ## jury case 33239
    exceptjury_full += ["AAPL@May 2, 2014", "AAPL@May 5, 2014", "INTC@May 2, 2014", "INTC@May 5, 2014",
                        "IBM@May 2, 2014", "IBM@May 5, 2014", "MSFT@May 2, 2014", "MSFT@May 5, 2014"]

    ## bench case 13906
    exceptbench_full += ["MU@May 8, 2013", "MU@March 21, 2012", "MU@January 11, 2012", "MU@March 8, 2010",
                         "MU@March 10, 2009"]
    exceptbench_full += ["NVDA@May 8, 2013", "NVDA@March 21, 2012", "NVDA@January 11, 2012", "NVDA@March 8, 2010",
                         "NVDA@March 10, 2009"]
    exceptbench_full += ["RMBS@May 8, 2013", "RMBS@March 21, 2012", "RMBS@January 11, 2012", "RMBS@March 8, 2010",
                         "RMBS@March 10, 2009"]

    ## bench case 4738
    exceptbench_full += ["HPQ@November 7, 2013", "INTC@November 7, 2013", "IBM@November 7, 2013"]

    ## bench case 4116
    exceptbench_full += ["BXS@August 2, 2011", "BXS@August 3, 2011", "BXS@September 27, 2010", "BXS@September 11, 2009"]
    exceptbench_full += ["BAC@August 2, 2011", "BAC@August 3, 2011", "BAC@September 27, 2010", "BAC@March 26, 2010",
                         "BAC@September 11, 2009"]
    exceptbench_full += ["BBT@August 2, 2011", "BXS@August 3, 2011", "BBT@September 27, 2010", "BBT@September 11, 2009"]
    exceptbench_full += ["CFG@August 2, 2011", "CFG@August 3, 2011", "CFG@September 27, 2010", "CFG@September 11, 2009"]
    exceptbench_full += ["CMA@August 2, 2011", "CMA@August 3, 2011", "CMA@September 27, 2010", "BXS@September 11, 2009"]
    exceptbench_full += ["CFR@August 2, 2011", "CFR@August 3, 2011", "CFR@September 27, 2010", "CFR@September 11, 2009"]
    exceptbench_full += ["FDC@August 2, 2011", "FDC@August 3, 2011", "FDC@September 27, 2010", "FDC@September 11, 2009"]
    exceptbench_full += ["KEY@August 2, 2011", "KEY@August 3, 2011", "KEY@September 27, 2010", "KEY@September 11, 2009"]
    exceptbench_full += ["MTB@August 2, 2011", "MTB@August 3, 2011", "MTB@September 27, 2010", "MTB@September 11, 2009"]
    exceptbench_full += ["STI@August 2, 2011", "STI@August 3, 2011", "STI@September 27, 2010", "STI@September 11, 2009"]
    exceptbench_full += ["USB@August 2, 2011", "USB@August 3, 2011", "USB@September 27, 2010", "USB@September 11, 2009"]
    exceptbench_full += ["WFC@August 2, 2011", "WFC@August 3, 2011", "WFC@September 27, 2010", "WFC@September 11, 2009"]
    exceptbench_full += ["ZION@August 2, 2011", "ZION@August 3, 2011", "ZION@September 27, 2010",
                         "ZION@September 11, 2009"]

    ## bench case 29907
    exceptbench_full += ["AAPL@September 18, 2015", "AAPL@September 19, 2014", "AAPL@June 20, 2014",
                         "AAPL@March 6, 2014"]
    exceptbench_full += ["AAPL@March 1, 2013", "AAPL@November 7, 2012", "AAPL@August 24, 2012", "AAPL@June 26, 2012"]
    exceptbench_full += ["INTC@September 18, 2015", "INTC@September 19, 2014", "INTC@June 20, 2014",
                         "INTC@March 6, 2014"]
    exceptbench_full += ["INTC@March 1, 2013", "INTC@November 7, 2012", "INTC@August 24, 2012", "INTC@June 26, 2012"]
    exceptbench_full += ["IBM@September 18, 2015", "IBM@September 19, 2014", "IBM@June 20, 2014", "IBM@March 6, 2014"]
    exceptbench_full += ["IBM@March 1, 2013", "IBM@November 7, 2012", "IBM@August 24, 2012", "IBM@June 26, 2012"]
    exceptbench_full += ["PHGL@September 18, 2015", "PHG@September 19, 2014", "PHG@June 20, 2014", "PHG@March 6, 2014"]
    exceptbench_full += ["PHG@March 1, 2013", "PHG@November 7, 2012", "PHG@August 24, 2012", "PHG@June 26, 2012"]
    exceptbench_full += ["MSFT@September 18, 2015", "MSFT@September 19, 2014", "MSFT@June 20, 2014",
                         "MSFT@March 6, 2014"]
    exceptbench_full += ["MSFT@March 1, 2013", "MSFT@November 7, 2012", "MSFT@August 24, 2012", "MSFT@June 26, 2012"]
    exceptbench_full += ["NOK@September 18, 2015", "NOK@September 19, 2014", "NOK@June 20, 2014", "NOK@March 6, 2014"]
    exceptbench_full += ["NOK@March 1, 2013", "NOK@November 7, 2012", "NOK@August 24, 2012", "NOK@June 26, 2012"]

    ## bench case 31069
    exceptbench_full += ["AMPH@May 9, 2016", "AMPH@October 28, 2011", "AMPH@October 21, 2011", "AMPH@October 7, 2011"]
    exceptbench_full += ["MNTA@May 9, 2016", "MNTA@October 28, 2011", "MNTA@October 21, 2011", "MNTA@October 7, 2011"]

    ## bench case 33239
    exceptbench_full += ["AAPL@June 23, 2017", "AAPL@January 18, 2016", "AAPL@August 20, 2015",
                         "AAPL@November 25, 2014"]
    exceptbench_full += ["INTC@June 23, 2017", "INTC@January 18, 2016", "INTC@August 20, 2015",
                         "INTC@November 25, 2014"]
    exceptbench_full += ["IBM@June 23, 2017", "IBM@January 18, 2016", "IBM@August 20, 2015", "IBM@November 25, 2014"]
    exceptbench_full += ["MSFT@June 23, 2017", "MSFT@January 18, 2016", "MSFT@August 20, 2015",
                         "MSFT@November 25, 2014"]
    ######## exception cases

    url_v = "https://www.docketnavigator.com/detail/summary/case/"
    ids_v = ["13906", "29907", "31069", "33239"]
    urls_v = []
    for id in ids_v:
        urls_v.append(url_v + id)

    exceptjury_v = []
    exceptbench_v = []

    ## jury case 29907
    exceptjury_v += ["AAPL@November 21, 2013", "NOK@November 21, 2013"]

    ## jury case 33239
    exceptjury_v += ["AAPL@May 2, 2014", "AAPL@May 5, 2014"]

    ### bench case 13906
    exceptbench_v += ["RMBS@May 8, 2013", "RMBS@March 21, 2012", "RMBS@January 11, 2012", "RMBS@March 8, 2010",
                      "RMBS@March 10, 2009"]

    ### bench case 29907
    exceptbench_v += ["AAPL@September 18, 2015", "AAPL@September 19, 2014", "AAPL@June 20, 2014",
                      "AAPL@March 6, 2014"]
    exceptbench_v += ["AAPL@March 1, 2013", "AAPL@November 7, 2012", "AAPL@August 24, 2012", "AAPL@June 26, 2012"]
    exceptbench_v += ["NOK@September 18, 2015", "NOK@September 19, 2014", "NOK@June 20, 2014", "NOK@March 6, 2014"]
    exceptbench_v += ["NOK@March 1, 2013", "NOK@November 7, 2012", "NOK@August 24, 2012", "NOK@June 26, 2012"]

    ## bench case 31069
    exceptbench_v += ["AMPH@May 9, 2016", "AMPH@October 28, 2011", "AMPH@October 21, 2011", "AMPH@October 7, 2011"]
    exceptbench_v += ["MNTA@May 9, 2016", "MNTA@October 28, 2011", "MNTA@October 21, 2011", "MNTA@October 7, 2011"]

    ## bench case 33239
    exceptbench_v += ["AAPL@June 23, 2017", "AAPL@January 18, 2016", "AAPL@August 20, 2015", "AAPL@November 25, 2014"]
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
                    amount_100thd.append(row[8] + "@" + rdates[ind])

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
                        juryresult.append(row[8] + "@" + rdates[remi])
                    else:
                        benchresult.append(row[8] + "@" + rdates[remi])


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
                        valid_benfit.append(row[8] + "@" + rdates[i])
                    if nonbenes[i] == row[9]:
                        valid_against.append(row[8] + "@" + rdates[i])

                    if amounts[i] > 100000:
                        valid_amount_100thd.append(row[8] + "@" + rdates[i])

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
                        valid_jury.append(row[8] + "@" + rdates[i])
                    elif row[26] not in urls_v:
                        valid_bench.append(row[8] + "@" + rdates[i])

        res_tjury = list(set(juryresult))
        res_tbench = list(set(benchresult))
        res_tjb = []
        res_t100thd = set(amount_100thd)
        for i in res_tjury:
            if i in res_tbench:
                res_tjb.append(i)
        for i in res_tjb:
            res_tjury.remove(i)
            res_tbench.remove(i)


        res_tvjury = list(set(valid_jury))
        res_tvbench = list(set(valid_bench))
        res_tvjb = []
        res_tv100thd = set(valid_amount_100thd)
        for i in res_tvjury:
            if i in res_tvbench:
                res_tvjb.append(i)
        for i in res_tvjb:
            res_tvjury.remove(i)
            res_tvbench.remove(i)

        res_tvbenefit = list(set(valid_benfit))
        res_tvagainst = list(set(valid_against))
        res_tvbfa = []
        for i in res_tvbenefit:
            if i in res_tvagainst:
                res_tvbfa.append(i)
        for i in res_tvbfa:
            res_tvbenefit.remove(i)
            res_tvagainst.remove(i)


        with open("../Data/Trial/Trial_TDC.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(["Stock_Ticker", "Decision_Date", "Category"])

            for row in res_tjury:
                cate = "TJ"
                if row in res_t100thd:
                    cate += "|T100"
                if row in res_tvbenefit:
                    cate += "|TVBF"
                if row in res_tvagainst:
                    cate += "|TVA"
                if row in res_tvbfa:
                    cate += "|TVBFA"
                if row in res_tvjury:
                    cate += "|TVJ"
                if row in res_tvbench:
                    cate += "|TVB"
                if row in res_tvjb:
                    cate += "|TVJB"
                if row in res_tv100thd:
                    cate += "|TV100"
                writer.writerow(row.split("@") + [cate])

            for row in res_tbench:
                cate = "TB"
                if row in res_t100thd:
                    cate += "|T100"
                if row in res_tvbenefit:
                    cate += "|TVBF"
                if row in res_tvagainst:
                    cate += "|TVA"
                if row in res_tvbfa:
                    cate += "|TVBFA"
                if row in res_tvjury:
                    cate += "|TVJ"
                if row in res_tvbench:
                    cate += "|TVB"
                if row in res_tvjb:
                    cate += "|TVJB"
                if row in res_tv100thd:
                    cate += "|TV100"
                writer.writerow(row.split("@") + [cate])

            for row in res_tjb:
                cate = "TB"
                if row in res_t100thd:
                    cate += "|T100"
                if row in res_tvbenefit:
                    cate += "|TVBF"
                if row in res_tvagainst:
                    cate += "|TVA"
                if row in res_tvbfa:
                    cate += "|TVBFA"
                if row in res_tvjury:
                    cate += "|TVJ"
                if row in res_tvbench:
                    cate += "|TVB"
                if row in res_tvjb:
                    cate += "|TVJB"
                if row in res_tv100thd:
                    cate += "|TV100"
                writer.writerow(row.split("@") + [cate])

        print ["All appellate data : ", len(res_tjury) + len(res_tbench) + len(res_tjb)]
        print ["Category TJ : Trial with jury decision : ", len(res_tjury)]
        print ["Category TB : Trial with bench decision : ", len(res_tbench)]
        print ["Category TJB : Trial with both jury&bench decision : ", len(res_tjb)]
        print ["Category T100 : Trial with remedy amount larger than $100,000 : ", len(res_t100thd)]
        print ["Category TVJ : Trial benefit valided with jury decision : ", len(res_tvjury)]
        print ["Category TVB : Trial benefit valided with bench decision : ", len(res_tvbench)]
        print ["Category TVJB : Trial benefit valided with with both jury&bench decision : ", len(res_tvjb)]
        print ["Category TVBF : Trial benefit valided and is beneficiary party in the remedy : ", len(res_tvbenefit)]
        print ["Category TVA : Trial benefit valided and is against party in the remedy : ", len(res_tvagainst)]
        print ["Category TVBFA : Trial benefit valided and is both beneficiary&agianst party in the remedy : ", len(res_tvbfa)]
        print ["Category TV100 : Trial benefit valided with remedy amount larger than $100,000 : ", len(res_tv100thd)]


trial_division()