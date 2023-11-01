import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

#CSV variables to remember
file = ''
flowColumn = ''
dayColumn = ''
df = ''

#Requesting file from user until viable file provided
while True:
    file = input("\nEnter csv name (including '.csv'): ")
    try:
        data = pd.read_csv(file, converters={flowColumn:float})
        df = pd.DataFrame(data)
        break
    except FileNotFoundError:
        print("\n***Error reading the CSV file*** \n(Make sure it is spelled correctly and in the same directory as this executable if not using relative/direct path.)")

    
#Collecting details on csv
while True:
    elevColumn = input("\nEnter name of elevation column (be mindful of capital letters): ")
    if elevColumn in df.columns:
        print("Column '" + elevColumn + "' selected.")
        break
    else:
        print("\n***This is not a column in the given csv***")
        print("\nColumns in the csv: ")
        for column in df.columns:
            print("'" + column + "'")

#Accepted date formats
date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y%m%d", "%d-%m-%Y", "%Y/%m/%d", "%m/%d/%Y %H:%M"]

formatAccepted = False

while True:
    dayColumn = input("\nEnter name of the time column (be mindful of capital letters): ")
    if dayColumn in df.columns:
        print("Column '" + dayColumn + "' selected.")
        for format in date_formats:
            try:
                df[dayColumn] = pd.to_datetime(df[dayColumn], format = format)
                formatAccepted = True
                break
            except ValueError:
                pass
        if formatAccepted == True:
            break
        else:
            print("***Error: This column is not in a recognized date format.***")
    else:
        print("\n***This is not a column in the given csv***")
        print("\nColumns in the csv: ")
        for column in df.columns:
            print("'" + column + "'")

#Prompting the user to decide between default ranges and unique ranges
print("\nDefault ranges are: 2.6ft (normal), 1.5ft (monitor), 2ft (minor), 3ft (moderate), 3.5ft (major)")
while True:
    specify = input("Specify ranges? (y/n): ")
    if specify == 'y':
        break
    elif specify == 'n':
        print("Default ranges selected.")
        break
    else:
        print("Invalid input.")      

#prompts user to specify ranges until they are finished 
if specify == 'y':
    #list to keep track of ranges
    ranges = []
    rangeCount = 1
    adding = True

    while adding == True:
        while True:
            start = input("\nEnter start of range " + str(rangeCount) + ": ")
            if not start.strip():
                print("Start cannot be empty.")
            else:
                try:
                    number = float(start)
                    break
                except ValueError:
                    try:
                        number = float(start)
                        break
                    except ValueError:
                        print("Start must be a number.")
                    
        while True:
            end = input("Enter end of range " + str(rangeCount) + ": ")
            if not end.strip():
                print("End cannot be empty.")
            else:
                try:
                    number = float(end)
                    break
                except ValueError:
                    try:
                        number = float(end)
                        break
                    except ValueError:
                        print("End must be a number.")
        
        if float(start) >= float(end):
            print("\nStart cannot be larger than or equal to end value. Range not added.")
                
        else:
            ranges.append((start, end))
            print("Range " + str(rangeCount) + " added: " + str(start) + " - " + str(end) + ".")
            while True:
                another = input("\nAdd another range? (y/n): ")
                if another == 'n':
                    adding = False
                    break
                elif another == 'y':
                    rangeCount+=1
                    break
                else:
                    print("Invalid input.")
else:
    #ranges will be set to defaults
    print("Ranges will be set to defaults.")
    ranges = [(-2, 1.5), (1.5, 2), (2, 3), (3, 3.5)]

#print ranges
print("\nYour ranges: ")
for t in ranges:
    print(t)


#Start of process
print("\nWorking...")


######################DATA ANALYSIS###############################

#Creating a dictionary to store dataframes. Range dataframe can be accessed by range#_#df
rangeDataFrames = {}

#Adding a dataframe for each range to list. Using default ranges if not specified. 
for r in ranges:
    dictName = "range" + str(r[0]) + "_" + str(r[1])
    dic = {
        'Day' : [],
        'Flow' : [],
        }
    dfRangeName = dictName + "df"
    dfRange = pd.DataFrame(dic)
    rangeDataFrames[dfRangeName] = dfRange


#New row function
x = 0
def new_row(dataFrame, elev):
    new_row = {'Day': df[dayColumn][x], 'Elev': elev}
    return new_row


#Sorting all of the elevations in the elevation column floato specified ranges
i = 0
while i < (len(df[elevColumn])):
    for r in ranges:
        dictName = "range" + str(r[0]) + "_" + str(r[1])
        dfRangeName = dictName + "df"

        if float(df[elevColumn][i]) >= float(r[0]):
            if df[elevColumn][i] >= float(r[0]) and df[elevColumn][i] <= float(r[1]):
                new_row = {'Day': df[dayColumn][i], 'Flow': df[elevColumn][i]}
                rangeDataFrames[dfRangeName] = pd.concat([rangeDataFrames[dfRangeName], pd.DataFrame([new_row])], ignore_index=True)
                break
        
    i += 1

print(rangeDataFrames)
    
