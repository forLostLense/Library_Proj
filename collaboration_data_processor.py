import csv
import os
import pickle
import numpy

# change the path to yours
directory = "/Users/Aivilo Sniktaw/Documents/School/Junior Year/Stats/Library_Proj/csv_location/"
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
        i = 0
        for file in files:

            if i > 5:
                break
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
            i += 1
    # print(LocationList)
    # print(List)
    return List, LocationList

def main3(month):
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
                hours = [str(n) for n in range(0,24)]
                eachLocation = []
                for t in hours:
                    for row in listrows:
                        if row[1] != "-" and row[5] == str(month) and row[7] == t:
                            rows.append(row)
                        elif t== 0 and row[7] == 24:
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
    return List, LocationList

# returns a list of number of collaborations per school
def main4(school):
    for root,dirs,files in os.walk(directory):
        for file in files:
            UserD = {}
            if file.endswith(".csv"):
                f=open(directory + file, 'r')
                filereader = csv.reader(f)
                listrows = list(filereader)
                rows = []
                for row in listrows:
                    if row[1] != "-" and row[2] == str(school):
                        rows.append(row)
                rows = rows[1:]
                UserD = findCollaboration(rows, UserD)
                f.close()
    return len(UserD)

# call this function from main
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

def isLater(day1, hour1, min1, day2, hour2, min2):
    if day2 > day1:
        return True

    if day1 > day2:
        return False

    if hour2 > hour1:
        return True

    if hour1 > hour2:
        return False

    if min2 > min1:
        return True

    return False



def findCollaboration(rows, UserD):
    print("collab")
    for i in range(len(rows)):
        if i % 100 == 0:
            print(i)
        j = i+1
        while j < len(rows):
            iRow = rows[i]
            jRow = rows[j]

            if iRow[1] == jRow[1]:
                j += 1
                continue

            # compare end time of first and start time of second
            if isLater(int(jRow[10]), int(jRow[7]), int(jRow[8]), int(iRow[16]), int(iRow[14]), int(iRow[15])):
                break

            overlap = calculateOverlap(int(iRow[6]), int(iRow[7]), int(iRow[8]), int(jRow[6]), int(jRow[7]), int(jRow[8]), int(iRow[12]), int(iRow[14]), int(iRow[15]), int(jRow[12]), int(jRow[14]), int(jRow[15]))
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

            j += 1
    return UserD


def getUserMap(d, sessionCutoff, timeCutoff):
    collaborators = list(d.keys())
    print("COLLABORATORS", len(d))
    overlaps = numpy.zeros(shape=(len(d), len(d)))
    numCollabs = numpy.zeros(shape=(len(d), 1))
    for i in range(len(collaborators)):
        if i % 1000 == 0:
            print("LOOPIN'", i)
        for j in range(i+1, len(collaborators)):
            iDict = d[collaborators[i]]
            if collaborators[j] in iDict:
                ijList = iDict[collaborators[j]]
                if len(ijList) >= sessionCutoff:
                    overlapTime = sum(ijList)
                    if overlapTime >= timeCutoff:
                        #print("Got one!", overlapTime)
                        overlaps[i, j] = overlapTime
                        overlaps[j, i] = overlapTime
                        numCollabs[i] += 1
                        numCollabs[j] += 1
    print(len(overlaps))
    print(overlaps)
    overlaps = overlaps[~numpy.all(overlaps==0, axis=1)]
    print(len(overlaps))
    return (overlaps, numCollabs)





def main4():
    d = getDict()
    print("starting")
    return getUserMap(d, 3, 120)

#####################################
# Test for overlap calculation
#####################################
# "","UUID","campus","WAPID","connect_year","connect_month","connect_day",
# "connect_hour","connect_minute","connect_dow","disconnect_month","disconnect_day","disconnect_year","disconnect_hour",
# # "disconnect_minute"
# iRow = ["1019","0ab358f3211fb7268c46b226dc6ad05e837cec862d89a5a57a0a08c51ec98ffc","cuc","CUC-HON-2-S-RTLS",2016,8,1,7,26,0,8,1,2016,10,33]
# jRow = ["1419","193b8bff00bdc347489961f3b3b0528ea37a30ceb8ae574bf4d9cc3b73a030b6","cuc","CUC-HON-2-S-RTLS",2016,8,1,7,42,0,8,1,2016,8,int("02")]
# print (overlap(iRow[6], iRow[7], iRow[8], jRow[6], jRow[7], jRow[8], iRow[11], iRow[13], iRow[14], jRow[11], jRow[13], jRow[14]))

# UserD = main()
# with open('collaboration_dic.pickle', 'wb') as handle:
#     pickle.dump(UserD, handle, protocol=pickle.HIGHEST_PROTOCOL)

#####################################
# To load pickle
#####################################
def getDict():
    with open('collaboration_dic.pickle', 'rb') as handle:
        b = pickle.load(handle)
        return b

#print (len(UserD.keys()))


#overlaps, numCollabs = main4()
# with open('collaboration_dic.pickle', 'rb') as handle:
#     b = pickle.load(handle)

# print (len(UserD.keys()))