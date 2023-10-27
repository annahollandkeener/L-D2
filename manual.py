import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

import stylefile

#CSV variables to remember
file = ''
flowColumn = ''
dayColumn = ''
df = ''

types = ['flow', 'elevation']
dataType = ''

while True: 
    print("\nData Types Expected")
    print("------------")
    for t in types:
        print("|'" + t + "'")
    print("------------")
    print("\nType 'types' for a description of each mode.")

    response = input("Select type: ")

    if response.lower() == 'types':
        print("\nDescription...")
    elif response.lower() == 'flow':
        print("\nFlow data selected.")
        dataType = response.lower()
        break 
    elif response.lower() == 'elevation':
        print("\nElevation data selected.")
        dataType = response.lower()
        break
    else:
        "Invalid input."

#Manual data entry mode


#Requesting file from user until viable file provided
while True:
    file = input("\nEnter csv name (including '.csv'): ")
    try:
        data = pd.read_csv(file, converters={flowColumn:int})
        df = pd.DataFrame(data)
        break
    except FileNotFoundError:
        print("\n***Error reading the CSV file*** \n(Make sure it is spelled correctly and in the same directory as this executable if not using relative/direct path.)")

    
#Collecting details on csv
while True:
    flowColumn = input("\nEnter name of flow column (be mindful of capital letters): ")
    if flowColumn in df.columns:
        print("Column '" + flowColumn + "' selected.")
        break
    else:
        print("\n***This is not a column in the given csv***")
        print("\nColumns in the csv: ")
        for column in df.columns:
            print("'" + column + "'")

date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y%m%d", "%d-%m-%Y", "%Y/%m/%d"]

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
print("\nDefault ranges are: 0-1500, 1500-3500, 3500-7500, 7500-10000, >10000")
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
                    number = int(start)
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
                    number = int(end)
                    break
                except ValueError:
                    try:
                        number = float(end)
                        break
                    except ValueError:
                        print("End must be a number.")
        
        if int(start) >= int(end):
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
    ranges = [(0,1500), (1500,3500), (3500, 7500), (7500, 10000), (10000, 50000)]

#print ranges
print("\nYour ranges: ")
for t in ranges:
    print(t)

while True:
    colors = ['basic', 'spectral']
    color = input("\nPlease select display option ('basic' or 'spectral'): ")

    if color in colors:
        break
    else:
        print("***Invalid input***")


#Start of process
print("\nWorking...")




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
def new_row(dataFrame, flow):
    new_row = {'Day': df[dayColumn][x], 'Flow': flow}
    return new_row


#Sorting all of the flows in the flow column into specified ranges
i = 0
while i < (len(df[flowColumn])):
    for r in ranges:
        dictName = "range" + str(r[0]) + "_" + str(r[1])
        dfRangeName = dictName + "df"

        if int(df[flowColumn][i]) >= int(r[0]):
            if df[flowColumn][i] >= int(r[0]) and df[flowColumn][i] <= int(r[1]):
                new_row = {'Day': df[dayColumn][i], 'Flow': df[flowColumn][i]}
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
            if nex == len(rangeDF):
                consecutive = False
                new_row = {'dayStart': rangeDF['Day'][i], 'duration': duration}
                instanceDF = pd.concat([instanceDF, pd.DataFrame([new_row])], ignore_index=True)
                i = curr
                return instanceDF
            else:
                oneDay = timedelta(days=1)
                if (((rangeDF['Day'][nex]) - oneDay) == (rangeDF['Day'][curr])):
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


#Taking note of consecutive days of flow at each rate and adding to corresponding instance dataframe 
for r in ranges:
    rangeDFName = "range" + str(r[0]) + "_" + str(r[1]) + "df"
    
    if len(rangeDataFrames[rangeDFName]) > 0:
        instDFName = "instances" + str(r[0]) + "_" + str(r[1])
        rangeDFName = "range" + str(r[0]) + "_" + str(r[1]) + "df"
        instDataFrames[instDFName] = flow_duration(rangeDFName, instDFName)
        

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
    