#Consecutive day count function
def flow_duration(range, instance):
    print("\n FLOW DURATION")
    i = 0
    curr = i
    nex = i + 1

    rangeDF = rangeDataFrames[range]
    instanceDF = instDataFrames[instance]

    while i < (len(rangeDF['Day']) - 1):
        consecutive = True
        duration = 1

        while consecutive == True:
            if nex == len(rangeDF):
                consecutive = False
                new_row = {'dayStart': rangeDF['Day'][i], 'duration': duration}
                instanceDF = pd.concat([instanceDF, pd.DataFrame([new_row])], ignore_index=True)
                i = curr
                return instanceDF
            else:
                oneDay = timedelta(days=1)
                if (((rangeDF['Day'][nex].day) - 1) == (rangeDF['Day'][curr].day)):
                    consecutive = True
                    duration += 1
                    curr += 1
                    nex += 1
                else:
                    consecutive = False
                    new_row = {'dayStart': rangeDF['Day'][i], 'duration': duration}
                    instanceDF = pd.concat([instanceDF, pd.DataFrame([new_row])], ignore_index=True)
                    curr += 1
                    nex += 1
                    i = curr
    print(instanceDF)
    return instanceDF

#Creating a dictionary to store instance dataframes. Instance dataframe can be accessed by instances#_#
instDataFrames = {}

#Adding a dataframe for each range to the instance df list. Using default ranges if not specified. 
for r in ranges:
    dictName = "instances" + str(r[0]) + "_" + str(r[1])
    dic = {
        'dayStart' : [],
        'duration' : [],
        }
    dfInst = pd.DataFrame(dic)
    instDataFrames[dictName] = dfInst
    print("INSTANCE")
    print(dictName)
    print(dfInst)

print(instDataFrames)


#Taking note of consecutive days of flow at each rate and adding to corresponding instance dataframe 
for r in ranges:
    rangeDFName = "range" + str(r[0]) + "_" + str(r[1]) + "df"
    
    if len(rangeDataFrames[rangeDFName]) > 0:
        instDFName = "instances" + str(r[0]) + "_" + str(r[1])
        rangeDFName = "range" + str(r[0]) + "_" + str(r[1]) + "df"
        instDataFrames[instDFName] = flow_duration(rangeDFName, instDFName)

        print("\n")
        print(instDataFrames[instDFName])
        print()

        

#Creating a dictionary to store instance dataframes. Instance dataframe can be accessed by instances#_#
tupleLists = {}

#Tuple creation for consecutive days
for r in ranges:
    listName = "tuples" + str(r[0]) + "_" + str(r[1])
    tupleList = []
    

    instDFName = "instances" + str(r[0]) + "_" + str(r[1])
    inst = instDataFrames[instDFName]

    print("INST DATA FRAMES: ")
    print(instDataFrames)

    for i in range(len(inst)):
        durationTime = timedelta(days = (inst['duration'][i]))
        new_tuple = (inst['dayStart'][i], inst['dayStart'][i] + durationTime)
        tupleList.append(new_tuple)
    
    tupleLists[listName] = tupleList

################ GRAPH SETUP ################ 

#creating month x-axis labelse
months = []
months.append(df[dayColumn][0])
monthDate = df[dayColumn][0]

oneMonth = relativedelta(months=1)

for date in df[dayColumn]:
    if date.month != monthDate.month:
        months.append(date)
        monthDate += oneMonth

monthDate += oneMonth
months.append(monthDate)

monthLabels = []
for m in months:
    monthLabels.append(m.strftime("%b"))


xtick_positions = months  # Define the Y-axis tick positions
xtick_labels = monthLabels # Define the labels for the tick positions

#Creating range y-axis labels
ytick_positions = []
ytick_labels = []

for r in ranges:
    ytick_positions.append(r[0])
    ytick_positions.append(r[1])
    ytick_labels.append(str(r[0]))
    ytick_labels.append(str(r[1]))

#Adding a folder to hold the graphs
new_folder_name = "Graphs"
count = 0

#This method creates a new folder every time
'''
while True:
    # Check if the directory exists
    if not os.path.exists(new_folder_name):
        # If it doesn't exist, create the new directory
        os.mkdir(new_folder_name)
        break
    else:
        count += 1
        new_folder_name = "Graphs (" + str(count) + ")"
'''

#This method overwrites the same folder
os.mkdir(new_folder_name)

################ PRODUCT CREATION ################ 

#Average Daily Flow Over a Year Graph Display
def avgDailyFlow(): 
    #Graph cration
    plt.figure(figsize=(8, 6))
    
    #Data definition
    plt.plot(df[dayColumn], df[elevColumn], color='blue', zorder = 2, linestyle = '-')
    
    #Labels
    plt.title("Water Surface Elevation Over Time")
    plt.xlabel("Month")
    plt.ylabel("Elevation (ft)")
    plt.xticks(months, monthLabels)
    plt.yticks(ytick_positions, ytick_labels)

    #Adding lines at ranges
    for r in ranges:
        plt.axhline(y=float(r[0]), color='white', linestyle='--', label='Horizontal Line at y=0', zorder=1)
        plt.axhline(y=float(r[1]), color='white', linestyle='--', label='Horizontal Line at y=0', zorder = 1)

    #limits
    plt.xlim(months[0], months[len(months) - 1])
    plt.ylim(float(ranges[0][0]), float(ranges[len(ranges) - 1][1]))

    plot_filename = os.path.join(new_folder_name, "Elevation Over Time.png")
    #plt.savefig(plot_filename)

    plt.show()

    #Duration Table Creation 
    print(instDataFrames)
        