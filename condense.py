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

ranges = [(-2, 1.5), (1.5, 2), (2, 3), (3, 3.5)]

#print ranges
print("\nYour ranges: ")
for t in ranges:
    print(t)


#Start of process
print("\nWorking...")

df = df.groupby(dayColumn)[elevColumn].mean().reset_index()

new_folder_name = "Grouped Data"
count = 0

while True:
    # Check if the directory exists
    if not os.path.exists(new_folder_name):
        # If it doesn't exist, create the new directory
        os.mkdir(new_folder_name)
        break
    else:
        count += 1
        new_folder_name = "Data (" + str(count) + ")"

print(df)
df.to_csv("Data.csv", index=False)
dataName = os.path.join(new_folder_name, "Data.csv")

print("Done! Grouped by hour.")