################ GRAPHS ################ 
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



#Adding a folder to hold the graphs
new_folder_name = "Graphs"
count = 0

while True:
    # Check if the directory exists
    if not os.path.exists(new_folder_name):
        # If it doesn't exist, create the new directory
        os.mkdir(new_folder_name)
        break
    else:
        count += 1
        new_folder_name = "Graphs (" + str(count) + ")"

#Flow Duration Curve Function and Graph Creation
def fdc(dataframe, flows):

    #Calculating probabilities for each flow 
    sortedFlows = sorted(dataframe[flows], reverse=True)
    n = len(sortedFlows)
    exceedance_prob = np.arange(1, n + 1) / (n + 1) * 100

    data = dataframe[flows] 
    x = range(len(data))  
    y = data  

    #Quartile Calculations
    q1 = np.percentile(data, 25)
    q2 = np.percentile(data, 50)
    q3 = np.percentile(data, 75)    

    #Graph Creation
    plt.figure(figsize=(8, 6))
    plt.plot(exceedance_prob, sortedFlows, linestyle='-', color='red')

    #limits
    plt.xlim(0, 100)
    plt.ylim(0, int(dataframe[flowColumn].max()))
    plt.grid(True)

    #labels
    xtick_positions = [0, 25, 50, 75, 100]  
    xtick_labels = ['0', '25', '50', '75', '100']
    plt.xticks(xtick_positions, xtick_labels)  
    plt.xlabel('Exceedance Probability (%)')
    plt.ylabel('Flow Rate (cfs)')
    plt.title('Flow Duration Curve')
    
   #quartile lines
    plt.hlines(q1, xmin=0, xmax=75, colors='y', linestyles='--', label='Q1')
    plt.vlines(75, ymin=0, ymax=q1, colors='y', linestyles='--', label='Q2 (Median)')
    plt.text(90, q1, "q1 = " + str(q1), fontsize=7, ha='center')
    
    plt.vlines(50, ymin=0, ymax=q2, colors='g', linestyles='--', label='Q2 (Median)')
    plt.hlines(q2, xmin=0, xmax=50, colors='g', linestyles='--', label='Q2 (Median)')
    plt.text(65, q2, "q2 = " + str(q2), fontsize=7, ha='center')

    plt.vlines(25, ymin=0, ymax=q3, colors='b', linestyles='--', label='Q2 (Median)')
    plt.hlines(q3, xmin=0, xmax=25, colors='b', linestyles='--', label='Q3')
    plt.text(40, q3, "q3 = " + str(q3), fontsize=7, ha='center')

    #legend
    legend_entries = []
    plt.subplots_adjust(bottom=0.2) 
    legend_entries.append(plt.Line2D([0], [0], color='y', label='q1', linestyle = '--'))
    legend_entries.append(plt.Line2D([0], [0], color='g', label='q2', linestyle = '--'))
    legend_entries.append(plt.Line2D([0], [0], color='b', label='q3', linestyle = '--'))
    
    plt.legend(handles=legend_entries, bbox_to_anchor=(0.5, -.15), loc='upper center', ncol=3)

    plot_filename = os.path.join(new_folder_name, "Flow Duration.png")
    plt.savefig(plot_filename)

    plt.show()

