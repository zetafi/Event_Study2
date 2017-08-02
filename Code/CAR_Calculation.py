import time
import requests
import re
import datetime
import math
import operator
import csv
import os
import random
from glob import glob
import bisect
import numpy as np



#Func 1
################################prices requirer##############################################
## Input: ticker
## Return : True/False

## Dates
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
################################ END prices requirer##############################################



#Func 2
################################Ratio calculator###################################################
## Input: compCode EventDate  EstimationWin start/end
## Output: list of ratio in EstWin if no error.
## Output: return a list of one string of the error information separated by @ if error occurs
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

################################END Ratio calculator###################################################

#print len(stock_rr('YHOO', datetime.datetime(2010, 04, 29), -60, -30))

def factor_get(eDate, begin, end, type):
    with open('../Data/factors.csv', 'rb') as csvfile:
        factors = csv.reader(csvfile)
        header = next(factors)
        factors = list(factors)

        if type not in header:
            errorlog = []
            errorlog.append("FACTOR_ERROR")
            errorlog.append(eDate.date().isoformat())
            errorlog.append("[" + str(begin) + ", " + str(end) + ")")
            errorlog.append("type: " + type)
            errorlog.append(" type does not exist!")
            print errorlog
            error = "@".join(errorlog)
            return ["ERROR",error]

        ## binary search for the index of the event day
        low = 0
        high = len(factors) - 1
        mid = (low + high) / 2
        while (high - low) > 1:
            mid = (low + high) / 2
            if datetime.datetime.strptime(factors[mid][0].replace(",",""), "%Y%m%d") <= eDate:
                low = mid
            elif eDate < datetime.datetime.strptime(factors[mid][0].replace(",",""), "%Y%m%d"):
                high = mid
        mid = low
        ## end binary search , mid as the result index
        if eDate != datetime.datetime.strptime(factors[mid][0].replace(",",""), "%Y%m%d"):
            errorlog = []
            errorlog.append("FACTOR_ERROR")
            errorlog.append(eDate.date().isoformat())
            errorlog.append("[" + str(begin) + ", " + str(end) + ")")
            errorlog.append("TYPE: " + type)
            errorlog.append("the Event Date does not exist in the factor file")
            print errorlog
            error = "@".join(errorlog)
            return ["ERROR", error]

        if mid + begin < 0 or mid + end > len(factors) :
            errorlog = []
            errorlog.append("FACTOR_ERROR")
            errorlog.append(eDate.date().isoformat())
            errorlog.append("[" + str(begin) + ", " + str(end) + ")")
            errorlog.append("TYPE: " + type)
            errorlog.append("Not enough factors data for this duration")
            print errorlog
            error = "@".join(errorlog)
            return ["ERROR", error]

        result_factor = []
        ntype = -1
        for t in range(4):
            if type == header[t]:
                ntype = t

        for i in range(begin, end):
            result_factor.append(float(factors[mid+i][ntype]))
        return result_factor


#print len(factor_get(datetime.datetime(2009, 1, 20), -60, -30, "HML"))


#Func 3
################################Abnormal Return calculator###################################################
## Input: compCode, EventDate, EstWin start/end, EvtWin start/end
## return:[comp name, event date, car, car/sigma] if no error
## return list of length 5 with first one a string "ERROR_CASE"
def abnormalRe(compCode, eDate, estbegin, estend, evtbegin, evtend, bs) :

    #Estimation window rates
    estwin_rr = stock_rr(compCode, eDate, estbegin, estend)

    evtwin_rr = stock_rr(compCode, eDate, evtbegin, evtend)

    #SPY as SP500 rates
    spy_est_rr = stock_rr('SPY', eDate, estbegin, estend)

    spy_evt_rr = stock_rr('SPY', eDate, evtbegin, evtend)

    if estwin_rr[0] == "ERROR"  or evtwin_rr[0] == "ERROR" \
            or spy_est_rr[0] == "ERROR"  or spy_evt_rr[0] == "ERROR":

        errorinfo = []
        errorinfo.append("ERROR_CASE")

        if estwin_rr[0] == "ERROR":
            errorinfo.append(estwin_rr[1])
        else:
            errorinfo.append("No_problem")

        if evtwin_rr[0] == "ERROR":
            errorinfo.append(evtwin_rr[1])
        else:
            errorinfo.append("No_problem")

        if spy_est_rr[0] == "ERROR":
            errorinfo.append(spy_est_rr[1])
        else:
            errorinfo.append("No_problem")

        if spy_evt_rr[0] == "ERROR":
            errorinfo.append(spy_evt_rr[1])
        else:
            errorinfo.append("No_problem")

        return errorinfo

    # CAPM regression with spy_rates and estwin rates
    beta = sum(map(operator.mul, map(lambda i: i-sum(estwin_rr)/len(estwin_rr), estwin_rr), map(lambda i: i-sum(spy_est_rr)/len(spy_est_rr), spy_est_rr))) / sum(map(lambda i: i*i, map(lambda i: i-sum(spy_est_rr)/len(spy_est_rr), spy_est_rr)))
    alpha = sum(estwin_rr)/len(estwin_rr) - beta*sum(spy_est_rr)/len(spy_est_rr)

    # RSE
    rse = (sum(map(lambda i:i*i, map(operator.sub, map(lambda i: i-alpha, estwin_rr), map(lambda i:i*beta, spy_est_rr)))) / (len(estwin_rr)-2))**0.5
    # AR
    ab_re = map(operator.sub, evtwin_rr, map(lambda i:i*beta+alpha, spy_evt_rr))

    #sd (rse * (evtend-evtbegin)**0.5 )


    # Bootstrap CAR calculation
    res = map(operator.sub, map(lambda i: i - alpha, estwin_rr), map(lambda i: i * beta, spy_est_rr))

    str_ab_re = "|".join(map(str, ab_re))
    str_res = "|".join(map(str,res))

    if bs:
        return "@".join([str_ab_re, str(rse), str_res])
    else:
        return "@".join([str_ab_re, str(rse)])

