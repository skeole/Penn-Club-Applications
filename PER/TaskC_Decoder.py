import time
import json

start_time = time.time()

with open("PERData/TaskCEncoded.skeole") as fileInput:
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

jason.append("PER CSV Modbus Log " + data[0][0] + " " + data[0][1]) # Header

ID_shifter = data[0][2]
time_shifter = data[0][3]

starting_index = -1

for i in range(1, len(data)):
    if data[i][0] != "": # if it's not an empty variable (i.e. if something actually exists here)
        jason.append("Value " + data[i][0] + ": " + str(i + ID_shifter)) # Variable definitions
        if starting_index == -1:
            if len(data[i]) > 1:
                if data[i][1] == 0:
                    starting_index = i

# [['05/25/23', '09:39:05 PM', 8191, 125000], ['Pcm OK (pcm.signals.pcmOk)', 72, 1, 173, 1]] # how the .skeole looks

# PER CSV Modbus Log 05/25/23 09:39:05 PM # how the .csv should look
# Value Pcm OK (pcm.signals.pcmOk): 8192
# 125000,8468,4.13725

# Note: This WILL NOT preserve the order of the data in the .csv; however, all of the originally contained data will be in there somewhere

jason.append(str(time_shifter) + "," + str(starting_index + ID_shifter) + "," + str(data[starting_index][2]))
# add the first time value to be the leader of the .csv data section

for i in range(1, 4096):
    for j in range(1 if i != starting_index else 3, len(data[i]), 2): # make sure you don't re-add the leading value twice
        jason.append(str(time_shifter + data[i][j]) + "," + str(i + ID_shifter) + "," + str(data[i][j + 1]))

json_string = (json.dumps(jason, separators=("\n", ""))[1:-1]).replace("\"", "")

with open("PERData/TaskCEncodedAndDecoded.txt", "w") as outfile:
    outfile.write(json_string)

print("Time to Run Code : " + str(int((time.time() - start_time) * 100 + 0.5) / 100))
# Takes roughly 35 seconds