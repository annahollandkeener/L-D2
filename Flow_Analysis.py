import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#CSV variables to remember
file = ''
flowColumn = ''
dayColumn = ''

#Remembering if user wants the flow duration curve chart included or not
while True:
    flowDurationCurve = input("Flow duration curve? (y/n): ")
    if flowDurationCurve == 'y':
        break
    elif flowDurationCurve == 'n':
        break
    else:
        print("Invalid input.")

#Remembering if user wants the instance duration charts included or not
while True:
    instanceClass = input("Flow instance classification? (y/n): ")
    if instanceClass == 'y':
        break
    elif instanceClass == 'n':
        break
    else:
        print("Invalid input.")       


#Collecting details on csv
file = input("Enter csv name (including '.csv'): ")
flowColumn = input("Enter name of flow column: ")
dayColumn = input("Enter name of the time column (units in days): ")

#Prompting the user to decide between default ranges and unique ranges
while True:
    print("Default ranges are: 0-1500, 1500-3500, 3500-7500, 7500-10000, >10000")
    specify = input("Specify ranges? (y/n): ")
    if specify == 'y':
        break
    elif specify == 'n':
        print("Default ranges selected: 0-1500, 1500-3500, 3500-7500, 7500-10000, >10000")
        break
    else:
        print("Invalid input.")      

#list to keep track of ranges
ranges = []

#preset ranges
defaultRanges = [(0,1500), (1500,3500), (3500, 7500), (7500, 10000), (10000, 50000)]

#prompts user to specify ranges until they are finished 
if specify == 'y':
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

if specify == 'y':
    print("\nYour ranges: ")
    for t in ranges:
        print(t)

#Start of process
print("\nWorking...")


#reading in user file
data = pd.read_csv(file, converters={flowColumn:int})
#converting it to a dataframe
df = pd.DataFrame(data)


#Creating a dictionary to store dataframes
rangeDataFrames = {}

#Adding a dataframe for each range to list. Using default ranges if not specified. 
if specify == 'n':
    for r in defaultRanges:
        dictName = "range" + r[0] + "_" + r[1]
        dic = {
            'Day' : [],
            'Flow' : [],
            }
        dfRangeName = dictName + "df"
        dfRange = pd.DataFrame(dic)
        rangeDataFrames[dfRangeName] = dfRange
#And using user given ranges when specified
if specify == 'y':
    for r in ranges:
        dic = {
            'Day' : [],
            'Flow' : [],
            }
        print(dic)
        dfName = "range" + str(r[0]) + "_" + str(r[1])
        #dfs called using range#_#
        dfName = pd.DataFrame(dic)
        rangeDataFrames.append(dfRange)

for frame in rangeDataFrames:
    print(frame)