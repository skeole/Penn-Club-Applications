import time
import json

start_time = time.time()

with open("PERData/TaskB.txt") as fileInput: # Timestamp, ID, Bit Quantity, Bit Array
    data = list(fileInput)
    data.pop(0) # remove the first entry, which is just a header

hex_alphabet = "0123456789ABCDEF"
def hex_to_decimal(hex_string): # converts a hex string to its hexadecimal coutnerpart
    hex_string = hex_string.upper() # so there's no issue if its "1a" or "1A"
    if hex_string[:2] == "0X": # 0x can mean a number is hexadecimal, so this removes 0x if the string starts with it
        hex_string = hex_string[2:]
    value = 0
    counter = 0
    for i in range(len(hex_string) - 1, -1, -1):
        value += hex_alphabet.index(hex_string[i]) * (16 ** counter)
        counter += 1
    return value

relevant_IDs = [ # not sorted descending to ascending
    hex_to_decimal("0x311"), # Battery Current
    hex_to_decimal("0x313"), # Battery Voltage
    hex_to_decimal("0x222")  # Front Wheel RPM
]

unsorted_names = ["Battery Current", "Battery Voltage", "Front Wheel RPM"]

IDs = relevant_IDs.copy()
IDs.sort()

sorted_names = unsorted_names.copy()
for i in range(len(sorted_names)):
    sorted_names[i] = unsorted_names[relevant_IDs.index(IDs[i])] # sorts both names and IDs in ascending order

def time_to_seconds(time_string): # converts the hour timestamp to seconds
    time_ = time_string.split(":")
    return int(time_[0]) * 3600 + int(time_[1]) * 60 + float(time_[2])

# the following four methods are used to convert little endians to their values as floats

def byte_to_bits(byte):
    bits = []
    for i in range(8):
        bits.insert(0, round(byte % 2))
        if bits[0] == 1:
            byte -= 1
        byte /= 2
    return bits

def binary_to_digits(binary):
    number = 0
    counter = 0
    for i in range(len(binary) - 1, -1, -1):
        number += binary[i] * (2 ** counter)
        counter += 1
    return number

def solve_mantissa(mantissa, exponent):
    true_exponent = exponent
    number = 2 ** exponent
    for i in mantissa:
        true_exponent -= 1
        number += i * (2 ** true_exponent)
    return number

def bytes_to_float(byte_one, byte_two, byte_three, byte_four):

    bits = []

    for i in byte_to_bits(byte_four):
        bits.append(i)
    for i in byte_to_bits(byte_three):
        bits.append(i)
    for i in byte_to_bits(byte_two):
        bits.append(i)
    for i in byte_to_bits(byte_one):
        bits.append(i)
    
    sign = 1 - 2 * bits[0] # 0 -> positive, 1 -> negative
    exponent = binary_to_digits(bits[1:9]) - 127
    solved_mantissa = solve_mantissa(bits[9:], exponent)

    return solved_mantissa * sign

starting_time = -1
relevant_data = [[], [], []] # same as in part A
highest_time = -1
for i in data:
    i = i.strip()
    if i == "": # so nothing gets messed up if the line is empty
        continue
    
    i = i.split(" [ ") # splits it before the bit array
    i[0] = i[0].split(" ") # splits first part into [Timestamp, ID part 1, ID part 2, bit quantity]
    if starting_time == -1:
        starting_time = time_to_seconds(i[0][0])
    time_stamp = round((time_to_seconds(i[0][0]) - starting_time) * 1000) # time stamp in milliseconds
        # convert to ms so there's no weird float error where its like 365.956000000000002 seconds
    highest_time = time_stamp

    id = hex_to_decimal(i[0][1] + i[0][2][2:])
    
    if id in relevant_IDs:

        converted_ID = IDs.index(id)

        i[1] = i[1][:-1]
        i[1] = i[1].split(", ")
        for j in range(len(i[1])):
            i[1][j] = int(i[1][j])
        
        if len(i[1]) == 4:
            i[1] = bytes_to_float(i[1][0], i[1][1], i[1][2], i[1][3])
        else:
            i[1] = (bytes_to_float(i[1][0], i[1][1], i[1][2], i[1][3]) + bytes_to_float(i[1][4], i[1][5], i[1][6], i[1][7])) * 0.5
            # record the average of the FL and FR wheels
        
        if abs(i[1]) > 1000000: # something was probably corrupted in the data
            continue # ignore this datapoint and move on
        else:
            relevant_data[converted_ID].append([time_stamp, i[1]])