################################END_Abnormal Return calculator###################################################




#print abnormalRe('NOK', datetime.datetime(2014,12,4),-60,-30,-5,0,False)


def abnormal_return_mf(compCode, eDate, estbegin, estend, evtbegin, evtend):
    # Estimation window rates
    estwin_rr = stock_rr(compCode, eDate, estbegin, estend)

    evtwin_rr = stock_rr(compCode, eDate, evtbegin, evtend)

    # Rf   Rm-Rf   SMB    HML
    est_Rf = factor_get(eDate, estbegin, estend, "RF")
    est_Rm_Rf = factor_get(eDate, estbegin, estend, "Mkt-RF")
    est_SMB = factor_get(eDate, estbegin, estend, "SMB")
    est_HML = factor_get(eDate, estbegin, estend, "HML")

    evt_Rf = factor_get(eDate, evtbegin, evtend, "RF")
    evt_Rm_Rf = factor_get(eDate, evtbegin, evtend, "Mkt-RF")
    evt_SMB = factor_get(eDate, evtbegin, evtend, "SMB")
    evt_HML = factor_get(eDate, evtbegin, evtend, "HML")

    if estwin_rr[0] == "ERROR"  or evtwin_rr[0] == "ERROR" \
            or est_Rf[0] == "ERROR" or evt_Rf[0] == "ERROR" \
            or est_Rm_Rf[0] == "ERROR" or evt_Rm_Rf[0] == "ERROR" \
            or est_SMB[0] == "ERROR" or evt_SMB[0] == "ERROR" \
            or est_HML[0] == "ERROR" or evt_HML[0] == "ERROR":

        errorinfo = []
        errorinfo.append("ERROR_CASE")

        if estwin_rr[0] == "ERROR":
            errorinfo.append(estwin_rr[1])
        else:
            errorinfo.append("No_problem")

        if evtwin_rr[0] == "ERROR":
            errorinfo.append(evtwin_rr[1])
        else:
            errorinfo.append("No_problem")

        if est_Rf[0] == "ERROR":
            errorinfo.append(est_Rm_Rf[1])
        else:
            errorinfo.append("No_problem")

        if evt_Rf[0] == "ERROR":
            errorinfo.append(evt_Rm_Rf[1])
        else:
            errorinfo.append("No_problem")
        if est_Rm_Rf[0] == "ERROR":
            errorinfo.append(est_Rm_Rf[1])
        else:
            errorinfo.append("No_problem")

        if evt_Rm_Rf[0] == "ERROR":
            errorinfo.append(evt_Rm_Rf[1])
        else:
            errorinfo.append("No_problem")
        if est_SMB[0] == "ERROR":
            errorinfo.append(est_SMB[1])
        else:
            errorinfo.append("No_problem")

        if evt_SMB[0] == "ERROR":
            errorinfo.append(evt_SMB[1])
        else:
            errorinfo.append("No_problem")
        if est_HML[0] == "ERROR":
            errorinfo.append(est_HML[1])
        else:
            errorinfo.append("No_problem")

        if evt_HML[0] == "ERROR":
            errorinfo.append(evt_HML[1])
        else:
            errorinfo.append("No_problem")

        return errorinfo

    ## Multifactor model
    #print len(estwin_rr)
    #print len(est_Rf)
    Y = map(operator.sub, estwin_rr, est_Rf)
    X = [[1]*(estend-estbegin), est_Rm_Rf, est_SMB, est_HML]

    Y = np.matrix(Y).getT()
    X = np.matrix(X).getT()


    #print Y
    BETA = (((X.getT().dot(X)).getI()).dot(X.getT())).dot(Y)

    RES = Y - X.dot(BETA)


    # RSE
    RSE = ((RES.getT().dot(RES))/(len(estwin_rr)-4))[0,0] ** 0.5

    # AR
    AB_RE = np.matrix(evtwin_rr).getT() - np.matrix(evt_Rf).getT() \
            - (np.matrix([[1]*(evtend-evtbegin), evt_Rm_Rf, evt_SMB, evt_HML]).getT()).dot(BETA)


    # SD (RES * ((evtend - evtbegin) ** 0.5))


    str_res = "|".join(map(str, AB_RE.getT().tolist()[0]))

    return str_res + "@" + str(RSE)

