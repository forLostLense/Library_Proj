import csv
import os 
directory = "/Users/yvenica/Desktop/Library_Proj/sorted_data/"

for root,dirs,files in os.walk(directory):
    for file in files:
       if file.endswith(".csv"):
           f=open(directory + file, 'r')
           print ("yes")
           f.close()