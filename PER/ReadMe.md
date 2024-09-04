ReadMe for Penn Electric Racing Software Challenge

All results, justifications, speeds, and time complexities, as well as the description of my file for part C, are included within each part's .md file (TaskA.md, TaskB.mb, TaskC.md)

In my opinion, the hardest part was linearly interpolating the data for parts A and B. It was difficult to figure out how to do this effectively, and I think my solution of making a new list rather than trying to insert new data points into an old list was a good way to solve the problem

Tasks A & B
Pros of log file A (csv-like)
    No need to mark number of bytes
    Very clear as to what it does: Timestamp, ID, and Value are easy to read
    ID is not listed in hexadecimal
    Values are listed straight up, not as an endian
Pros of log file B (.txt)
    Because everything is listed in bit form, it's probably easier to write to this file type
    Ability to store multiple pieces of data together under the same ID, rather than hope they are logged at the same time as separate entries

Through this challenge, I learned how to better parse data to both reduce variable size, as well as improve processing speed. I was able to accomplish such parsing methods to efficiently analyze all the data that needed to be analyzed, without wasted RAM. 

To improve performance, I could likely revisit my parsing methods and make it quicker. I frequently use type checking and type casting, which is a very slow operation. 

I made a graph for part A (TaskA_Wheel_Speeds.png), showing the front wheel and back wheel speeds as a function of time. I used numpy and matplotlib to create the graph
    It's somewhat interesting how the wheel speeds are so spiky. Maybe this is due to slight current spikes and dips as the motor rotates and heats up. I'm really not sure, but the end result seems to balance out. Additionally, maybe it could be because the wheels are lifted off the ground temporarily, greatly increasing wheel speed (but not true speed of the car) for the fraction of a second while the car is airborne. Then, the wheels would have a sharp decrease in speed when the car lands again. 
    
    Additionally, I thought the blue and red would be perfectly aligned with each other (after all, it's physically not possible for the back wheels to be moving faster than the front ones), but there are times where the red seems to be slightly slower than the blue, indicating that that does happen sometimes. Maybe this is because the car is in rear wheel drive, where the back wheels are generating all the force for the motion. Maybe there's some loss of energy due to friction when the motion is transferred (back wheels -> car against road -> front wheel), resulting in the back wheel speed being very slightly faster than the car's true speed, which is in turn very slightly faster than the rotational speed of the front wheels. 

To deal with data potentially being sent at different time intervals, I made a linear interpolation of the data to estimate the value of all variables over all milliseconds of the race-not just at the times that the values are updated. 

For part C, I think I could improve the performance by converting the text file into a binary storage format. However, beyond this, I don't see any ways to reduce file size. While converting between .csv and .skeole is slow, I don't necessarily see that as a bad thing. I think the .skeole organizes its data well, and it would be easy to log new data into the structure during a race. 