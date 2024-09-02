import time

start_time = time.time()

with open("PERData/TaskB.txt") as fileInput: # CSV-Like Format: Timestamp, ID, Value
    data = list(fileInput)
    data.pop(0)

hex_alphabet = "0123456789ABCDEF"
def hex_to_decimal(hex_string):
    hex_string = hex_string.upper()
    if hex_string[:2] == "0X":
        hex_string = hex_string[2:]
    value = 0
    counter = 0
    for i in range(len(hex_string) - 1, -1, -1):
        value += hex_alphabet.index(hex_string[i]) * (16 ** counter)
        counter += 1
    return value

relevant_IDs = [
    hex_to_decimal("0x311"), # Battery Current
    hex_to_decimal("0x313"), # Battery Voltage
    hex_to_decimal("0x222")  # Front Wheel RPM
]

def time_to_seconds(time_string):
    time_ = time_string.split(":")
    return int(time_[0]) * 3600 + int(time_[1]) * 60 + float(time_[2])

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
relevant_data = []
for i in data:
    i = i.strip()
    if i == "":
        continue
    
    i = i.split(" [ ")
    i[0] = i[0].split(" ")
    if starting_time == -1:
        starting_time = time_to_seconds(i[0][0])
    time_stamp = round((time_to_seconds(i[0][0]) - starting_time) * 1000) # time stamp in milliseconds

    id = hex_to_decimal(i[0][1] + i[0][2][2:])
    
    if id in relevant_IDs:

        i[1] = i[1][:-1]
        i[1] = i[1].split(", ")
        for j in range(len(i[1])):
            i[1][j] = int(i[1][j])
        
        if len(i[1]) == 4:
            i[1] = [bytes_to_float(i[1][0], i[1][1], i[1][2], i[1][3])]
        else:
            i[1] = [bytes_to_float(i[1][0], i[1][1], i[1][2], i[1][3]), bytes_to_float(i[1][4], i[1][5], i[1][6], i[1][7])]
        
        relevant_data.append([time_stamp, id, i[1]])

# print(bytes_to_float(217, 184, 130, 65)) # should be 16.340258
# print(bytes_to_float(122, 175, 137, 65)) # should be 17.210682

print("Setup Time : " + str(int((time.time() - start_time) * 100 + 0.5) / 100)) # takes roughly 2.5 seconds to parse and organize all the data