ReadMe for Software Challenge Task A (TaskA.py)

Results:
    Minimum Speed: 0.0 MPH
    Maximum Speed: 49.68 MPH
    Average Speed: 23.96 MPH
    Total Energy Consumed: 4.85 kWh

The output file is saved to TaskA_Wheel_Speeds.png
    Front wheel speed is logged in red, while back wheel speed is logged in blue

Time taken to run: roughly 33 seconds

Time Complexity: O(k*(n+t)), where n is the number of data points in the .csv file, k is the number of relevant variables and t is the elapsed time of the race
    k*n is from when we check for if the data point is relevant over all data points
    k*t is from when we linearly interpolate all of the data

Instructions to run and compile code:
1. Ensure numpy (pip3 install numpy) and matplotlib (pip3 install matplotlib) are both installed
2. Change the name of the file where the data is found is on line 9. For me, it was in a folder called PERData, so the file name was "PERData/TaskA.csv"
3. Change the name of the file to which you wish to write the logs for power over time on line 185. For me, it was a file called "TaskAPowerConsumed.txt" in a folder called PERData, so the file name was "PERData/TaskAPowerConsumed.txt"
4. The code is now ready to run!