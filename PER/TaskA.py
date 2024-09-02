import time

start_time = time.time()

with open("PERData/TaskA.csv") as fileInput: # CSV-Like Format: Timestamp, ID, Value
    data = list(fileInput)
    data.pop(0)

Voltage_ID = -1
Current_ID = -1
FL_Wheel_Speed_ID = -1
FR_Wheel_Speed_ID = -1
BL_Wheel_Speed_ID = -1
BR_Wheel_Speed_ID = -1

relevant_names = [
    "Voltage (ams.pack.voltage)", 
    "Current (ams.pack.current)", 
    "Front Left Wheel Speed (pcm.wheelSpeeds.frontLeft)", 
    "Front Right Wheel Speed (pcm.wheelSpeeds.frontRight)", 
    "Back Left Wheel Speed (pcm.wheelSpeeds.backLeft)", 
    "Back Right Wheel Speed (pcm.wheelSpeeds.backRight)"
]

relevant_IDs = [-1, -1, -1, -1, -1, -1]

variable_names = []
relevant_data = []
min_ID = -1
max_ID = -1
first_time = -1
first_data_index = -1

for i in range(len(data)):
    data[i] = data[i].strip()
    if data[i][0] == "V":
        temp = data[i][6:].split(": ")
        if temp[0] in relevant_names:
            temp[1] = int(temp[1])
            if min_ID == -1:
                min_ID = temp[1]
            
            temp[1] -= min_ID
            max_ID = temp[1]
            relevant_IDs[relevant_names.index(temp[0])] = temp[1]
            variable_names.append(temp)
    else:
        if first_data_index == -1:
            first_data_index = i
        data[i] = data[i].split(",")
        data[i][1] = int(data[i][1]) - min_ID
        if data[i][1] in relevant_IDs:
            data[i][2] = float(data[i][2])
            if first_time == -1:
                first_time = int(data[i][0])
            data[i][0] = int(data[i][0]) - first_time
            relevant_data.append(data[i])

''' print(relevant_names)
print(variable_names)
print(relevant_IDs)
print(relevant_data) '''

relevant_IDs.sort()

for i in range(len(variable_names)):
    variable_names[i][1] = i

for i in range(len(relevant_data)):
    relevant_data[i][1] = relevant_IDs.index(relevant_data[i][1])

for i in range(len(relevant_names)):
    relevant_names[i] = variable_names[i][0]

''' print(relevant_names)
print(variable_names)
print(relevant_IDs)
print(relevant_data) '''

# print("Setup Time : " + str(int((time.time() - start_time) * 100 + 0.5) / 100)) # takes roughly 25 seconds to parse and organize all the data