import os

print("\n------------Flow Analysis------------")

modes = ['manual', 'usgs']

mode = ''

while True: 
    print("\nModes: ")
    print("------------")

    for mode in modes:
        print("|'" + mode + "'")
    print("------------")
    print("\nType 'modes' for a description of each mode.")
    response = input("Select mode: ")

    
    if response.lower() == 'mode':
        print("\nDescription...")
    elif response.lower() == 'manual':
        print("\nManual mode selected.")
        mode = response.lower()
        break 
    elif response.lower() == 'usgs':
        print("\nUSGS mode selected.")
        mode = response.lower()
    else:
        print("\nInvalid input.")

if mode == 'manual':
    file_name = 'Flow_Analysis.py'
elif mode == 'USGS':
    file_name = 'USGS'
    
os.system('python {}'.format(file_name))


