import time
import json

import numpy as np 
import matplotlib.pyplot as plt 

start_time = time.time() # this is so we can record total time code takes to run

with open("PERData/TaskA.csv") as fileInput: # open the data file as a variable
    data = list(fileInput) # CSV-Like Format: Timestamp, ID, Value
    data.pop(0) # remove the first entry, which is just a header

relevant_names = [
    "Voltage (ams.pack.voltage)", 
    "Current (ams.pack.current)", 
    "Front Left Wheel Speed (pcm.wheelSpeeds.frontLeft)", 
    "Front Right Wheel Speed (pcm.wheelSpeeds.frontRight)", 
    "Back Left Wheel Speed (pcm.wheelSpeeds.backLeft)", 
    "Back Right Wheel Speed (pcm.wheelSpeeds.backRight)"
] # the names we're filtering for

relevant_IDs = [-1, -1, -1, -1, -1, -1] # we don't know the IDs yet, but the order is the same as in relevant_names

variable_names = [] # this will be used so we can reorder the IDs and names according to ascending order
relevant_data = [] # filter out useful data
min_ID = -1 # the smallest ID in the list, used to normalize the IDs
max_ID = -1 # largest ID in the list. I don't think I'm using this one anymore
first_time = -1 # smallest time recorded, used to normalize the time
first_data_index = -1 # so we know where the variable definition stops and data reporting starts

for i in range(len(data)):
    data[i] = data[i].strip() # remove whitespace (there will be a \newline)
    if data[i][0] == "V": # if its a variable definer
        temp = data[i][6:].split(": ") # first part will be variable name, second will be value
        if temp[0] in relevant_names: # if its a relevant variable
            temp[1] = int(temp[1]) # convert string of second part to integer equivalent
            if min_ID == -1:
                min_ID = temp[1] # IDs are in ascending order, so the first one defined will be the minimum
            
            temp[1] -= min_ID # normalize the ID
            max_ID = temp[1] # IDs are in ascending order, so the last one defined will be the maximum
            relevant_IDs[relevant_names.index(temp[0])] = temp[1] # update list of relevant IDs
            variable_names.append(temp) # variable names will be sorted based on ID
    else:
        if first_data_index == -1:
            first_data_index = i # same logic as min ID
        data[i] = data[i].split(",") # Non-adjusted timestamp, non-adjusted ID, value
        data[i][1] = int(data[i][1]) - min_ID # adjust the ID
        if data[i][1] in relevant_IDs: # if its a relevant datapoint
            data[i][2] = float(data[i][2]) # convert string value to float equivalent
            if first_time == -1: # same logic as minID and first data index
                first_time = int(data[i][0])
            data[i][0] = int(data[i][0]) - first_time # normalize time
            relevant_data.append(data[i]) # add it to the ith relevant data spot

''' print(relevant_names) # for debugging purposes
print(variable_names)
print(relevant_IDs)
print(relevant_data) '''

relevant_IDs.sort() # sort relevant IDs so it matches variable_names

for i in range(len(variable_names)):
    variable_names[i][1] = i # normalize IDs

for i in range(len(relevant_data)): # match variable IDs with normalized ID
    relevant_data[i][1] = relevant_IDs.index(relevant_data[i][1])

for i in range(len(relevant_names)):
    relevant_names[i] = variable_names[i][0] # reorder relevant names

''' print(relevant_names) # for debugging purposes
print(variable_names)
print(relevant_IDs)
print(relevant_data) '''

# Adjusted Time, Adjusted ID, Value

last_recorded_speeds = [0, 0, 0, 0]
current_index = 0

adjusted_datas = []

def adjust_data(ID, start_from_zero = True): # start from zero: assume value takes 0 at time stamp 0, otherwise take first recorded value at time stamp 0
    # Linearly interpolate values between updates
    # for example, if two consecutive data entries of (time, value) are (6, 6) and (10, 8), then add in (7, 6.5), (8, 7) and (9, 7.5) between them
    adjusted_data = [-1] * (relevant_data[-1][0] + 1)
    adjusted_data[0] = 0
    last_index = 0

    for i in range(len(relevant_data)):
        if (relevant_data[i][0] == 0) or (not start_from_zero):
            if relevant_data[i][1] == ID:
                adjusted_data[0] = relevant_data[i][2]
                last_index = i
                break
        elif start_from_zero:
            break

    for i in range(len(relevant_data)):
        if relevant_data[i][1] == ID and i != last_index:
            if not relevant_data[i][0] == relevant_data[last_index][0]:
                # There are two entries for ID 8753 at time 1386895 lmao, so this is actually needed
                slope = (relevant_data[i][2] - relevant_data[last_index][2]) * 1.0 / (relevant_data[i][0] - relevant_data[last_index][0])
                for j in range(relevant_data[last_index][0] + 1, relevant_data[i][0] + 1):
                    adjusted_data[j] = relevant_data[last_index][2] + slope * (j - relevant_data[last_index][0])
            else:
                adjusted_data[relevant_data[i][0]] = 0.5 * (relevant_data[last_index][2] + relevant_data[i][2])
            last_index = i
    
    for i in range(len(adjusted_data)):
        if adjusted_data[i] == -1:
            adjusted_data[i] = adjusted_data[i - 1]
    
    return adjusted_data

