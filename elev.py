import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import shutil
from tabulate import tabulate

#CSV variables to remember
file = ''
elevColumn = ''
dayColumn = ''
df = ''

#Requesting file from user until viable file provided
while True:
    file = input("\nEnter csv name (including '.csv'): ")
    try:
        data = pd.read_csv(file, converters={elevColumn:float})
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
'''
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
'''
#else:
#ranges will be set to defaults
#print("Ranges will be set to defaults.")
ranges = [(-2, 1.5), (1.5, 2), (2, 3), (3, 3.5)]

#print ranges
print("\nYour ranges: ")
for t in ranges:
    print(t)


#Start of process
print("\nWorking...")


######################DATA ANALYSIS###############################

#Properly Filtering DataFrame. Groups by hour and takes assigns the mean for each hour. 
df = df.groupby(pd.Grouper(freq='60min', key='Reading')).mean(numeric_only=True).round(2).dropna().reset_index()

#Creating a dictionary to store dataframes. Range dataframe can be accessed by range#_#df
rangeDataFrames = {}

#Adding a dataframe for each range to list. Using default ranges if not specified. 
for r in ranges:
    dictName = "range" + str(r[0]) + "_" + str(r[1])
    dic = {
        'Day' : [],
        'Elev' : [],
        }
    dfRangeName = dictName + "df"
    dfRange = pd.DataFrame(dic)
    rangeDataFrames[dfRangeName] = dfRange

#Sorting all of the elevations in the elevation column floato specified ranges
i = 0
print(df.columns)
while i < (len(df[elevColumn])):
    for r in ranges:
        dictName = "range" + str(r[0]) + "_" + str(r[1])
        dfRangeName = dictName + "df"

        if float(df[elevColumn][i]) >= float(r[0]):
            if df[elevColumn][i] >= float(r[0]) and df[elevColumn][i] <= float(r[1]):
                new_row = {'Day': df[dayColumn][i], 'Elev': df[elevColumn][i]}
                rangeDataFrames[dfRangeName] = pd.concat([rangeDataFrames[dfRangeName], pd.DataFrame([new_row])], ignore_index=True)
                break
        
    i += 1
    
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
            #print("nex: " + str(nex) + ", len(rangeDF): " + str(len(rangeDF)))
            if nex == len(rangeDF):
                print("REACHED THE END OF RANGE DF")
                consecutive = False
                new_row = {'dayStart': rangeDF['Day'][i], 'duration': duration, 'elev': rangeDF['Elev'][i]}
                instanceDF = pd.concat([instanceDF, pd.DataFrame([new_row])], ignore_index=True)
                i = curr
                return instanceDF
            else:
                if ((rangeDF['Day'][nex] - rangeDF['Day'][curr]) <= timedelta(hours=1)):
                    #print("CONSECUTIVE HOUR")
                    consecutive = True
                    duration += 1
                    curr += 1
                    nex += 1
                    
                else:
                    print("NON CONSECUTIVE HOUR")
                    consecutive = False
                    new_row = {'dayStart': rangeDF['Day'][i], 'duration': duration, 'elev': rangeDF['Elev'][+i]}
                    instanceDF = pd.concat([instanceDF, pd.DataFrame([new_row])], ignore_index=True)
                    curr += 1
                    nex += 1
                    i = curr

    return instanceDF

#Creating a dictionary to store instance dataframes. Instance dataframe can be accessed by instances#_#
instDataFrames = {}

#Adding a dataframe for each range to the instance df list. Using default ranges if not specified. 
for r in ranges:
    dictName = "instances" + str(r[0]) + "_" + str(r[1])
    dic = {
        'dayStart' : [],
        'duration' : [],
        'elev': []
        }
    dfInst = pd.DataFrame(dic)
    instDataFrames[dictName] = dfInst


