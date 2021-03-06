import collaboration_data_processor as data
import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
from pylab import figure, show


def heatmap_month(locationlist, intensity):
    # x = ['6','7','8','9','10','11','12']
    x = [int(i) for x in range(31) for i in range(6,13)]
    y = [int(x) for x in range(1, len(locationlist)+1) for i in range(7)]
    intensity = [item for sublist in intensity for item in sublist]
    M = np.zeros((max(x) + 1, max(y) + 1))
    M[x, y] = intensity
    print(M)

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
    fig.savefig('plots/MonthLocationHeatMap.png', bbox_inches='tight')
    # and show it on the screen
    show()

def heatmap_hour(locationlist, intensity, month):
    x = [int(i) for x in range(31) for i in range(0,24)]
    y = [int(x) for x in range(1, len(locationlist)+1) for i in range(24)]
    intensity = [item for sublist in intensity for item in sublist]
    M = np.zeros((max(x) + 1, max(y) + 1))
    M[x, y] = intensity
    # print(M)

    fig, ax = plt.subplots()
    axes = plt.gca()
    axes.set_ylim([-0.5,23.5])
    axes.set_xlim([0.5,31.5])
    plt.title('Hours vs Location Overlap Frequencies')
    plt.ylabel('HOURS')
    plt.xlabel('LOCATION')
    ax.imshow(M)
    # show()

    # save to file
    fig.savefig('plots/HoursLocationHeatMap'+month+'.png', bbox_inches='tight')
    # and show it on the screen
    # show()

def plots():
    for i in range(6,13):
        intensity_hour, locationList = data.main3(str(i))
        heatmap_hour(locationList, intensity_hour, str(i))


def sumList(intensity, num):
    sumList = []
    for i in range(num):
        num = sum([sublist[i] for sublist in intensity])
        sumList.append(num)
    return sumList

def hour_list(intensity_hour):
    hourList = [0 for i in range(24)]
    for j in range(6,13):
        list = sumList(intensity_hour, 24)
        hourList = [hourList[k]+ list[k] for k in range(24)]
    return hourList

def collaboration_by_school(schools):
    schoolList = []
    for school in schools:
        length = data.main4(school)
        schoolList.append(length)
        print(length)

    y_pos = np.arange(len(schools))
    plt.bar(y_pos, schoolList, align = 'center', alpha = 0.5)
    plt.xticks(y_pos, ['HMC', 'POMONA', 'CMC', 'SCRIPPS', 'PITZER', 'CGU', 'KGI'])
    plt.ylabel("Number of Collaborations")
    plt.title("Number of Collaborations by Campus")

    # save to file
    plt.savefig('plots/CampusCollab.png', bbox_inches='tight')
    plt.show()


def percent_collaboration_school(schools):
    schoolList = []
    PopList = [829, 1660, 1347, 1057, 1089, 2261, 429]
    for i in range(len(schools)):
        length = 100*data.main4(schools[i])/(PopList[i])
        print(length)
        schoolList.append(length)

    y_pos = np.arange(len(schools))
    plt.bar(y_pos, schoolList, align = 'center', alpha = 0.5)
    plt.xticks(y_pos, ['HMC', 'POMONA', 'CMC', 'SCRIPPS', 'PITZER', 'CGU', 'KGI'])
    plt.ylabel("Percentage of Collaborations")
    plt.title("Number of Collaborations Normalized by Population of School")

    # save to file
    plt.savefig('plots/CampusCollabPercent.png', bbox_inches='tight')
    plt.show()

def cutoff(max_threshold):
    x = []
    y = []
    for i in range(max_threshold):
        UserD = data.main(i)
        num = len(UserD.keys())
        y.append(num)
        print(num)
        x.append(i)
    return x, y

def cutoffPlot(x, y):
    plt.plot(x,y,'.r-')
    plt.xlabel("Threshold")
    plt.ylabel("Number of Total Collaborations")
    plt.title("Number of Collaborations vs Threshold")

    # save to file
    plt.savefig('plots/cutoffPlot.png', bbox_inches='tight')
    plt.show()



#####################################
# Main Function for Plotting
#####################################
# intensity_month, locationList = data.main2()
# heatmap_month(locationList, intensity_month)
# plots()
# schools = ['hmc', 'pom', 'cmc', 'scr', 'pit', 'cgu', 'kgi']
# collaboration_by_school(schools)
# percent_collaboration_school(schools)
# y = [8777, 8777, 8748, 8711, 8665, 8630,8591, 8544,8504, 8455, 8400, 8144,
# 8002, 7985, 7967, 7956, 7940, 7929, 7913, 7900, 7883,7619, 7319,
# 7277,7236,7202,7169,7122, 7086, 7064,7043,6916, 6740,
# 6724, 6708, 6699, 6689, 6673, 6663, 6652, 6642, 6607,
# 6423, 6400, 6388,6378, 6370,6362, 6353,6345,6330]
# x = [i for i in range(0, 51)]
# cutoffPlot(x, y)