for i in range(6):
    adjusted_datas.append(adjust_data(i)) # list of all the adjusted data values

# Task goals:
    # miminum speed (MPH)
    # maximum speed (MPH)
    # average speed (MPH)
    # power consumed (all points in race)
    # total energy consumed

# speed: average of four wheels

''' Names: This is just so I can reference the names easily. Note: adjusted_datas[0] does not necessarily correspond to Voltage, this is just the order I originally wrote them in
"Voltage (ams.pack.voltage)", 
"Current (ams.pack.current)", 
"Front Left Wheel Speed (pcm.wheelSpeeds.frontLeft)", 
"Front Right Wheel Speed (pcm.wheelSpeeds.frontRight)", 
"Back Left Wheel Speed (pcm.wheelSpeeds.backLeft)", 
"Back Right Wheel Speed (pcm.wheelSpeeds.backRight)" '''

min_speed = 9999999
max_speed = 0
average_speed = 0
power_consumed = []
total_energy_consumed = 0
front_wheel_speeds = []
back_wheel_speeds = []
for i in range(len(adjusted_datas[0])):
    current_speed = 0.25 * ( # this is how we figure out the normalized index of the variable names
        adjusted_datas[relevant_names.index("Front Left Wheel Speed (pcm.wheelSpeeds.frontLeft)")][i] + 
        adjusted_datas[relevant_names.index("Front Right Wheel Speed (pcm.wheelSpeeds.frontRight)")][i] + 
        adjusted_datas[relevant_names.index("Back Left Wheel Speed (pcm.wheelSpeeds.backLeft)")][i] + 
        adjusted_datas[relevant_names.index("Back Right Wheel Speed (pcm.wheelSpeeds.backRight)")][i]
    ) # speed = average of all four wheel speeds

    front_wheel_speeds.append(0.5 * (adjusted_datas[relevant_names.index("Front Left Wheel Speed (pcm.wheelSpeeds.frontLeft)")][i] + 
        adjusted_datas[relevant_names.index("Front Right Wheel Speed (pcm.wheelSpeeds.frontRight)")][i]))
    back_wheel_speeds.append(0.5 * (adjusted_datas[relevant_names.index("Back Left Wheel Speed (pcm.wheelSpeeds.backLeft)")][i] + 
        adjusted_datas[relevant_names.index("Back Right Wheel Speed (pcm.wheelSpeeds.backRight)")][i]))

    min_speed = min(min_speed, current_speed)
    max_speed = max(max_speed, current_speed)
    average_speed += current_speed

    power_consumed.append(adjusted_datas[relevant_names.index("Voltage (ams.pack.voltage)")][i] * adjusted_datas[relevant_names.index("Current (ams.pack.current)")][i])
        # voltage * current
    total_energy_consumed += (0.5 if (i == 0 or i == len(adjusted_datas[0]) - 1) else 1) * (0.001) * adjusted_datas[
        relevant_names.index("Voltage (ams.pack.voltage)")][i] * adjusted_datas[
        relevant_names.index("Current (ams.pack.current)")][i]
        # power output * time elapsed = work consumed over a time period
        # trapezoidal integration

average_speed /= len(adjusted_datas[relevant_names.index("Front Left Wheel Speed (pcm.wheelSpeeds.frontLeft)")])
# divide by number of datapoints to get average speed

total_energy_consumed /= (3600.0 * 1000.0) # currently in joules; this converts joules to kWh

print("Minimum Speed (MPH): " + str(min_speed)) # 0 MPH
print("Maximum Speed (MPH): " + str(max_speed)) # 49.68 MPH
print("Average Speed (MPH): " + str(average_speed)) # 23.96 MPH
print("Total Energy Consumed (kWh): " + str(total_energy_consumed)) # 4.85 kWh

for i in range(len(power_consumed)):
    power_consumed[i] = str(i + first_time) + " " + str(power_consumed[i]) # de-normalize power

power_json_string = (json.dumps(power_consumed, separators=("\n", ""))[1:-1]).replace("\"", "") # json.dumps() is much faster than adding every entry into a string
    # json.dump() directly to a file is faster than json.dumps(), but it gives less freedom with how the string is formatted

with open("PERData/TaskAPowerConsumed.txt", "w") as outfile: # Output power consumed at every time into a separate file
    outfile.write(power_json_string)

time_array = np.arange(0, len(front_wheel_speeds))

front_wheel_speeds = np.array(front_wheel_speeds)
back_wheel_speeds = np.array(back_wheel_speeds)
 
# Plotting the data
plt.title("Wheel Speed over Time") 
plt.xlabel("Time Elapsed (ms)") 
plt.ylabel("Speed (MPH)") 
plt.plot(time_array, front_wheel_speeds, color = "red") # front wheel speeds logged in red
plt.plot(time_array, back_wheel_speeds, color = "blue") # back wheel speeds logged in blue
plt.show()

print("Time to Run Code : " + str(int((time.time() - start_time) * 100 + 0.5) / 100)) # prints the amount of time the code takes to run, down to 0.01 seconds
# takes roughly 33 seconds