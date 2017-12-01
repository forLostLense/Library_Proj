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
#####################################
# Main Function for Plotting
#####################################
# intensity_month, locationList = data.main2()
# sum_of_month(intensity_month)
# heatmap_month(locationList, intensity_month)
# print(data.main3(9))
# plots()
