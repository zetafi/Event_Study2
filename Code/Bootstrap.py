import csv
import random


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


cates_app = [["A1", "A2", "A3"]]


def bs_one():
    appellate_sd_filepath = "../Data/Appellate/Appellate_TDCSM_[-60,-30)_[-20,5)_BS.csv"
    with open(appellate_sd_filepath, 'rb') as csvfile:
        appdata = csv.reader(csvfile)
        header = next(appdata)

        listappdata = list(appdata)

        cate = cates_app[0]

        bstime = 100000

        total_result_abs = []
        total_result_sq = []
        total_result_mean = []

        for win in windows_app:
            print "Window " + str(win[0]) + " " + str(win[1])
            resultabs = []
            resultsq = []
            resultmean = []
            for count in range(bstime):
                tmp_abs = float(0)
                tmp_sq = float(0)
                tmp_mean = float(0)
                count = 0

                for row in listappdata:
                    if row[4] == "ERROR":
                        continue

                    res = row[4].split("@")[2].split("|")

                    for i in range(0, len(res)):
                        res[i] = float(res[i])

                    cond_take = True

                    if win[0] < 0:
                        lastfiling = row[2].split("|")
                        for i in range(0, len(lastfiling)):
                            lastfiling[i] = int(lastfiling[i])
                            if lastfiling[i] <= -win[0]:
                                cond_take = False
                                break

                    if cond_take:
                        count += 1
                        car = float(0)
                        for count in range(0, win[1] - win[0]):
                            car += random.choice(res)
                        tmp_abs += abs(car)
                        tmp_sq += car ** 2
                        tmp_mean += car

                resultabs.append(tmp_abs)
                resultsq.append(tmp_sq)
                resultmean.append(tmp_mean / count)

            resultabs.sort()
            resultsq.sort()
            resultmean.sort()
            critical_value_abs = [resultabs[90000], resultabs[95000], resultabs[99000]]
            critical_value_sq = [resultsq[90000], resultsq[95000], resultsq[99000]]
            critical_value_mean = [resultmean[90000], resultmean[95000], resultmean[99000]]

            total_result_abs.append(["[" + str(win[0]) + "," + str(win[1]) + ")"] + critical_value_abs)
            total_result_sq.append(["[" + str(win[0]) + "," + str(win[1]) + ")"] + critical_value_sq)
            total_result_mean.append(["[" + str(win[0]) + "," + str(win[1]) + ")"] + critical_value_mean)

        with open("../Result/Standard_EstWin/A1&A2&A3/BS_mean_CAR.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(["Event Window", "90%", "95%", "99%"])
            for i in total_result_mean:
                writer.writerow(i)

        with open("../Result/Standard_EstWin/A1&A2&A3/BS_abs_CAR.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(["Event Window", "90%", "95%", "99%"])
            for i in total_result_abs:
                writer.writerow(i)

        with open("../Result/Standard_EstWin/A1&A2&A3/BS_sq_CAR.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(["Event Window", "90%", "95%", "99%"])
            for i in total_result_sq:
                writer.writerow(i)


def bs_two():
    windows_app2 = [[evtWin7l, evtWin7h]]

    appellate_sd_filepath = "../Data/Appellate/Appellate_TDCSM_[-60,-30)_[-20,5)_BS.csv"
    with open(appellate_sd_filepath, 'rb') as csvfile:
        appdata = csv.reader(csvfile)
        header = next(appdata)

        listappdata = list(appdata)

        cate = cates_app[0]

        bstime = 100000

        total_result_abs = []
        total_result_sq = []
        total_result_mean = []

        for win in windows_app2:
            print "Window " + str(win[0]) + " " + str(win[1])
            resultabs = []
            resultsq = []
            resultmean = []
            for count in range(bstime):
                tmp_abs = float(0)
                tmp_sq = float(0)
                tmp_mean = float(0)
                count = 0

                for row in listappdata:
                    if row[4] == "ERROR":
                        continue

                    res = row[4].split("@")[2].split("|")

                    for i in range(0, len(res)):
                        res[i] = float(res[i])

                    cond_take = True

                    if win[0] < 0:
                        lastfiling = row[2].split("|")
                        for i in range(0, len(lastfiling)):
                            lastfiling[i] = int(lastfiling[i])
                            if lastfiling[i] <= -win[0]:
                                cond_take = False
                                break

                    if cond_take:
                        count += 1
                        car = float(0)
                        for count in range(0, win[1] - win[0]):
                            car += random.choice(res)
                        tmp_abs += abs(car)
                        tmp_sq += car ** 2
                        tmp_mean += car

                resultabs.append(tmp_abs)
                resultsq.append(tmp_sq)
                resultmean.append(tmp_mean / count)

            resultabs.sort()
            resultsq.sort()
            resultmean.sort()
            critical_value_abs = [resultabs[90000], resultabs[95000], resultabs[99000]]
            critical_value_sq = [resultsq[90000], resultsq[95000], resultsq[99000]]
            critical_value_mean = [resultmean[90000], resultmean[95000], resultmean[99000]]

            total_result_abs.append(["[" + str(win[0]) + "," + str(win[1]) + ")"] + critical_value_abs)
            total_result_sq.append(["[" + str(win[0]) + "," + str(win[1]) + ")"] + critical_value_sq)
            total_result_mean.append(["[" + str(win[0]) + "," + str(win[1]) + ")"] + critical_value_mean)

        with open("../Result/Standard_EstWin/A1&A2&A3/BS_mean_CAR.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(["Event Window", "90%", "95%", "99%"])
            for i in total_result_mean:
                writer.writerow(i)

        with open("../Result/Standard_EstWin/A1&A2&A3/BS_abs_CAR.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(["Event Window", "90%", "95%", "99%"])
            for i in total_result_abs:
                writer.writerow(i)

        with open("../Result/Standard_EstWin/A1&A2&A3/BS_sq_CAR.csv", 'w') as resultfile:
            writer = csv.writer(resultfile)
            writer.writerow(["Event Window", "90%", "95%", "99%"])
            for i in total_result_sq:
                writer.writerow(i)

