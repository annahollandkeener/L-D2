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
    while True:
        dataType = input("Enter data type ('elevation', 'flow')")
        if dataType.lower() == 'flow':
            file_name = 'manual.py'
        elif dataType.lower() == 'elevation':
            file_name = 'elev.py'
        else:
            print("Invalid input.")
elif mode == 'USGS':
    file_name = 'USGS'
    
os.system('python {}'.format(file_name))