#print abnormal_return_mf('NOK', datetime.datetime(2014, 12, 4), -60, -30, -20, 5)

## Func 4
def all_AR(filepath, estWinl,estWinh, evtWinl, evtWinh, mod = "SM", bs = False):

    if filepath.find("Trial") == -1:
        type = "Appellate"
    else:
        type = "Trial"

    if bs == False:
        bootstrap = "NBS"
    else:
        bootstrap = "BS"

    header = None
    results = []

    count = 0

    with open(filepath, 'rb') as csvfile :
        datas = csv.reader(csvfile)
        header = next(datas)

        for row in datas:
            eDate = datetime.datetime.strptime(row[1], "%B %d, %Y")
            if mod == "SM":
                cal = abnormalRe(row[0], eDate, estWinl, estWinh, evtWinl, evtWinh, bs)
            else:
                cal = abnormal_return_mf(row[0], eDate, estWinl, estWinh, evtWinl, evtWinh)

            if isinstance(cal,list):
                with open("../Data/" + type + "/ERROR_LOG_" + mod + "_[" + str(estWinl) + "," + str(estWinh) + ")_[" + str(evtWinl) + "," + str(evtWinh) + ")_" + bootstrap + ".csv", "a") as errorfile:
                    errorwriter = csv.writer(errorfile)
                    errorwriter.writerow([row[0], row[1]] + cal[1:len(cal)])
                cal = "ERROR"
            else:
                count += 1
            row.append(cal)
            results.append(row)

    header.append(mod + "_[" + str(estWinl) + "," + str(estWinh) + ")_[" + str(evtWinl) + "," + str(evtWinh) + ")_" + bootstrap)


    ind = filepath.find(".csv")
    newfilepath = filepath[0:ind]+mod + "_[" + str(estWinl) + "," + str(estWinh) + ")_[" + str(evtWinl) + "," + str(evtWinh) + ")_" + bootstrap+".csv"
    with open(newfilepath, 'w') as resultfile:
        writer = csv.writer(resultfile)
        writer.writerow(header)

        for row in results:
            writer.writerow(row)



#all_AR("../Data/Appellate/Appellate_TDC.csv", -60, -30, -20, 5, mod="SM", bs=False)
#all_AR("../Data/Appellate/Appellate_TDC.csv", -225, -50, -20, 5, mod="SM", bs=True)
#all_AR("../Data/Appellate/Appellate_TDC.csv", -180, -10, -20, 5, mod="SM", bs=True)
#all_AR("../Data/Appellate/Appellate_TDC.csv", -60, -30, -20, 5, mod="MM", bs=False)

#all_AR("../Data/Trial/Trial_TDC.csv", -60, -30, -20, 5, mod="SM", bs=False)
##TODO ext window wrong
#all_AR("../Data/Trial/Trial_TDC.csv", -180, -10, -20, 5, mod="SM", bs=True)
#all_AR("../Data/Trial/Trial_TDC.csv", -225, -50, -20, 5, mod="SM", bs=True)
#all_AR("../Data/Trial/Trial_TDC.csv", -60, -30, -20, 5, mod="MM", bs=False)




estWinl = -60
estWinh = -30

extestWinl1 = -225
extestWinh1 = -50

extestWinl2 = -180
extestWinh2 = -10

evtWin1l = -20
evtWin1h = 0
evtWin2l = -10
evtWin2h = 0
evtWin3l = -5
evtWin3h = 0
evtWin4l = -2
evtWin4h = 0
evtWin5l = -2
evtWin5h = 3
evtWin6l = 0
evtWin6h = 2
evtWin7l = 0
evtWin7h = 5

windows_app = [[evtWin1l,evtWin1h], [evtWin2l,evtWin2h], [evtWin3l,evtWin3h], [evtWin4l,evtWin4h], [evtWin5l,evtWin5h], [evtWin6l,evtWin6h], [evtWin7l,evtWin7h]]
windows_tr = [[evtWin3l,evtWin3h], [evtWin4l,evtWin4h], [evtWin5l,evtWin5h], [evtWin6l,evtWin6h], [evtWin7l,evtWin7h]]

cates_app = [["A1"], ["A2"], ["A1", "A2", "A3"]]
cates_tr = [["TJ"], ["TB"], ["T100"], ["TJ","TB","TJB"], ["TVJ"], ["TVB"], ["TV100"], ["TVBF"], ["TVA"], ["TVJ", "TVB", "TVJB"]]


