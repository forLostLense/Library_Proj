import csv
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
from pylab import figure, show

# change the path to yours
directory = "/Users/IvyLiu/Desktop/Sorted_Data/"
def main():
    UserD = {}
    for root,dirs,files in os.walk(directory):
        for file in files:
           if file.endswith(".csv"):
               f=open(directory + file, 'r')
               filereader = csv.reader(f)
               listrows = list(filereader)
               rows = []
               for row in listrows:
                    if row[1] != "-":
                        rows.append(row)
               rows = rows[1:]
               UserD = findCollaboration(rows, UserD)
               f.close()
    return UserD


#modified main function for heatmap friendly data structure
def main2():
    List = []
    LocationList = []
    for root,dirs,files in os.walk(directory):
        for file in files:
            LocationList.append(file)
            UserD = {}
            if file.endswith(".csv"):
                f=open(directory + file, 'r')
                filereader = csv.reader(f)
                listrows = list(filereader)
                rows = []
                months = ['6','7','8','9','10','11','12']
                eachLocation = []
                for m in months:
                    for row in listrows:
                        if row[1] != "-" and row[5] == m:
                            rows.append(row)
                    rows = rows[1:]
                    UserD = findCollaboration(rows, UserD)
                    print(len(UserD))
                    eachLocation.append(len(UserD))
                    UserD = {}
                    rows = []
                print(eachLocation)
                List.append(eachLocation)
                f.close()
    # print(LocationList)
    print(List)
    # heatmap1(LocationList, List)
    return List, LocationList

# call this function from main
def heatmap1(locationlist, intensity):
    # x = ['6','7','8','9','10','11','12']
    x = [int(i) for x in range(31) for i in range(6,13)]
    y = [int(x) for x in range(1, len(locationlist)+1) for i in range(7)]
    intensity = [item for sublist in intensity for item in sublist]
    M = np.zeros((max(x) + 1, max(y) + 1))
    M[x, y] = intensity
    # print(M)

    fig, ax = plt.subplots()
    axes = plt.gca()
    axes.set_ylim([6.5,12.5])
    axes.set_xlim([0.5,31.5])
    plt.title('Month vs Location Overlap Frequencies')
    plt.ylabel('MONTH')
    plt.xlabel('LOCATION')
    ax.imshow(M)
    show()

    # save to file
    fig.savefig('MonthLocationHeatMap.png', bbox_inches='tight')
    # and show it on the screen
    show()

def calculateOverlap(dayStart1, hourStart1, minStart1, dayStart2, hourStart2, minStart2, dayEnd1, hourEnd1, minEnd1, dayEnd2, hourEnd2, minEnd2):
    # Number of minutes since midnight on person 1's start day.
    start1 = hourStart1 * 60 + minStart1
    start2 = (dayStart2 - dayStart1) * 24 * 60 + hourStart2 * 60 + minStart2
    lastStart = max(start1, start2)

    # Still number of minutes since midnight on person 1's start day
    end1 = (dayEnd1 - dayStart1) * 24 * 60 + hourEnd1 * 60 + minEnd1
    end2 = (dayEnd2 - dayStart1) * 24 * 60 + hourEnd2 * 60 + minEnd2
    firstEnd = min(end1, end2)

    overlap = firstEnd - lastStart
    return(overlap)

def findCollaboration(rows, UserD):
    for i in range(len(rows)):
        j = i
        while j < len(rows):
            iRow = rows[i]
            jRow = rows[j]
            overlap = calculateOverlap(int(iRow[6]), int(iRow[7]), int(iRow[8]), int(jRow[6]), int(jRow[7]), int(jRow[8]), int(iRow[11]), int(iRow[13]), int(iRow[14]), int(jRow[11]), int(jRow[13]), int(jRow[14]))
            if overlap > 30:
                # Add session to each user
                if iRow[1] in UserD:
                    iDict = UserD[iRow[1]]
                    if jRow[1] in iDict:
                        UserD[iRow[1]][jRow[1]].append(overlap)
                    else:
                        UserD[iRow[1]][jRow[1]] = [overlap]
                else:
                    UserD[iRow[1]] = {jRow[1]: [overlap]}

                if jRow[1] in UserD:
                    jDict = UserD[jRow[1]]
                    if iRow[1] in jDict:
                        UserD[jRow[1]][iRow[1]].append(overlap)
                    else:
                        UserD[jRow[1]][iRow[1]] = [overlap]
                else:
                    UserD[jRow[1]] = {iRow[1]: [overlap]}
            else:
                break
            j += 1
    return UserD


