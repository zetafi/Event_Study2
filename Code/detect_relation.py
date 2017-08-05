import csv
import sys
import datetime
import operator
import requests
import time
import os
import re
import math

def getY():
    csv.field_size_limit(sys.maxsize)
    with open('../Data/Trial/all_complete_trial.csv', 'rb') as csvfile:
        fulltrdata = csv.reader(csvfile)
        header = fulltrdata.next()

        amount100thd = []

        for row in fulltrdata:

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
                    amount100thd.append(row[8] + "@" + rdates[ind] + "@" + str(amounts[ind]))

        with open("../Data/Trial/Trial_detection.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(["Stock_Ticker", "Decision_Date", "Remedy_Amount"])

            for i in amount100thd:
                writer.writerow(i.split("@"))




def getY2():
    csv.field_size_limit(sys.maxsize)
    with open('../Data/Appellate/appellate_all.csv', 'rb') as csvfile:
        apdata = csv.reader(csvfile)
        header = apdata.next()

        results = []

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

                        lastind = ind - 1
                        lastfiling = (
                        datetime.datetime.strptime(fdates[ind], "%B %d, %Y").date() - datetime.datetime.strptime(
                            fdates[lastind], "%B %d, %Y").date()).days
                        while lastfiling == 0:
                            lastind -= 1
                            lastfiling = (
                            datetime.datetime.strptime(fdates[ind], "%B %d, %Y").date() - datetime.datetime.strptime(
                                fdates[lastind], "%B %d, %Y").date()).days


                        if judgresult == "Affirmed" or judgresult == "affirmed":
                            results.append([row[8] + "@" + fdates[ind] + "@1", str(lastfiling)])
                        else:
                            results.append([row[8] + "@" + fdates[ind] + "@0", str(lastfiling)])

        res_dict = {}
        for item in results:
            if res_dict.has_key(item[0]):
                res_dict[item[0]].append(item[1])
            else:
                res_dict[item[0]] = [item[1]]

        fresults = []
        for key, value in res_dict.iteritems():
            add = True
            for v in value:
                if v <20:
                    add = False
            if add:
                fresults.append(key)

        with open("../Data/Appellate/Appellate_detection2_app01.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(["Stock_Ticker", "Decision_Date", "Affirmed_1__NotAff_0"])

            for i in fresults:
                writer.writerow(i.split("@"))

#getY()


#getY2()


bDate = (1970, 1, 1)
startDate = (1998, 1, 1)
endDate = (2017, 5, 30)

def request_prices(ticker):
    try:
        print "try to get price : " + ticker
        r = requests.get('https://finance.yahoo.com/quote/aapl/history')
        time.sleep(5)
        txt = r.text
        cookie = r.cookies['B']
        pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')
        for line in txt.splitlines():
            m = pattern.match(line)
            if m is not None:
                crumb = m.groupdict()['crumb']

        ##solve \u002 situation in the crumb
        ##replaced
        crumb = crumb.replace("\u002F", "/");
        ####

        data = (ticker, int((datetime.datetime(*startDate) - datetime.datetime(*bDate)).total_seconds()),
                int((datetime.datetime(*endDate) - datetime.datetime(*bDate)).total_seconds()), crumb)
        url = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1={1}&period2={2}&interval=1d&events=history&crumb={3}".format(
            *data)
        data = requests.get(url, cookies={'B': cookie})
        data_file = open("../Data/prices/" + ticker + ".csv", "w")
        data_file.write(data.text)
        data_file.close()

        with open('../Data/prices/' + ticker + '.csv', 'rb') as csvfile:
            prices = csv.reader(csvfile)
            header = next(prices)
            if header[0] != "Date":
                print "fail to get the prices"
                return False
        print "got prices : " + ticker
        return True
    except:
        print "Another Attempt for " + ticker
        return False



def stock_rr(compCode, eDate, begin, end) :

    if compCode in ["PHGL"]:
        errorlog = []
        errorlog.append(compCode)
        errorlog.append(eDate.date().isoformat())
        errorlog.append("[" + str(begin) + ", " + str(end) + ")")
        errorlog.append("can\'t get the company price from yahoo finance")
        print errorlog
        error = "@".join(errorlog)
        return ["ERROR", error]

    if not os.path.exists("../Data/prices/" + compCode + ".csv"):
        done = False
        while not done:
            done = request_prices(compCode)


    #Read estimation window data
    with open('../Data/prices/' + compCode + '.csv', 'rb') as csvfile :
        prices = csv.reader(csvfile)
        header = next(prices)
        prices = list(prices)


        ## binary search for the index of the event day
        low = 0
        high = len(prices) - 1
        mid = (low + high) / 2
        while (high - low) > 1 :
            mid = (low + high) / 2
            if datetime.datetime.strptime(prices[mid][0], "%Y-%m-%d") <= eDate :
                low = mid
            elif eDate < datetime.datetime.strptime(prices[mid][0], "%Y-%m-%d") :
                high = mid
        mid = low
        ## end binary search , mid as the result index



        ## If the event date is not in the price file return error informatino
        if eDate != datetime.datetime.strptime(prices[mid][0], "%Y-%m-%d"):
            ## stock_rr error information format [ticker, eDate, [Begin, end), error description]
            errorlog = []
            errorlog.append(compCode)
            errorlog.append(eDate.date().isoformat())
            errorlog.append("[" + str(begin) + ", " + str(end) + ")")
            errorlog.append("the Event Date does not exist in its price file")
            print errorlog
            error = "@".join(errorlog)
            return ["ERROR", error]



        # verify enough data for estimation
        if mid + begin  < 1 or mid + end > len(prices) :
            errorlog = []
            errorlog.append(compCode)
            errorlog.append(eDate.date().isoformat())
            errorlog.append("[" + str(begin) + ", " + str(end) + ")")
            errorlog.append("Not enough price data for this duration")
            print errorlog
            error = "@".join(errorlog)
            return ["ERROR", error]


        ## retrieve the result estimation window
        estwin_price = []

        ## retrieve the adjusted close prices
        for i in range(begin-1, end) :
            if prices[mid + i][5] != "null":
                estwin_price.append(float(prices[mid + i][5]))
            else:
                estwin_price.append(0)

        pos0 = [i for i, x in enumerate(estwin_price) if x == 0]

        ## Return error if there are 0 prices in the duration
        if len(pos0) != 0:
            errorlog = []
            errorlog.append(compCode)
            errorlog.append(eDate.date().isoformat())
            errorlog.append("[" + str(begin) + ", " + str(end) + ")")

            errordes = ""
            for i in pos0:
                errordes += "Zero Price error, " + prices[mid + i + begin][0] + " price is : " + prices[mid + i + begin][5] + " | "
            errorlog.append(errordes)
            print errorlog
            error = "@".join(errorlog)
            return ["ERROR", error]


        #retrieve the return rate
        estwin_rr = []
        for i in range(1, len(estwin_price)) :
            estwin_rr.append(math.log(estwin_price[i]/estwin_price[i-1]))
            #  another algorithm : estwin_rr.append( (estwin_price[i] - estwin_price[i-1])/estwin_price[i-1] )


        ## Return error if the prices are constant in the duration
        if sum(estwin_rr)==0:
            errorlog = []
            errorlog.append(compCode)
            errorlog.append(eDate.date().isoformat())
            errorlog.append("[" + str(begin) + ", " + str(end) + ")")
            errorlog.append("Prices are constant in this duration, not useful")
            print errorlog
            error = "@".join(errorlog)
            return ["ERROR", error]

        #print [prices[mid+begin][0], prices[mid+end][0],begin,end]
        return estwin_rr




def abnormalRe(compCode, eDate,evtbegin, evtend) :

    #Estimation window rates

    evtwin_rr = stock_rr(compCode, eDate, evtbegin, evtend)

    #SPY as SP500 rates

    spy_evt_rr = stock_rr('SPY', eDate, evtbegin, evtend)

    if evtwin_rr[0] == "ERROR" or spy_evt_rr[0] == "ERROR":

        errorinfo = []
        errorinfo.append("ERROR_CASE")

        if evtwin_rr[0] == "ERROR":
            errorinfo.append(evtwin_rr[1])
        else:
            errorinfo.append("No_problem")

        if spy_evt_rr[0] == "ERROR":
            errorinfo.append(spy_evt_rr[1])
        else:
            errorinfo.append("No_problem")

        return errorinfo

    # CAPM regression with spy_rates and estwin rates
    beta = sum(map(operator.mul, map(lambda i: i-sum(evtwin_rr)/len(evtwin_rr), evtwin_rr), map(lambda i: i-sum(spy_evt_rr)/len(spy_evt_rr), spy_evt_rr))) / sum(map(lambda i: i*i, map(lambda i: i-sum(spy_evt_rr)/len(spy_evt_rr), spy_evt_rr)))
    alpha = sum(evtwin_rr)/len(evtwin_rr) - beta*sum(spy_evt_rr)/len(spy_evt_rr)

    # RSE
    #rse = (sum(map(lambda i:i*i, map(operator.sub, map(lambda i: i-alpha, estwin_rr), map(lambda i:i*beta, spy_est_rr)))) / (len(estwin_rr)-2))**0.5
    # AR
    estimated_rr = map(lambda i:i*beta+alpha, spy_evt_rr)

    #sd (rse * (evtend-evtbegin)**0.5 )


    return sum(estimated_rr)
################################END_Abnormal Return calculator###################################################





def calculate_ar():
    with open('../Data/Appellate/Appellate_detection2_app01.csv', 'rb') as csvfile :
        datas = csv.reader(csvfile)
        header = next(datas)

        results = []

        count = 0
        for row in datas:
            eDate = datetime.datetime.strptime(row[1], "%B %d, %Y")
            cal = abnormalRe(row[0], eDate, -20, 0)

            if isinstance(cal,list):
                with open("../Data/Appellate/ERROR_LOG_SM_[-20,0)_2LS.csv", "a") as errorfile:
                    errorwriter = csv.writer(errorfile)
                    errorwriter.writerow([row[0], row[1]] + cal[1:len(cal)])
                cal = "ERROR"
            else:
                count += 1

            row.append(cal)
            results.append(row)

        header.append("SM_[-20,0)_2LS")


        with open("../Data/Appellate/Appellate_detection2_app01_SM_[-20,0)_2LS.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(header)
            for row in results:
                writer.writerow(row)


#calculate_ar()



def step2_reg():
    with open('../Data/Appellate/Appellate_detection2_app01_SM_[-20,0)_2LS.csv', 'rb') as csvfile :
        datas = csv.reader(csvfile)
        header = next(datas)
        Y = []
        X = []
        count = 0

        for row in datas:
            if row[3] != "ERROR":
                Y.append(int(row[2]))
                X.append(float(row[3]))
                count += 1

        print count
        # with open("../Data/Appellate/Appellate_detection2_reg01_XY.csv", 'w') as resultfile:
        #     writer = csv.writer(resultfile)
        #     writer.writerow(["X", "Y"])
        #
        #     for i in range(len(Y)):
        #         writer.writerow([X[i], Y[i]])

#step2_reg()