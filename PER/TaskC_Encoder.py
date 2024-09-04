''' CUSTOM DATA FORMAT - list; Assuming < 2^12 - 1 Variables; more than double what current has
Entries go in this format:
{
    { // General Variables
        Log Date, 
        Log Time, 
        ID_Shifter, 
        Starting_Time
    }, {
        Name 1, 
        Time Stamp 1, 
        Value 1, 
        Time Stamp 2, 
        Value 2, ...
    }, {
        Name 2, 
        Time Stamp 1, 
        Value 1, 
        Time Stamp 2, 
        Value 2, ...
    }, ...
} '''

import time
import json

start_time = time.time()

with open("PERData/TaskA.csv") as fileInput: # CSV-Like Format: Timestamp, ID, Value
    data = list(fileInput)

jason = [] # didn't want to name the json as json because that would probably mess things up, so I'm naming it jason instead

for i in range(4096):
    jason.append([])

for i in range(len(data)):
    data[i] = data[i].strip()
    if data[i] == "":
        continue
    if data[i][0] == "P": # Header. Need to keep data from header because I think its important to keep
        data[i] = data[i].split()
        jason[0].append(data[i][4])
        jason[0].append(data[i][5] + " " + data[i][6])
    elif data[i][0] == "V": # Variable definition
        temp = data[i][6:].split(": ")
        
        temp[1] = int(temp[1])
        if len(jason[0]) == 2:
            jason[0].append(temp[1] - 1)
        
        jason[temp[1] - jason[0][2]].append(temp[0])
    else: # Data update
        data[i] = data[i].split(",")

        if len(jason[0]) == 3:
            jason[0].append(int(data[i][0]))

        data[i][0] = int(data[i][0]) - jason[0][3] # Adjusted Time Stamp
        data[i][1] = int(data[i][1]) - jason[0][2] # Adjusted ID
        if "." in data[i][2] or data[i][2] == "inf" or data[i][2] == "NaN" or data[i][2] == "-inf": # see which ones need to be converted to int or float
            data[i][2] = float(data[i][2])
        else:
            data[i][2] = int(data[i][2])
        
        jason[data[i][1]].append(data[i][0])
        jason[data[i][1]].append(data[i][2])

with open("PERData/TaskCEncoded.skeole", "w") as outfile:
    # outfile.write(str(jason)) # - this worked as well, but was around 238 MB
    outfile.write(json.dumps(jason, separators=(",", ""))) # json.dumps() allows for more compact formatting than json.dump(), though it takes longer to execute

print("Time to Run Code : " + str(int((time.time() - start_time) * 100 + 0.5) / 100))
# takes roughly 50 seconds
# Compresses the .csv file of 285 MB to into a custom .skeole file of 204 MB, which is roughly a 30% reduction