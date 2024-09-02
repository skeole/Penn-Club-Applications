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

with open("PERData/TaskCEncoded.txt") as fileInput:
    data = list(fileInput)[0].strip()

if jason_string == data:
    print("Encoding and Decoding is lossless!")
else:
    print("Something went wrong")

print("Setup Time : " + str(int((time.time() - start_time) * 100 + 0.5) / 100)) # takes roughly 30 seconds to check for equality