# This file checks for lossnessness by converting an already-encoded-and-decoded .csv (which has switched from .csv to .skeole back to .csv)
    # into a .skeole again, and checking that the two .skeole files produced are equivalent
    # technically, this does not prove data loss; a true proof would be showing .csv to .skeole to .csv is the same
    # however, it's not possible to re-convert it into the exact same .csv because the way the data is entered into the .csv is not ordered in a consistent manner
    # even if it was possible to do so, the time complexity would be too large to do so in a reasonable amount of time
    # however, you can see that TaskA.csv and TaskCEncodedAndDecoded.txt contain the same amount of non-empty lines lines (16 766 709), an indication that there is no data loss

import time
import json

start_time = time.time()

with open("PERData/TaskCEncodedAndDecoded.txt") as fileInput: # CSV-Like Format: Timestamp, ID, Value
    data = list(fileInput)

jason = []

for i in range(4096):
    jason.append([])

for i in range(len(data)):
    data[i] = data[i].strip()
    if data[i] == "":
        continue
    if data[i][0] == "P":
        data[i] = data[i].split()
        jason[0].append(data[i][4])
        jason[0].append(data[i][5] + " " + data[i][6])
    elif data[i][0] == "V":
        temp = data[i][6:].split(": ")
        
        temp[1] = int(temp[1])
        if len(jason[0]) == 2:
            jason[0].append(temp[1] - 1)
        
        jason[temp[1] - jason[0][2]].append(temp[0])
    else:
        data[i] = data[i].split(",")

        if len(jason[0]) == 3:
            jason[0].append(int(data[i][0]))

        data[i][0] = int(data[i][0]) - jason[0][3] # Adjusted Time Stamp
        data[i][1] = int(data[i][1]) - jason[0][2] # Adjusted ID
        if "." in data[i][2] or data[i][2] == "inf" or data[i][2] == "nan" or data[i][2] == "-inf":
            data[i][2] = float(data[i][2])
        else:
            data[i][2] = int(data[i][2])
        
        jason[data[i][1]].append(data[i][0])
        jason[data[i][1]].append(data[i][2])

jason_string = json.dumps(jason, separators=(",", ""))

with open("PERData/TaskCEncoded.skeole") as fileInput:
    data = list(fileInput)[0].strip()

if jason_string == data: # check for equality here
    print("Encoding and Decoding is lossless!") # yippee :D
else:
    print("Something went wrong") # not yippee D:

print("Time to Run Code : " + str(int((time.time() - start_time) * 100 + 0.5) / 100))
# takes roughly 40 seconds