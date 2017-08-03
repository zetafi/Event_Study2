# import csv
# import sys
#
#
#
#
#
#
#
# csv.field_size_limit(sys.maxsize)
#
# with open('../Data/Appellate/appellate_all.csv', 'rb') as csvfile:
#     apdata = csv.reader(csvfile)
#     header = apdata.next()
#
#     roles = []
#
#     count1 = 0
#     count2 = 0
#     count3 = 0
#     count4 = 0
#
#     counts = [0] * len(cross)
#
#     for row in apdata:
#         for ind in range(len(cross)):
#             if row[5] == cross[ind]:
#                 counts[ind] += 1
#
#     for ind in range(len(counts)):
#         if counts[ind] >= 10:
#             print cross[ind]
#             print counts[ind]
#
#
#         # if row[5] in petitioner:
#         #     count1 += 1
#         # elif row[5] in respondent:
#         #     count2 += 1
#         # elif row[5] in other:
#         #     count3 += 1
#         # elif row[5] in cross:
#         #     count4 += 1
#         # else:
#         #     pass
#     print count1
#     print count2
#     print count3
#     print count4