#Fun4
################################CAR calculator###################################################
## Input:
## Return:
def CAR_app_SD():

    ## Standard estimation window
    appellate_sd_filepath = "../Data/Appellate/Appellate_TDCSM_[-60,-30)_[-20,5)_NBS.csv"
    if not os.path.isdir("../Data/Appellate/SD_CAR"):
        os.mkdir("../Data/Appellate/SD_CAR")

    with open(appellate_sd_filepath, 'rb') as csvfile:
        appdata = csv.reader(csvfile)
        header = next(appdata)

        listappdata = list(appdata)

        for cate in cates_app:
            res_win1 = []
            res_win2 = []
            res_win3 = []
            res_win4 = []
            res_win5 = []
            res_win6 = []
            res_win7 = []

            total_res = [res_win1, res_win2, res_win3, res_win4, res_win5, res_win6, res_win7]

            for row in listappdata:
                if row[3] not in cate or row[4] == "ERROR":
                    continue

                ar = row[4].split("@")[0].split("|")
                rse = float(row[4].split("@")[1])

                for i in range(0, len(ar)):
                    ar[i] = float(ar[i])

                condn10 = True
                condn20 = True
                condn5 = True
                condn2 = True
                lastfiling = row[2].split("|")
                for i in range(0, len(lastfiling)):
                    lastfiling[i] = int(lastfiling[i])
                    if lastfiling[i] <= 20:
                        condn20 = False
                        if lastfiling[i] <= 10:
                            condn10 = False
                            if lastfiling[i] <= 5:
                                condn5 = False
                                if lastfiling[i] <=2:
                                    condn2 = False

                if condn20:
                    res_win1.append([row[0], row[1], sum(ar[(evtWin1l + 20):(evtWin1h + 20)]), sum(ar[(evtWin1l + 20):(evtWin1h + 20)]) / (rse * pow(evtWin1h - evtWin1l, 0.5))])

                if condn10:
                    res_win2.append([row[0], row[1], sum(ar[(evtWin2l + 20):(evtWin2h + 20)]), sum(ar[(evtWin2l + 20):(evtWin2h + 20)]) / (rse * pow(evtWin2h - evtWin2l, 0.5))])

                if condn5:
                    res_win3.append([row[0], row[1], sum(ar[(evtWin3l + 20):(evtWin3h + 20)]), sum(ar[(evtWin3l + 20):(evtWin3h + 20)]) / (rse * pow(evtWin3h - evtWin3l, 0.5))])

                if condn2:
                    res_win4.append([row[0], row[1], sum(ar[(evtWin4l + 20):(evtWin4h + 20)]), sum(ar[(evtWin4l + 20):(evtWin4h + 20)]) / (rse * pow(evtWin4h - evtWin4l, 0.5))])
                    res_win5.append([row[0], row[1], sum(ar[(evtWin5l + 20):(evtWin5h + 20)]), sum(ar[(evtWin5l + 20):(evtWin5h + 20)]) / (rse * pow(evtWin5h - evtWin5l, 0.5))])

                res_win6.append([row[0], row[1], sum(ar[(evtWin6l + 20):(evtWin6h + 20)]), sum(ar[(evtWin6l + 20):(evtWin6h + 20)]) / (rse * pow(evtWin6h - evtWin6l, 0.5))])
                res_win7.append([row[0], row[1], sum(ar[(evtWin7l + 20):(evtWin7h + 20)]), sum(ar[(evtWin7l + 20):(evtWin7h + 20)]) / (rse * pow(evtWin7h - evtWin7l, 0.5))])


            for wini in range(0,7):
                with open("../Data/Appellate/SD_CAR/" + "&".join(cate) + "_[" + str(windows_app[wini][0]) + "," + str(
                        str(windows_app[wini][1])) + ")_EstWin" + str(
                        estWinl) + "," + str(estWinh) + "_" + str(len(total_res[wini])) + ".csv", 'w') as resultfile:
                    writer = csv.writer(resultfile)
                    writer.writerow(["Stock_Ticker", "Decision_Date", "CAR", "CAR/Sigma"])
                    for i in total_res[wini]:
                        writer.writerow(i)
                print "\n\n"
                print "".join(cate) + "_[" + str(windows_app[wini][0]) + "," + str(
                        str(windows_app[wini][1])) + ")_EstWin" + str(
                        estWinl) + "," + str(estWinh) + "_" + str(len(total_res[wini]))
                print "\n\n"