#Taking note of consecutive days of flow at each rate and adding to corresponding instance dataframe 
for r in ranges:
    rangeDFName = "range" + str(r[0]) + "_" + str(r[1]) + "df"
    
    if len(rangeDataFrames[rangeDFName]) > 0:
        instDFName = "instances" + str(r[0]) + "_" + str(r[1])
        rangeDFName = "range" + str(r[0]) + "_" + str(r[1]) + "df"
        
        instDataFrames[instDFName] = flow_duration(rangeDFName, instDFName)

        days = []

        for d in instDataFrames[instDFName]['duration']:
            days.append(round(d / 24, 1))
        
        instDataFrames[instDFName]['Duration in Days'] = days

#Creating a dictionary to store instance dataframes. Instance dataframe can be accessed by instances#_#
tupleLists = {}

#Tuple creation for consecutive days
for r in ranges:
    listName = "tuples" + str(r[0]) + "_" + str(r[1])
    tupleList = []
    

    instDFName = "instances" + str(r[0]) + "_" + str(r[1])
    inst = instDataFrames[instDFName]

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

#Creating range y-axis labels
ytick_positions = []
ytick_labels = []

for r in ranges:
    ytick_positions.append(r[0])
    ytick_positions.append(r[1])
    ytick_labels.append(str(r[0]))
    ytick_labels.append(str(r[1]))

################ PRODUCT CREATION ################ 

#Average Daily Flow Over a Year Graph Display
def avgDailyFlow(): 
    #Graph cration
    plt.figure(figsize=(20, 6))
    
    #Data definition
    plt.plot(df[dayColumn], df[elevColumn], color='blue', zorder = 2, linestyle = '-')
    
    #Labels
    plt.title("Water Surface Elevation Over Time")
    if relativedelta(df[dayColumn][len(df)- 1], df[dayColumn][0]).months > 1:
        plt.xlabel("Month")
    else:
        plt.xlabel("Day")
    plt.ylabel("Elevation (ft)")
    #plt.xticks(months, monthLabels)
    plt.yticks(ytick_positions, ytick_labels)

    #Adding lines at ranges
    for r in ranges:
        plt.axhline(y=float(r[0]), color='grey', linestyle='--', label='Horizontal Line at y=0', zorder=1)
        plt.axhline(y=float(r[1]), color='grey', linestyle='--', label='Horizontal Line at y=0', zorder = 1)

    #limits
    plt.xlim(months[0], df[dayColumn].max())

    #if the max data point is higher than the specified range, use the max as the limit
    #else, use the specified range as the limit
    if df[elevColumn].max() >= float(ranges[len(ranges) - 1][1]):
        if df[elevColumn].min() > float(ranges[0][0]):
            plt.ylim(float(ranges[0][0]), df[elevColumn].max())
        else:
            plt.ylim(float(ranges[0][0]), df[elevColumn].max())
    elif df[elevColumn].max() < float(ranges[len(ranges) - 1][1]):
        if df[elevColumn].min() > float(ranges[0][0]):
            plt.ylim(float(ranges[0][0]), float(ranges[len(ranges) - 1][1]))
        else:
            plt.ylim(float(ranges[0][0]), float(ranges[len(ranges) - 1][1]))



    plot_filename = os.path.join(new_folder_name, "Elevation Over Time.png")
    plt.savefig(plot_filename)

    plt.show()

################## Executing Map and CSV ##################
#displaying all elevation over time

new_folder_name = "elev_analysis"
count = 0

while True:

    folder_path = os.path.join(os.getcwd(), new_folder_name)

    # Check if the directory exists
    if not os.path.exists(folder_path):
        # If it doesn't exist, create the new directory
        os.mkdir(folder_path)
        break
    else:
        count += 1
        new_folder_name = "elev_analysis (" + str(count) + ")"

for r in ranges:
    instDFName = "instances" + str(r[0]) + "_" + str(r[1])
    inst = instDataFrames[instDFName]

    if len(inst) > 0:
        print(inst)
        csv_path = os.path.join(folder_path, str(r[0]) + " to " + str(r[1]) + " ft.csv")
        inst.to_csv(csv_path)

avgDailyFlow()