#Making graphs for Days within certain ranges
def rangeGraph():
    for r in ranges:
        rangeDFName = "range" + str(r[0]) + "_" + str(r[1]) + "df"
        rangeDF = rangeDataFrames[rangeDFName]

        #defining plot size
        plt.figure(figsize=(8, 6))

        #defining plot type
        if color == 'spectral':
            
            i = 0
            mColors = ['lightblue', "#a5d6c5", "#84ad89","#b0c27a","#f5f587","#e0b15a","#e89464","#b37659","#b06363","#f27c7c","#c086c4", "#b6abcc",]
            startColor = months[i].month

            while i < (len(months) - 1):
                if i >= len(mColors) - 1:
                    startColor = 0
                plt.fill_between([months[i], months[i + 1]], y1 = int(r[0]) * (-.25), y2 = int(r[1]) * 1.25,  color=mColors[startColor], alpha=0.5)
                i += 1
                startColor += 1
    
            var = 'black'
        else:
            var = 'red'
        
        plt.scatter(rangeDF['Day'], rangeDF['Flow'], color=var, linestyle='None', zorder=2, marker='o', edgecolor='white', s=90)

        #Labels
        plt.title("Days Within Flow Rate " + str(r[0]) + " - " + str(r[1]))
        plt.xlabel("Month")
        plt.ylabel("Flow Rate (cfs)")

        #Limits and limit labels
        plt.xlim(months[0], months[len(months) - 1])
        plt.xticks(months, monthLabels)
        plt.ylim(int(r[0]) * (-.25), int(r[1]) * 1.25)

        #legend
        legend_entries = []
        legend_entries.append(plt.Line2D([0], [0], color=var, label='Day', marker = 'o'))
        plt.subplots_adjust(bottom=0.2) 
        plt.legend(handles=legend_entries, bbox_to_anchor=(0.5, -.15), loc='upper center', ncol=2)

        plot_filename = os.path.join(new_folder_name, "Range " + str(r[0]) + " - " + str(r[1]) + ".png")
        plt.savefig(plot_filename)

        plt.show()


#Average Daily Flow Over a Year Graph Display
def avgDailyFlow(): 
    #Graph cration
    plt.figure(figsize=(8, 6))
    
     #Theme 
    if color == 'spectral':
        i = 0
        mColors = ['lightblue', "#a5d6c5", "#84ad89","#b0c27a","#f5f587","#e0b15a","#e89464","#b37659","#b06363","#f27c7c","#c086c4", "#b6abcc",]
        startColor = months[i].month

        while i < (len(months) - 1):
            if i >= len(mColors) - 1:
                startColor = 0
            plt.fill_between([months[i], months[i + 1]], y1 = 0, y2 = int(df[flowColumn].max()) * 1.25,  color=mColors[startColor], alpha=0.5)
            i += 1
            startColor += 1
            
        var = 'gray'
    else: 
        var = "red"

    #Data definition
    plt.plot(df["Day"], df["MF"], color=var, zorder = 2, marker = 'o', markerfacecolor = 'black', markeredgecolor = "white", linestyle = '-')
    
    #Labels
    plt.title("Average Daily Flow Rate Over a Year")
    plt.xlabel("Month")
    plt.ylabel("Flow Rate (cfs)")
    plt.xticks(months, monthLabels)
    yticks = []
    ytickLabels = []

    #Adding lines at ranges
    for r in ranges:
        plt.axhline(y=r[0], color='white', linestyle='--', label='Horizontal Line at y=0', zorder=1)
        yticks.append(r[0])
        ytickLabels.append(str(r[0]))
        plt.axhline(y=r[1], color='white', linestyle='--', label='Horizontal Line at y=0', zorder = 1)
        yticks.append(r[1])
        ytickLabels.append(str(r[1]))
    
    plt.yticks(yticks, ytickLabels)

    #limits
    plt.xlim(months[0], months[len(months) - 1])
    plt.ylim(0, int(df[flowColumn].max()) * 1.1)

    #legend
    legend_entries = []
    legend_entries.append(plt.Line2D([0], [0], color='black', label='Day', marker = 'o'))
    plt.subplots_adjust(bottom=0.2) 
    plt.legend(handles=legend_entries, bbox_to_anchor=(0.5, -.15), loc='upper center', ncol=2)

    plot_filename = os.path.join(new_folder_name, "Average Daily Flow.png")
    plt.savefig(plot_filename)

    plt.show()