def CAR_app_EXT1():
    ## Extended estimation window1

    appellate_ext_filepath = "../Data/Appellate/Appellate_TDCSM_[-225,-50)_[-20,5)_BS.csv"
    if not os.path.isdir("../Data/Appellate/EXT1_CAR"):
        os.mkdir("../Data/Appellate/EXT1_CAR")

    with open(appellate_ext_filepath, 'rb') as csvfile:
        appdata = csv.reader(csvfile)
        header = next(appdata)

        listappdata = list(appdata)

        for cate in cates_app:
            res_win1 = []
            res_win2 = []
            res_win3 = []
            res_win4 = []
            res_win5 = []
            res_win6 = []
            res_win7 = []

            total_res = [res_win1, res_win2, res_win3, res_win4, res_win5, res_win6, res_win7]

            for row in listappdata:
                if row[3] not in cate or row[4] == "ERROR":
                    continue

                ar = row[4].split("@")[0].split("|")
                rse = float(row[4].split("@")[1])
                res = row[4].split("@")[2].split("|")

                for i in range(0, len(ar)):
                    ar[i] = float(ar[i])
                for i in range(0, len(res)):
                    res[i] = float(res[i])



                condn10 = True
                condn20 = True
                condn5 = True
                condn2 = True
                lastfiling = row[2].split("|")
                for i in range(0, len(lastfiling)):
                    lastfiling[i] = int(lastfiling[i])
                    if lastfiling[i] <= 20:
                        condn20 = False
                        if lastfiling[i] <= 10:
                            condn10 = False
                            if lastfiling[i] <= 5:
                                condn5 = False
                                if lastfiling[i] <=2:
                                    condn2 = False

                if condn20:
                    car1 = sum(ar[(evtWin1l + 20):(evtWin1h + 20)])
                    car_mc1 = []
                    for bs in range(0, 100000):
                        car = float(0)
                        for count in range(0, evtWin1h - evtWin1l):
                            car += random.choice(res)
                        car_mc1.append(car)
                    car_mc1.sort()
                    pval1 = float(bisect.bisect_left(car_mc1, car1))
                    pval1 /= 100000
                    res_win1.append([row[0], row[1], car1, car1 / (rse * pow(evtWin1h - evtWin1l, 0.5)), pval1])

                if condn10:
                    car2 = sum(ar[(evtWin2l + 20):(evtWin2h + 20)])
                    car_mc2 = []
                    for bs in range(0, 100000):
                        car = float(0)
                        for count in range(0, evtWin2h - evtWin2l):
                            car += random.choice(res)
                        car_mc2.append(car)
                    car_mc2.sort()
                    pval2 = float(bisect.bisect_left(car_mc2, car2))
                    pval2 /= 100000
                    res_win2.append([row[0], row[1], car2, car2 / (rse * pow(evtWin2h - evtWin2l, 0.5)), pval2])

                if condn5:
                    car3 = sum(ar[(evtWin3l + 20):(evtWin3h + 20)])
                    car_mc3 = []
                    for bs in range(0, 100000):
                        car = float(0)
                        for count in range(0, evtWin3h - evtWin3l):
                            car += random.choice(res)
                        car_mc3.append(car)
                    car_mc3.sort()
                    pval3 = float(bisect.bisect_left(car_mc3, car3))
                    pval3 /= 100000
                    res_win3.append([row[0], row[1], car3, car3 / (rse * pow(evtWin3h - evtWin3l, 0.5)), pval3])

                if condn2:
                    car4 = sum(ar[(evtWin4l + 20):(evtWin4h + 20)])
                    car_mc4 = []
                    for bs in range(0, 100000):
                        car = float(0)
                        for count in range(0, evtWin4h - evtWin4l):
                            car += random.choice(res)
                        car_mc4.append(car)
                    car_mc4.sort()
                    pval4 = float(bisect.bisect_left(car_mc4, car4))
                    pval4 /= 100000
                    res_win4.append([row[0], row[1], car4, car4 / (rse * pow(evtWin4h - evtWin4l, 0.5)), pval4])

                    car5= sum(ar[(evtWin5l + 20):(evtWin5h + 20)])
                    car_mc5 = []
                    for bs in range(0, 100000):
                        car = float(0)
                        for count in range(0, evtWin5h - evtWin5l):
                            car += random.choice(res)
                        car_mc5.append(car)
                    car_mc5.sort()
                    pval5 = float(bisect.bisect_left(car_mc5, car5))
                    pval5 /= 100000
                    res_win5.append([row[0], row[1], car5, car5 / (rse * pow(evtWin5h - evtWin5l, 0.5)), pval5])

                car6 = sum(ar[(evtWin6l + 20):(evtWin6h + 20)])
                car_mc6 = []
                for bs in range(0, 100000):
                    car = float(0)
                    for count in range(0, evtWin6h - evtWin6l):
                        car += random.choice(res)
                    car_mc6.append(car)
                car_mc6.sort()
                pval6 = float(bisect.bisect_left(car_mc6, car6))
                pval6 /= 100000
                res_win6.append([row[0], row[1], car6, car6 / (rse * pow(evtWin6h - evtWin6l, 0.5)), pval6])

                car7 = sum(ar[(evtWin7l + 20):(evtWin7h + 20)])
                car_mc7 = []
                for bs in range(0, 100000):
                    car = float(0)
                    for count in range(0, evtWin7h - evtWin7l):
                        car += random.choice(res)
                    car_mc7.append(car)
                car_mc7.sort()
                pval7 = float(bisect.bisect_left(car_mc7, car7))
                pval7 /= 100000
                res_win7.append([row[0], row[1], car7, car7/ (rse * pow(evtWin7h - evtWin7l, 0.5)), pval7])



            for wini in range(0,7):
                with open("../Data/Appellate/EXT1_CAR/" + "&".join(cate) + "_[" + str(windows_app[wini][0]) + "," + str(
                        str(windows_app[wini][1])) + ")_EstWin" + str(
                    extestWinl1) + "," + str(extestWinh1) + "_" + str(len(total_res[wini])) + ".csv", 'w') as resultfile:
                    writer = csv.writer(resultfile)
                    writer.writerow(["Stock_Ticker", "Decision_Date", "CAR", "CAR/Sigma", "Bootstrap(CAR>%)"])
                    for i in total_res[wini]:
                        writer.writerow(i)
                print "\n\n"
                print "".join(cate) + "_[" + str(windows_app[wini][0]) + "," + str(
                        str(windows_app[wini][1])) + ")_EstWin" + str(
                        extestWinl1) + "," + str(extestWinh1) + "_" + str(len(total_res[wini]))
                print "\n\n"


