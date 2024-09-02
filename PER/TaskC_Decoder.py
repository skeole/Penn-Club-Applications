''' DATA FORMAT - list; Assuming < 2^12 - 1 Variables; more than double what current has
Entries go in this format:
{
    { // General Variables
        Log Date, 
        Log Time, 
        ID_Shifter, 
        Starting_Time
    }, {
        Name 1, 
        {
            Time Stamp 1, 
            Value 1
        }, {
            Time Stamp 2, 
            Value 2
        }, ...
    }, {
        Name 2, 
        {
            Time Stamp 1, 
            Value 1
        }, {
            Time Stamp 2, 
            Value 2
        }, ...
    }, ...
} '''

import time
import json

start_time = time.time()

with open("PERData/TaskCEncoded.txt") as fileInput:
    data = list(fileInput)[0].strip()[2:-2].split("],[")

for i in range(len(data)): # Takes around 15 seconds to parse this
    data[i] = data[i].split(",")
    for j in range(len(data[i])):
        if (j == 0) or (i == 0 and j == 1):
            data[i][j] = data[i][j][1:-1]
        elif "." in data[i][j] or data[i][j] == "inf" or data[i][j] == "nan" or data[i][j] == "-inf" or data[i][j] == "Infinity" or data[i][j] == "-Infinity" or data[i][j] == "NaN":
            data[i][j] = float(data[i][j])
        else:
            data[i][j] = int(data[i][j])

jason = []

jason.append("PER CSV Modbus Log " + data[0][0] + " " + data[0][1])

ID_shifter = data[0][2]
time_shifter = data[0][3]

starting_index = -1

for i in range(1, len(data)):
    if data[i][0] != "":
        jason.append("Value " + data[i][0] + ": " + str(i + ID_shifter))
        if starting_index == -1:
            if len(data[i]) > 1:
                if data[i][1] == 0:
                    starting_index = i

# [['05/25/23', '09:39:05 PM', 8191, 125000], ['Pcm OK (pcm.signals.pcmOk)', 72, 1, 173, 1]]

# PER CSV Modbus Log 05/25/23 09:39:05 PM
# Value Pcm OK (pcm.signals.pcmOk): 8192
# 125000,8468,4.13725

jason.append(str(time_shifter) + "," + str(starting_index + ID_shifter) + "," + str(data[starting_index][2]))

for i in range(1, 4096):
    for j in range(1 if i != starting_index else 3, len(data[i]), 2):
        jason.append(str(time_shifter + data[i][j]) + "," + str(i + ID_shifter) + "," + str(data[i][j + 1]))

json_string = (json.dumps(jason, separators=("\n", ""))[1:-1]).replace("\"", "")

with open("PERData/TaskCEncodedAndDecoded.txt", "w") as outfile: # CSV-Like Format: Timestamp, ID, Value
    outfile.write(json_string)

print("Setup Time : " + str(int((time.time() - start_time) * 100 + 0.5) / 100)) # Takes around 30 seconds