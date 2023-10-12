import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#CSV variables to remember
file = ''
flowColumn = ''
dayColumn = ''
df = ''

print("\n------------Flow Analysis------------\n")

#Remembering if user wants the flow duration curve chart included or not
while True:
    flowDurationCurve = input("Flow duration curve? (y/n): ")
    if flowDurationCurve == 'y':
        break
    elif flowDurationCurve == 'n':
        break
    else:
        print("*** Invalid input ***")

#Remembering if user wants the instance duration charts included or not
while True:
    instanceClass = input("\nFlow instance classification? (y/n): ")
    if instanceClass == 'y':
        break
    elif instanceClass == 'n':
        break
    else:
        print("*** Invalid input ***")       

#Requesting file from user until viable file provided
while True:
    file = input("\nEnter csv name (including '.csv'): ")
    try:
        data = pd.read_csv(file, converters={flowColumn:int})
        #Converting it to a dataframe
        df = pd.DataFrame(data)
        break
    except FileNotFoundError:
        print("\n*** Error reading the CSV file. \nMake sure it is spelled correctly and in the same directory as this executable ***")

    
#Collecting details on csv
while True:
    flowColumn = input("\nEnter name of flow column (be mindfu of capital letters): ")
    if flowColumn in df.columns:
        print("Column '" + flowColumn + "' selected.")
        break
    else:
        print("\n*** This is not a column in the given csv ***")

while True:
    dayColumn = input("\nEnter name of the time column (units in days, be mindfu of capital letters): ")
    if dayColumn in df.columns:
        print("Column '" + dayColumn + "' selected.")
        break
    else:
        print("\n*** This is not a column in the given csv ***")


#Prompting the user to decide between default ranges and unique ranges
print("\nDefault ranges are: 0-1500, 1500-3500, 3500-7500, 7500-10000, >10000")
while True:
    specify = input("Specify ranges? (y/n): ")
    if specify == 'y':
        break
    elif specify == 'n':
        print("Default ranges selected: 0-1500, 1500-3500, 3500-7500, 7500-10000, >10000")
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
    ranges = [(0,1500), (1500,3500), (3500, 7500), (7500, 10000), (10000, 50000)]

#print ranges
print("\nYour ranges: ")
for t in ranges:
    print(t)

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

print(rangeDataFrames)

'''
#New row function
x = 0
def new_row(dataFrame, flow):
    new_row = {'Day': df['Day'][x], 'Flow': flow}
    return new_row

#Sorting all of the flows in the flow column into specified ranges
for flow in df['MF']:
    if flow >= ranges:
        range0_1500df = range0_1500df.append(new_row(range0_1500df, flow), ignore_index=True)
        x += 1
    elif ((flow > 1500) & (flow <= 3500)):
        range1500_3500df = range1500_3500df.append(new_row(range3500_7500df, flow), ignore_index=True)
        x += 1
    elif ((flow > 3500) & (flow <= 7500)):
        range3500_7500df = range3500_7500df.append(new_row(range3500_7500df, flow), ignore_index=True)
        x += 1
    elif ((flow > 7500) & (flow <= 10000)):
        range7500_10000df = range7500_10000df.append(new_row(range7500_10000df, flow), ignore_index=True)
        x += 1
    elif (flow > 10000):
        rangeOver10000df = rangeOver10000df.append(new_row(rangeOver10000df, flow), ignore_index=True)
        x += 1
    else:
        catchall.append(flow)
        x += 1
'''