def CAR_app_EXT2():
    ## Extended estimation window2
    #TODO evtwindow
    appellate_ext_filepath = "../Data/Appellate/Appellate_TDCSM_[-180,-10)_[-20,5)_BS.csv"
    if not os.path.isdir("../Data/Appellate/EXT2_CAR"):
        os.mkdir("../Data/Appellate/EXT2_CAR")

    with open(appellate_ext_filepath, 'rb') as csvfile:
        appdata = csv.reader(csvfile)
        header = next(appdata)

        listappdata = list(appdata)

        for cate in cates_app:
            res_win1 = []
            res_win2 = []
            res_win3 = []
            res_win4 = []
            res_win5 = []
            res_win6 = []
            res_win7 = []

            total_res = [res_win1, res_win2, res_win3, res_win4, res_win5, res_win6, res_win7]

            for row in listappdata:
                if row[3] not in cate or row[4] == "ERROR":
                    continue

                ar = row[4].split("@")[0].split("|")
                rse = float(row[4].split("@")[1])

                #TODO bootstrap

                for i in range(0, len(ar)):
                    ar[i] = float(ar[i])

                condn10 = True
                condn20 = True
                condn5 = True
                condn2 = True
                lastfiling = row[2].split("|")
                for i in range(0, len(lastfiling)):
                    lastfiling[i] = int(lastfiling[i])
                    if lastfiling[i] <= 20:
                        condn20 = False
                        if lastfiling[i] <= 10:
                            condn10 = False
                            if lastfiling[i] <= 5:
                                condn5 = False
                                if lastfiling[i] <=2:
                                    condn2 = False

                if condn20:
                    res_win1.append([row[0], row[1], sum(ar[(evtWin1l + 20):(evtWin1h + 20)]), sum(ar[(evtWin1l + 20):(evtWin1h + 20)]) / (rse * pow(evtWin1h - evtWin1l, 0.5))])

                if condn10:
                    res_win2.append([row[0], row[1], sum(ar[(evtWin2l + 20):(evtWin2h + 20)]), sum(ar[(evtWin2l + 20):(evtWin2h + 20)]) / (rse * pow(evtWin2h - evtWin2l, 0.5))])

                if condn5:
                    res_win3.append([row[0], row[1], sum(ar[(evtWin3l + 20):(evtWin3h + 20)]), sum(ar[(evtWin3l + 20):(evtWin3h + 20)]) / (rse * pow(evtWin3h - evtWin3l, 0.5))])

                if condn2:
                    res_win4.append([row[0], row[1], sum(ar[(evtWin4l + 20):(evtWin4h + 20)]), sum(ar[(evtWin4l + 20):(evtWin4h + 20)]) / (rse * pow(evtWin4h - evtWin4l, 0.5))])
                    res_win5.append([row[0], row[1], sum(ar[(evtWin5l + 20):(evtWin5h + 20)]), sum(ar[(evtWin5l + 20):(evtWin5h + 20)]) / (rse * pow(evtWin5h - evtWin5l, 0.5))])

                res_win6.append([row[0], row[1], sum(ar[(evtWin6l + 20):(evtWin6h + 20)]), sum(ar[(evtWin6l + 20):(evtWin6h + 20)]) / (rse * pow(evtWin6h - evtWin6l, 0.5))])
                res_win7.append([row[0], row[1], sum(ar[(evtWin7l + 20):(evtWin7h + 20)]), sum(ar[(evtWin7l + 20):(evtWin7h + 20)]) / (rse * pow(evtWin7h - evtWin7l, 0.5))])

            for wini in range(0,7):
                with open("../Data/Appellate/EXT2_CAR/" + "&".join(cate) + "_[" + str(windows_app[wini][0]) + "," + str(
                        str(windows_app[wini][1])) + ")_EstWin" + str(
                    extestWinh2) + "," + str(extestWinh2) + "_" + str(len(total_res[wini])) + ".csv", 'w') as resultfile:
                    writer = csv.writer(resultfile)
                    writer.writerow(["Stock_Ticker", "Decision_Date", "CAR", "CAR/Sigma"])
                    for i in total_res[wini]:
                        writer.writerow(i)
                print "\n\n"
                print "".join(cate) + "_[" + str(windows_app[wini][0]) + "," + str(
                        str(windows_app[wini][1])) + ")_EstWin" + str(
                        extestWinl2) + "," + str(extestWinh2) + "_" + str(len(total_res[wini]))
                print "\n\n"


