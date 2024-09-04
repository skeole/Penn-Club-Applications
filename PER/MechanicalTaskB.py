# This file is only for the mechanical challenge, NOT for the electrical software challenge

import math

metal_names = ["A", "B", "C", "D"]
metal_costs = [7500, 15000, 8000, 2000] # dollars per kilogram
metal_densities = [4920, 1740, 3070, 7850] # kilograms per cubic meter
metal_resistivities = [4.8 * (10 ** -8), 3.6 * (10 ** -8), 7.9 * (10 ** -8), 2.2 * (10 ** -7)] # ohm-meters
metal_specific_heats = [335, 193, 456, 149]

wire_length = 0.1 # meters
wire_amperage = 100 # amperes
time_duration = 2255 # seconds
temperature_increase = 15 # Kelvin or degrees Celsius

def area(metal_name): # square meters
    index = metal_names.index(metal_name)
    return math.sqrt((wire_amperage * wire_amperage * time_duration * metal_resistivities[index]) / (temperature_increase * metal_densities[index] * metal_specific_heats[index]))

def price(metal_name): # dollars
    index = metal_names.index(metal_name)
    return area(metal_name) * wire_length * metal_costs[index] * metal_densities[index]

metal_cross_sectional_areas = [] # square meters
for i in metal_names:
    metal_cross_sectional_areas.append(area(i))
    print("For metal " + i + ", the cross-sectional area is " + str(round(area(i) * 10000 * 1000) * 0.001) + " square centimeters, with a price of " + str(round(price(i) * 100) * 0.01) + " dollars.")

# A: 2.092 square centimeters, $772.09
# B: 4.014 square centimeters, $1047.77
# C: 2.913 square centimeters, $715.35
# D: 5.318 square centimeters, $834.85

# Verification - I couldn't figure out an easy way to calculate it without a straight-up calculation, so I used this to verify the calculated cross-sectional areas indeed give a temperature increase of 15 Kelvin
print()

def resistance(metal_name):
    index = metal_names.index(metal_name)
    return metal_resistivities[index] * wire_length / metal_cross_sectional_areas[index]

def power(metal_name):
    return wire_amperage * wire_amperage * resistance(metal_name)

def thermal_energy_transfer(metal_name):
    return power(metal_name) * time_duration

def mass(metal_name):
    index = metal_names.index(metal_name)
    return metal_densities[index] * metal_cross_sectional_areas[index] * wire_length

def change_in_temperature(metal_name):
    index = metal_names.index(metal_name)
    return thermal_energy_transfer(metal_name) / (mass(metal_name) * metal_specific_heats[index])

for i in metal_names: # uncomment this if you want to verify; but they're all around 15 degrees so we're good
    print(change_in_temperature(i))