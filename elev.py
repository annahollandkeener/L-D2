import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
import shutil

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
date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y%m%d", "%d-%m-%Y", "%Y/%m/%d", "%m/%d/%Y %H:%M", "%m/%d/%Y %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"]

formatAccepted = False

while True:
    dayColumn = input("\nEnter name of the time column (be mindful of capital letters): ")
    if dayColumn in df.columns:
        print("Column '" + dayColumn + "' selected.")
        for format in date_formats:
            try:
                df[dayColumn] = pd.to_datetime(df[dayColumn], format = format)
                dateType = date_formats.index(format)
                formatAccepted = True
                break
            except ValueError:
                print('passed')
                pass
        if formatAccepted == True:
            break
        else:
            print("\n***Error: This column is not in a recognized date format***")
            print("Accepted formats include: \n")
            for format in date_formats:
                print(format)

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
#ranges = [(-2, 1.5), (1.5, 2), (2, 3), (3, 3.5)]
ranges = [(0, 5), (5, 10), (10, 15), (15, 20)]

#print ranges
print("\nYour ranges: ")
for t in ranges:
    print(t)


#Start of process
print("\nWorking...")

print(df[dayColumn].dtype)
print(df.columns)
print(df)


######################DATA ANALYSIS###############################

#Properly Filtering DataFrame.
#Groups by hour and takes assigns the mean for each hour. 
dateTypes = ['year', 'month', 'day', 'hour', 'minute']
try:
    df[dayColumn][0].year
    increment = 'year'
except AttributeError:
    try:
        df[dayColumn][0].month
        increment = 'month'
    except:
        try:    
            df[dayColumn][0].day
            increment = 'day'
        except AttributeError:
            try:
                df[dayColumn][0].hour
                increment = 'hour'
            except AttributeError:
                try:
                    df[dayColumn][0].minute
                    increment = 'minute'
                except:
                    try:
                        df[dayColumn][0].second
                        increment = 'second'
                    except:
                        print("***Warning: Timestamp interval too large. Results will likely be inaccurate.***")
                    



                    
print(dateType)
print(df[dayColumn].dtypes)
df = df.groupby(pd.Grouper(freq='60min', key=dayColumn)).mean(numeric_only=True).round(2).dropna().reset_index()

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
                consecutive = False
                new_row = {'dayStart': rangeDF['Day'][i], 'duration': duration, 'elev': rangeDF['Elev'][i]}
                instanceDF = pd.concat([instanceDF, pd.DataFrame([new_row])], ignore_index=True)
                i = curr
                return instanceDF
            else:
                if ((rangeDF['Day'][nex] - rangeDF['Day'][curr]) <= timedelta(days=1)):
                    #print("CONSECUTIVE HOUR")
                    consecutive = True
                    duration += 1
                    curr += 1
                    nex += 1
                else:
                    consecutive = False
                    new_row = {'dayStart': rangeDF['Day'][i], 'duration': duration, 'elev': rangeDF['Elev'][i]}
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
            days.append(round(d // 24, 0))
        
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

#Adding ticks at min and max values of data
ytick_positions.append(df[elevColumn].min())
ytick_positions.append(df[elevColumn].max())
ytick_labels.append(str(df[elevColumn].min()) + ' (min)')
ytick_labels.append(str(df[elevColumn].max()) + ' (max)')



################ PRODUCT CREATION ################ 

#Average Daily Flow Over a Year Graph Display
def avgDailyFlow(): 
    #Graph cration
    plt.figure(figsize=(20, 6))
    
    #Data definition
    plt.plot(df[dayColumn], df[elevColumn], color='#424242', zorder = 2, linestyle = '-')
    
    #Labels
    plt.title("Elevation Over Time")
    if relativedelta(df[dayColumn][len(df)- 1], df[dayColumn][0]).months > 1:
        plt.xlabel("Month")
    elif relativedelta(df[dayColumn][len(df)- 1], df[dayColumn][0]).years > 1:
        plt.xlabel("Year")
    else:
        plt.xlabel("Day")

    plt.ylabel("Elevation (ft)")
    #plt.xticks(months, monthLabels)
    plt.yticks(ytick_positions, ytick_labels)

    #limits
    plt.xlim(df[dayColumn].min(), df[dayColumn].max())

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

    #Adding lines at ranges
    for r in ranges:
        plt.axhline(y=float(r[0]), color='grey', linestyle='--', label='Horizontal Line at y=0', zorder=1)
        plt.axhline(y=float(r[1]), color='grey', linestyle='--', label='Horizontal Line at y=0', zorder = 1)

    #Adds a horizontal line at the top of the graph 
    if df[elevColumn].max() < float(ranges[len(ranges) - 1][1]):
        plt.axhline(y=float(ranges[len(ranges) - 1][1]), color='grey', linestyle='--', label='Horizontal Line at y=0', zorder = 1)
    else:
        plt.axhline(y=df[elevColumn].max(), color='grey', linestyle='--', label='Horizontal Line at y=0', zorder = 1)


    #start color
    red = 197/255
    green = 247/255
    blue = 158/255
 
    #Establishing where the bottom of the graph starts
    if df[elevColumn].min() > float(ranges[0][0]):
        bottom = float(ranges[0][0])
    else:
        bottom = df[elevColumn].min()

    #Establishing where the top of the graph starts
    if df[elevColumn].max() >= float(ranges[len(ranges) - 1][1]):
        top = df[elevColumn].max()
    else:
        top = float(ranges[len(ranges) - 1][1])

    #Coloring between each range, making more red as goes up 
    for r in ranges:
        if r == ranges[0]:
            plt.fill_between(df[dayColumn], bottom, r[1], color= (197/255, 247/255, 158/255), alpha=0.5, label='Shaded Area')
        elif r == ranges[len(ranges) - 1]:
            plt.fill_between(df[dayColumn], r[0], top, color= (247/255, 158/255, 158/255), alpha=0.5, label='Shaded Area')
        else:
            if red < 247/255:
                red += 25/255
            else:
                green -= 25/255
            plt.fill_between(df[dayColumn], r[0], r[1], color= (red, green, blue), alpha=0.5, label='Shaded Area')


    #Putting graph in folder
    plot_filename = os.path.join(new_folder_name, "Elevation Over Time.png")
    plt.savefig(plot_filename)

    plt.show()

################## Executing Map and CSV ##################
#displaying all elevation over time

new_folder_name = "elev_analysis"
count = 0

#Creating a folder to put outputs in 
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
        csv_path = os.path.join(folder_path, str(r[0]) + " to " + str(r[1]) + " ft.csv")
        inst.to_csv(csv_path, index = False)

avgDailyFlow()
print("MAX: ")
print(df[elevColumn].max())