def CAR_app_MLT():
    ## Multi-factor model & Standard estimation window
    appellate_sd_filepath = "../Data/Appellate/Appellate_TDCMM_[-60,-30)_[-20,5)_NBS.csv"
    if not os.path.isdir("../Data/Appellate/MLT_CAR"):
        os.mkdir("../Data/Appellate/MLT_CAR")

    with open(appellate_sd_filepath, 'rb') as csvfile:
        appdata = csv.reader(csvfile)
        header = next(appdata)

        listappdata = list(appdata)

        for cate in cates_app:
            res_win1 = []
            res_win2 = []
            res_win3 = []
            res_win4 = []
            res_win5 = []
            res_win6 = []
            res_win7 = []

            total_res = [res_win1, res_win2, res_win3, res_win4, res_win5, res_win6, res_win7]

            for row in listappdata:
                if row[3] not in cate or row[4] == "ERROR":
                    continue

                ar = row[4].split("@")[0].split("|")
                rse = float(row[4].split("@")[1])

                for i in range(0, len(ar)):
                    ar[i] = float(ar[i])

                condn10 = True
                condn20 = True
                condn5 = True
                condn2 = True
                lastfiling = row[2].split("|")
                for i in range(0, len(lastfiling)):
                    lastfiling[i] = int(lastfiling[i])
                    if lastfiling[i] <= 20:
                        condn20 = False
                        if lastfiling[i] <= 10:
                            condn10 = False
                            if lastfiling[i] <= 5:
                                condn5 = False
                                if lastfiling[i] <=2:
                                    condn2 = False

                if condn20:
                    res_win1.append([row[0], row[1], sum(ar[(evtWin1l + 20):(evtWin1h + 20)]), sum(ar[(evtWin1l + 20):(evtWin1h + 20)]) / (rse * pow(evtWin1h - evtWin1l, 0.5))])

                if condn10:
                    res_win2.append([row[0], row[1], sum(ar[(evtWin2l + 20):(evtWin2h + 20)]), sum(ar[(evtWin2l + 20):(evtWin2h + 20)]) / (rse * pow(evtWin2h - evtWin2l, 0.5))])

                if condn5:
                    res_win3.append([row[0], row[1], sum(ar[(evtWin3l + 20):(evtWin3h + 20)]), sum(ar[(evtWin3l + 20):(evtWin3h + 20)]) / (rse * pow(evtWin3h - evtWin3l, 0.5))])

                if condn2:
                    res_win4.append([row[0], row[1], sum(ar[(evtWin4l + 20):(evtWin4h + 20)]), sum(ar[(evtWin4l + 20):(evtWin4h + 20)]) / (rse * pow(evtWin4h - evtWin4l, 0.5))])
                    res_win5.append([row[0], row[1], sum(ar[(evtWin5l + 20):(evtWin5h + 20)]), sum(ar[(evtWin5l + 20):(evtWin5h + 20)]) / (rse * pow(evtWin5h - evtWin5l, 0.5))])

                res_win6.append([row[0], row[1], sum(ar[(evtWin6l + 20):(evtWin6h + 20)]), sum(ar[(evtWin6l + 20):(evtWin6h + 20)]) / (rse * pow(evtWin6h - evtWin6l, 0.5))])
                res_win7.append([row[0], row[1], sum(ar[(evtWin7l + 20):(evtWin7h + 20)]), sum(ar[(evtWin7l + 20):(evtWin7h + 20)]) / (rse * pow(evtWin7h - evtWin7l, 0.5))])

            for wini in range(0,7):
                with open("../Data/Appellate/MLT_CAR/" + "&".join(cate) + "_[" + str(windows_app[wini][0]) + "," + str(
                        str(windows_app[wini][1])) + ")_EstWin" + str(
                        estWinl) + "," + str(estWinh) + "_" + str(len(total_res[wini])) + ".csv", 'w') as resultfile:
                    writer = csv.writer(resultfile)
                    writer.writerow(["Stock_Ticker", "Decision_Date", "CAR", "CAR/Sigma"])
                    for i in total_res[wini]:
                        writer.writerow(i)
                print "\n\n"
                print "".join(cate) + "_[" + str(windows_app[wini][0]) + "," + str(
                        str(windows_app[wini][1])) + ")_EstWin" + str(
                        estWinl) + "," + str(estWinh) + "_" + str(len(total_res[wini]))
                print "\n\n"



# CAR_app_SD()
# CAR_app_MLT()
# CAR_app_EXT1()
# CAR_app_EXT2()


def CAR_tr_SD():
    ## Standard estimation window
    trial_sd_filepath = "../Data/Trial/Trial_TDCSM_[-60,-30)_[-20,5)_NBS.csv"
    if not os.path.isdir("../Data/Trial/SD_CAR"):
        os.mkdir("../Data/Trial/SD_CAR")

    with open(trial_sd_filepath, 'rb') as csvfile:
        trdata = csv.reader(csvfile)
        header = next(trdata)

        listtrdata = list(trdata)

        for cate in cates_tr:
            for win in windows_tr:
                car_res = []
                for row in listtrdata:
                    if row[3] == "ERROR":
                        continue
                    cates_row = row[2].split("|")
                    right_cate = False
                    for item in cates_row:
                        if item in cate:
                            right_cate = True
                            break
                    if not right_cate:
                        continue

                    ar = row[3].split("@")[0].split("|")
                    rse = float(row[3].split("@")[1])
                    for i in range(0, len(ar)):
                        ar[i] = float(ar[i])
                    car = sum(ar[(win[0] + 20):(win[1] + 20)])
                    car_res.append([row[0], row[1], car, car / (rse * pow(win[1] - win[0], 0.5))])

                with open("../Data/Trial/SD_CAR/" + "&".join(cate) + "_[" + str(win[0]) + "," + str(
                        str(win[1])) + ")_EstWin" + str(estWinl) + "," + str(estWinh) + "_" + str(len(car_res)) + ".csv", 'w') as resultfile:
                    writer = csv.writer(resultfile)
                    writer.writerow(["Stock_Ticker", "Decision_Date", "CAR", "CAR/Sigma"])
                    for i in car_res:
                        writer.writerow(i)
                print "\n\n"
                print "&".join(cate) + "_[" + str(win[0]) + "," + str(win[1]) + ")_EstWin" + str(
                    estWinl) + "," + str(estWinh) + "_" + str(len(car_res))
                print "\n\n"


