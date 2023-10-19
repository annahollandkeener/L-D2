import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import stylefile



#CSV variables to remember
file = ''
flowColumn = ''
dayColumn = ''
df = ''

print("\n------------Flow Analysis------------\n")
#Manual data entry mode
'''

#Remembering if user wants the flow duration curve chart included or not
while True:
    flowDurationCurve = input("Flow duration curve? (y/n): ")
    if flowDurationCurve == 'y':
        break
    elif flowDurationCurve == 'n':
        break
    else:

        print("***Invalid input***")

#Remembering if user wants the instance duration charts included or not
while True:
    instanceClass = input("\nFlow instance classification? (y/n): ")
    if instanceClass == 'y':
        break
    elif instanceClass == 'n':
        break
    else:
        print("***Invalid input***")     
    '''  


#Requesting file from user until viable file provided
while True:
    file = input("\nEnter csv name (including '.csv'): ")
    try:
        data = pd.read_csv(file, converters={flowColumn:int})
        #Converting it to a dataframe
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


while True:
    dayColumn = input("\nEnter name of the time column (units in days, be mindful of capital letters): ")
    if dayColumn in df.columns:
        print("Column '" + dayColumn + "' selected.")
        break
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



#Creating a dictionary to store dataframes. 
rangeDataFrames = {}

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
    new_row = {'Day': df['Day'][x], 'Flow': flow}
    return new_row


#Sorting all of the flows in the flow column into specified ranges
i = 0
while i < (len(df[flowColumn])):
    for r in ranges:
        dictName = "range" + str(r[0]) + "_" + str(r[1])
        dfRangeName = dictName + "df"

        if int(df[flowColumn][i]) >= int(r[0]):
            if df[flowColumn][i] >= int(r[0]) and df[flowColumn][i] <= int(r[1]):
                new_row = {'Day': df['Day'][i], 'Flow': df[flowColumn][i]}
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
                if (((rangeDF['Day'][nex]) - 1) == (rangeDF['Day'][curr])):
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
    instDFName = "instances" + str(r[0]) + "_" + str(r[1])
    rangeDFName = "range" + str(r[0]) + "_" + str(r[1]) + "df"
    instDataFrames[instDFName] = flow_duration(rangeDFName, instDFName)

    
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
            var = 'black'
        else:
            var = 'red'
        
        plt.scatter(rangeDF['Day'], rangeDF['Flow'], color=var, linestyle='None', zorder=2, marker='o', edgecolor='white', s=90)

        #Labels
        plt.title("Days Within Flow Rate " + str(r[0]) + " - " + str(r[1]) + " (2013-2023)")
        plt.xlabel("Month")
        plt.ylabel("Flow Rate (cfs)")

        #Limits and limit labels
        plt.xlim(1, 366)
        plt.xticks(stylefile.xtick_positions, stylefile.xtick_labels)
        plt.ylim(0, int(r[1]) * 1.25)

        #Theme 
        if color == 'spectral':
            stylefile.monthColors(plt)
            plt.legend(handles=stylefile.monthLegend, bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=2)

        plt.show()


#Average Daily Flow Over a Year Graph Display
def avgDailyFlow(): 
    #Graph cration
    plt.figure(figsize=(8, 6))
    
     #Theme 
    if color == 'spectral':
        stylefile.monthColors(plt)
        var = 'gray'
    else: 
        var = "red"

    #Data definition
    plt.plot(df["Day"], df["MF"], color=var, zorder = 2, marker = 'o', markerfacecolor = 'black', markeredgecolor = "white", linestyle = '-')
    
    #Labels
    plt.title("Average Daily Flow Rate Over a Year (2013-2023)")
    plt.xlabel("Month")
    plt.ylabel("Flow Rate (cfs)")
    plt.xticks(stylefile.xtick_positions, stylefile.xtick_labels)

    #Adding lines at ranges
    for r in ranges:
        plt.axhline(y=r[0], color='white', linestyle='--', label='Horizontal Line at y=0', zorder=1)
        plt.axhline(y=r[1], color='white', linestyle='--', label='Horizontal Line at y=0', zorder = 1)
   
    #limits
    plt.xlim(0, 365)
    plt.ylim(0, int(df[flowColumn].max()) * 1.1)

    #legend
    plt.legend(handles=stylefile.monthLegend, bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=2)

    plt.show()

#Bar Chart Duration Graph Function
def instanceBar():
    for i in instDataFrames:
        #Creation of bar graph
        plt.bar(i['dayStart'], i['duration'], zorder = 2, color = 'black')

        #labels
        plt.title("Instance Durations 0-1500 cfs")
        plt.xlabel("Start Day")
        plt.ylabel("Duration (days)")
        plt.xticks(stylefile.xtick_positions, stylefile.xtick_labels)

        #limits
        plt.xlim(0, 366)
        plt.ylim(0, 30)
     
        #theme
        stylefile.monthColors(plt)

        #legend
        plt.legend(handles=stylefile.monthLegend, bbox_to_anchor=(0.5, -0.2), loc='upper center', ncol=2)
        plt.show()
    


#Flow Duration Graph Creation
fdc(df, flowColumn)

#Average Daily Flow Over a Year Graph Creation
avgDailyFlow()

#Range Graph Creation for Each Range
rangeGraph()

#Bar Chart Duration Graph Creation
instanceBar()