#Bar Chart Duration Graph Function
def instanceBar():
    for r in ranges:
        instanceDFName = "instances" + str(r[0]) + "_" + str(r[1]) 
        instanceDF = instDataFrames[instanceDFName]

        plt.figure(figsize=(8, 6))
        
         #Theme 
        if color == 'spectral':
            i = 0
            mColors = ['lightblue', "#a5d6c5", "#84ad89","#b0c27a","#f5f587","#e0b15a","#e89464","#b37659","#b06363","#f27c7c","#c086c4", "#b6abcc",]
            startColor = months[i].month

            while i < (len(months) - 1):
                if i >= len(mColors) - 1:
                    startColor = 0
                plt.fill_between([months[i], months[i + 1]], y1 = 0, y2 = int(r[1]) * 1.25,  color=mColors[startColor], alpha=0.5)
                i += 1
                startColor += 1
            var = 'black'
        else: 
            var = "red"

        #Creation of bar graph
        plt.bar(instanceDF['dayStart'], instanceDF['duration'], zorder = 2, color = var, width = 3)


        #labels
        plt.title("Days Within Flow Rate " + str(r[0]) + " - " + str(r[1]))
        plt.title("Instance Durations Within " + str(r[0]) + " - " + str(r[1]) + " cfs")
        plt.xlabel("Start Day")
        plt.ylabel("Duration (days)")
        plt.xticks(months, monthLabels)

        #limits
        plt.xlim(months[0], months[len(months) - 1])
        if len(instanceDF['duration']) > 0:
            plt.ylim(0, instanceDF['duration'].max() * 1.15)
        else:
            plt.ylim(ranges[0][0], ranges[len(ranges) - 1][1])

        #legend
        
        plot_filename = os.path.join(new_folder_name, "Instance Bar: " + str(r[0]) + " - " + str(r[1]) + ".png")
        plt.savefig(plot_filename)
        plt.show()

#Flow Instance Duration Graph Creation
def allInstDur():
    
    #Plot creation
    #fig, ax = plt.subplots()
    plt.figure(figsize = (15, 6))
    
    #Theme 
    if color == 'spectral':
        i = 0
        mColors = ['lightblue', "#a5d6c5", "#84ad89","#b0c27a","#f5f587","#e0b15a","#e89464","#b37659","#b06363","#f27c7c","#c086c4", "#b6abcc",]
        startColor = months[i].month
        
        while i < (len(months) - 1):
            if i >= len(mColors) - 1:
                startColor = 0
            plt.fill_between([months[i], months[i + 1]], y1 = -(int(ranges[len(ranges) - 1][1])) , y2 = int(ranges[len(ranges) - 1][1]) * 1.25,  color=mColors[startColor], alpha=0.5)
            i += 1
            startColor += 1

        var = 'black'
    else: 
        var = "red"

    #Making lines based on start and end of each flow instance
    for r in ranges:
        tupleListName = "tuples" + str(r[0]) + "_" + str(r[1])
        rangeName = str(r[0]) + " - " + str(r[1])

        tuplesBool = False
        for tup in tupleLists[tupleListName]:
            if tupleLists[tupleListName] > 0:
                tuplesBool = True
            plt.hlines(y=[rangeName], xmin=tup[0], xmax=tup[1], color=var, linewidth=8)

    #limits
    plt.xlim(months[0], months[len(months) - 1])
    if tuplesBool == False:
        plt.ylim(0, int(ranges[len(ranges) - 1][1]))
        plt.yticks([])

    #labels
    plt.title("Duration of Flow at Different Rates")
    plt.xlabel("Day")
    plt.ylabel("Flow (cfs)")
    plt.xticks(months, monthLabels)
    
    #legend
    legend_entries = []
    legend_entries.append(plt.Line2D([0], [0], color=var, label='Period of Consecutive Days', linewidth=8, linestyle='-'))
    plt.subplots_adjust(bottom=0.2) 
    plt.legend(handles=legend_entries, bbox_to_anchor=(0.5, -.15), loc='upper center', ncol=2)
   
    plot_filename = os.path.join(new_folder_name, "All Instance Durations.png")
    plt.savefig(plot_filename)
    plt.show()


#Flow Duration Graph Creation
fdc(df, flowColumn)


#Average Daily Flow Over a Year Graph Creation
avgDailyFlow()

#Range Graph Creation for Each Range
rangeGraph()


#Bar Chart Duration Graph Creation
instanceBar()


#Flow Instance Duration Graph Creation
allInstDur()

print("\nDone!\n")