#####################################
# Test for overlap calculation
#####################################
# "","UUID","campus","WAPID","connect_year","connect_month","connect_day",
# "connect_hour","connect_minute","connect_dow","disconnect_month","disconnect_day","disconnect_year","disconnect_hour",
# # "disconnect_minute"
# iRow = ["1019","0ab358f3211fb7268c46b226dc6ad05e837cec862d89a5a57a0a08c51ec98ffc","cuc","CUC-HON-2-S-RTLS",2016,8,1,7,26,0,8,1,2016,10,33]
# jRow = ["1419","193b8bff00bdc347489961f3b3b0528ea37a30ceb8ae574bf4d9cc3b73a030b6","cuc","CUC-HON-2-S-RTLS",2016,8,1,7,42,0,8,1,2016,8,int("02")]
# print (overlap(iRow[6], iRow[7], iRow[8], jRow[6], jRow[7], jRow[8], iRow[11], iRow[13], iRow[14], jRow[11], jRow[13], jRow[14]))

locationlist = ['statsdata CUC-HON-2-S-RTLS .csv', 'statsdata CUC-HON-2-E-BRIDGE .csv', \
'statsdata CUC-HON-1-E-ELEVATOR .csv', 'statsdata CUC-HON-3-E-ASIAN_STUDIES .csv', \
'statsdata CUC-MUDD-3-S-KECK2 .csv', 'statsdata CUC-HON-2-S-HALL_BEHIND_ADMIN .csv', \
'statsdata CUC-HON-3-N-BOOK .csv', 'statsdata CUC-MUDD-1-W-MATERIALS_HANDLING .csv', \
'statsdata CUC-HON-2-N-WELCOME_DESK .csv', 'statsdata CUC-MUDD-2-NE .csv', \
'statsdata CUC-HON-3-W-ASIAN_STUDIES .csv', 'statsdata CUC-HON-1-W-CAFE .csv', \
'statsdata CUC-MUDD-3-N-IRIS .csv', 'statsdata CUC-MUDD-2-W .csv', \
'statsdata CUC-HON-3-NW-SITTING_AREA .csv', 'statsdata CUC-HON-1-S-CONNECTION .csv', \
'statsdata CUC-HON-2-W-CONFERENCE_ROOM .csv', 'statsdata CUC-HON-3-S-BOOK .csv', \
'statsdata CUC-HON-3-W-CENTER .csv', 'statsdata CUC-HON-4-NORTH .csv', \
'statsdata CUC-HON203-AP105-15 .csv', 'statsdata CUC-MUDD-1-W-ELEVATOR .csv', \
'statsdata CUC-HON-3-E-BRIDGE .csv', 'statsdata CUC-HON-2-S-STUDY_AREA .csv', \
'statsdata CUC-HON-1-N-CAFE .csv', 'statsdata CUC-HON-3-E-OUTSIDE_DC .csv', \
'statsdata CUC-HON-2-S-ADMIN_CONF_ROOM .csv', 'statsdata CUC-HON-4-EAST .csv', \
'statsdata CUC-MUDD-3-IRIS-N .csv', 'statsdata CUC-HON-1-NE-CAFE .csv', \
'statsdata CUC-HON-4-SOUTH .csv']


intensity = [[0, 0, 77, 194, 131, 161, 207], [0, 0, 206, 825, 760, 1000, 1075], [0, 0, 148, 659, 641, 765, 930], [0, 0, 41, 125, 116, 176, 261], [0, 0, 118, 371, 324, 462, 407], [0, 0, 14, 29, 24, 34, 47], [0, 0, 69, 297, 295, 407, 394], [0, 0, 28, 122, 150, 234, 370], [0, 0, 151, 733, 591, 637, 800], [0, 0, 134, 498, 511, 657, 780], [0, 0, 24, 110, 147, 171, 256], [0, 0, 225, 724, 789, 1032, 816], [0, 1, 40, 166, 223, 252, 267], [0, 0, 106, 503, 458, 535, 584], [0, 0, 73, 245, 262, 385, 346], [0, 0, 114, 285, 269, 314, 309], [0, 0, 58, 255, 254, 329, 315], [0, 1, 151, 516, 519, 705, 695], [0, 0, 75, 255, 294, 417, 514], [0, 0, 38, 132, 158, 180, 300], [0, 0, 30, 106, 107, 132, 152], [0, 0, 32, 116, 128, 200, 286], [0, 0, 156, 567, 531, 700, 741], [0, 0, 105, 839, 755, 881, 663], [0, 0, 127, 444, 452, 606, 636], [0, 0, 122, 453, 472, 554, 594], [0, 0, 58, 175, 208, 238, 317], [0, 0, 77, 348, 374, 453, 543], [0, 1, 39, 81, 71, 79, 62], [0, 0, 306, 960, 948, 1004, 943], [0, 0, 63, 185, 210, 282, 403]]

UserD = heatmap1(locationlist, intensity)

# with open('collaboration_dic.pickle', 'wb') as handle:
#     pickle.dump(UserD, handle, protocol=pickle.HIGHEST_PROTOCOL)

#####################################
# To load pickle
#####################################
with open('collaboration_dic.pickle', 'rb') as handle:
    b = pickle.load(handle)

#print (len(UserD.keys()))
