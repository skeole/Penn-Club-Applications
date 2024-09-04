ReadMe for Software Challenge Task B (TaskB.py)

Results:
    Minimum Speed: 0.0 MPH
    Maximum Speed: 97.81 MPH
    Average Speed: 29.16 MPH
    Total Energy Consumed: 4.63 kWh

Time taken to run: roughly 8 seconds

Time Complexity: O(k*(n+t)), where n is the number of lines in the .txt file, k is the number of relevant variables and t is the elapsed time of the race
    k*n is from when we check for if the data point is relevant over all data points
    k*t is from when we linearly interpolate all of the data

Instructions to run and compile code:
1. Change the name of the file where the data is found is on line 6. For me, it was in a folder called PERData, so the file name was "PERData/TaskB.txt"
2. Change the name of the file to which you wish to write the logs for power over time on line 193. For me, it was a file called "TaskBPowerConsumed.txt" in a folder called PERData, so the file name was "PERData/TaskBPowerConsumed.txt"
3. The code is now ready to run!