# print(bytes_to_float(217, 184, 130, 65)) # should be 16.340258
# print(bytes_to_float(122, 175, 137, 65)) # should be 17.210682
# debugging purposes to ensure little endian to float converter was working correctly

def adjust_data(converted_ID, start_from_zero = True): # start from zero: assume value takes 0 at time stamp 0, otherwise take first recorded value at time stamp 0
    # Linearly interpolate values between updates
    # data comes in [time, value] packets
    # same idea as in part A, although I think the code might read a little different in a few places because I parsed the data slightly differently for part B

    current_data = relevant_data[converted_ID]
    adjusted_data = [-1] * (highest_time + 1)
    adjusted_data[0] = current_data[0][1] if ((not start_from_zero) or (current_data[0] == 0)) else 0
    last_index = 0
    current_data.insert(0, [0, adjusted_data[0]])

    for i in range(len(current_data)):
        if i != last_index:
            if current_data[i][0] != current_data[last_index][0]: # Just in case lol
                slope = (current_data[i][1] - current_data[last_index][1]) * 1.0 / (current_data[i][0] - current_data[last_index][0])
                for j in range(current_data[last_index][0] + 1, current_data[i][0] + 1):
                    adjusted_data[j] = current_data[last_index][1] + slope * (j - current_data[last_index][0])
            else:
                adjusted_data[current_data[i][0]] = 0.5 * (current_data[last_index][1] + current_data[i][1])
            last_index = i
    
    for i in range(len(adjusted_data)):
        if adjusted_data[i] == -1:
            adjusted_data[i] = adjusted_data[i - 1]
    
    return adjusted_data

for i in range(3):
    relevant_data[i] = adjust_data(i, start_from_zero = False)

# Names: "Battery Current", "Battery Voltage", "Front Wheel RPM" # Just for reference. Again, these names are not sorted
min_speed = 9999999
max_speed = 0
average_speed = 0
power_consumed = []
total_energy_consumed = 0

for i in range(len(relevant_data[0])):
    current_speed = relevant_data[sorted_names.index("Front Wheel RPM")][i] * (20.5) * (3.1415926536) * 60.0 / 63360.0
        # convert RPM into MPH

    min_speed = min(min_speed, current_speed)
    max_speed = max(max_speed, current_speed)
    average_speed += current_speed

    power_consumed.append(relevant_data[sorted_names.index("Battery Current")][i] * relevant_data[sorted_names.index("Battery Voltage")][i])
    total_energy_consumed += (0.5 if (i == 0 or i == len(relevant_data[0]) - 1) else 1) * (0.001) * relevant_data[
        sorted_names.index("Battery Current")][i] * relevant_data[sorted_names.index("Battery Voltage")][i]
        # trapezoidal integration

average_speed /= len(relevant_data[0]) # same as part A

total_energy_consumed /= (3600.0 * 1000.0) # same as part A

print("Minimum Speed (MPH): " + str(min_speed)) # 0 MPH
print("Maximum Speed (MPH): " + str(max_speed)) # 97.81 MPH
print("Average Speed (MPH): " + str(average_speed)) # 29.16 MPH
print("Total Energy Consumed (kWh): " + str(total_energy_consumed)) # 4.63 kWh

for i in range(len(power_consumed)):
    power_consumed[i] = str(round(i + starting_time * 1000)) + " " + str(power_consumed[i])

power_json_string = (json.dumps(power_consumed, separators=("\n", ""))[1:-1]).replace("\"", "")

with open("PERData/TaskBPowerConsumed.txt", "w") as outfile: # same as part A
    outfile.write(power_json_string)

print("Time to Run Code : " + str(int((time.time() - start_time) * 100 + 0.5) / 100))
# takes roughly 8 seconds