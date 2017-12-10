import csv
import os
import pickle

# change the path to yours
directory = "/Users/IvyLiu/Desktop/Sorted_Data/"
def main(threshold):
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
               UserD = findCollaboration(rows, UserD, threshold)
               f.close()
    return UserD


#modified main function for heatmap friendly data structure
def main2():
    List = []
    LocationList = []
    for root,dirs,files in os.walk(directory):
        for file in files:
            UserD = {}
            if file.endswith(".csv"):
                LocationList.append(file)
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
                    UserD = findCollaboration(rows, UserD, 30)
                    print(len(UserD))
                    eachLocation.append(len(UserD))
                    UserD = {}
                    rows = []
                print(eachLocation)
                List.append(eachLocation)
                f.close()

    return List, LocationList

def main3(month):
    List = []
    LocationList = []
    for root,dirs,files in os.walk(directory):
        for file in files:
            UserD = {}
            if file.endswith(".csv"):
                LocationList.append(file)
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
                    UserD = findCollaboration(rows, UserD, 30)
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
                UserD = findCollaboration(rows, UserD, 30)
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

def findCollaboration(rows, UserD, threshold):
    for i in range(len(rows)):
        j = i
        while j < len(rows):
            iRow = rows[i]
            jRow = rows[j]
            if iRow[1] == jRow[1]:
                j += 1
                continue
            overlap = calculateOverlap(int(iRow[6]), int(iRow[7]), int(iRow[8]), int(jRow[6]), int(jRow[7]), int(jRow[8]), int(iRow[11]), int(iRow[13]), int(iRow[14]), int(jRow[11]), int(jRow[13]), int(jRow[14]))
            if overlap > threshold:
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
# UserD = main(30)
# with open('collaboration_dic.pickle', 'wb') as handle:
#     pickle.dump(UserD, handle, protocol=pickle.HIGHEST_PROTOCOL)

#####################################
# To load pickle
#####################################
# with open('collaboration_dic.pickle', 'rb') as handle:
#     b = pickle.load(handle)

# print (len(UserD.keys()))