def CAR_tr_EXT1():
    ## Standard estimation window
    trial_ext_filepath = "../Data/Trial/Trial_TDCSM_[-225,-50)_[-20,5)_BS.csv"
    if not os.path.isdir("../Data/Trial/EXT1_CAR"):
        os.mkdir("../Data/Trial/EXT1_CAR")

    with open(trial_ext_filepath, 'rb') as csvfile:
        trdata = csv.reader(csvfile)
        header = next(trdata)

        listtrdata = list(trdata)

        for cate in cates_tr:
            for win in windows_tr:

                print "Category : " + "&".join(cate) + "EstWin : " + str(win[0]) + " to " + str(win[1]) + "\n\n"
                car_res = []
                for row in listtrdata:
                    if row[3] == "ERROR":
                        continue
                    cates_row = row[2].split("|")
                    right_cate = False
                    for item in cates_row:
                        if item in cate:
                            right_cate = True
                            break
                    if not right_cate:
                        continue

                    ar = row[3].split("@")[0].split("|")
                    rse = float(row[3].split("@")[1])
                    res = row[3].split("@")[2].split("|")
                    for i in range(0, len(ar)):
                        ar[i] = float(ar[i])
                    for i in range(0, len(res)):
                        res[i] = float(res[i])

                    car = sum(ar[(win[0] + 20):(win[1] + 20)])
                    car_mc = []
                    for bs in range(0, 100000):
                        car = float(0)
                        for count in range(0, win[1] - win[0]):
                            car += random.choice(res)
                        car_mc.append(car)
                    car_mc.sort()
                    pval = float(bisect.bisect_left(car_mc, car))
                    pval /= 100000
                    car_res.append([row[0], row[1], car, car / (rse * pow(win[1] - win[0], 0.5)), pval])

                with open("../Data/Trial/EXT1_CAR/" + "&".join(cate) + "_[" + str(win[0]) + "," + str(
                        str(win[1])) + ")_EstWin" + str(extestWinl1) + "," + str(extestWinh1) + "_" + str(len(car_res)) + ".csv", 'w') as resultfile:
                    writer = csv.writer(resultfile)
                    writer.writerow(["Stock_Ticker", "Decision_Date", "CAR", "CAR/Sigma", "Bootstrap(CAR>%)"])
                    for i in car_res:
                        writer.writerow(i)
                print "\n\n"
                print "&".join(cate) + "_[" + str(win[0]) + "," + str(win[1]) + ")_EstWin" + str(
                    estWinl) + "," + str(estWinh) + "_" + str(len(car_res))
                print "\n\n"


def CAR_tr_MLT():
    ## Standard estimation window
    trial_mlt_filepath = "../Data/Trial/Trial_TDCMM_[-60,-30)_[-20,5)_NBS.csv"
    if not os.path.isdir("../Data/Trial/MLT_CAR"):
        os.mkdir("../Data/Trial/MLT_CAR")

    with open(trial_mlt_filepath, 'rb') as csvfile:
        trdata = csv.reader(csvfile)
        header = next(trdata)

        listtrdata = list(trdata)

        for cate in cates_tr:
            for win in windows_tr:
                car_res = []
                for row in listtrdata:
                    if row[3] == "ERROR":
                        continue
                    cates_row = row[2].split("|")
                    right_cate = False
                    for item in cates_row:
                        if item in cate:
                            right_cate = True
                            break
                    if not right_cate:
                        continue

                    ar = row[3].split("@")[0].split("|")
                    rse = float(row[3].split("@")[1])
                    for i in range(0, len(ar)):
                        ar[i] = float(ar[i])
                    car = sum(ar[(win[0] + 20):(win[1] + 20)])
                    car_res.append([row[0], row[1], car, car / (rse * pow(win[1] - win[0], 0.5))])

                with open("../Data/Trial/MLT_CAR/" + "&".join(cate) + "_[" + str(win[0]) + "," + str(
                        str(win[1])) + ")_EstWin" + str(estWinl) + "," + str(estWinh) + "_" + str(len(car_res)) + ".csv", 'w') as resultfile:
                    writer = csv.writer(resultfile)
                    writer.writerow(["Stock_Ticker", "Decision_Date", "CAR", "CAR/Sigma"])
                    for i in car_res:
                        writer.writerow(i)
                print "\n\n"
                print "&".join(cate) + "_[" + str(win[0]) + "," + str(win[1]) + ")_EstWin" + str(
                    estWinl) + "," + str(estWinh) + "_" + str(len(car_res))
                print "\n\n"




#CAR_tr_SD()
## TODO run ext1
#CAR_tr_EXT1()
#CAR_tr_MLT()
