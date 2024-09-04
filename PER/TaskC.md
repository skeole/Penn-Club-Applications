ReadMe for Software Challenge Task C (TaskC_Encoder.py, TaskC_Decoder.py, and TaskC_Verification.py)

Custom file format: .skeole
    Requirements for converting from .csv to .skeole:
    - IDs must be sorted with smallest one first in the .csv (ones after this do not need to be in order)
    - The first datapoint in the csv must be the earliest time
    - Datapoints corresponding to same can ID must be arranged by increasing time
        - They do not have to be consecutive
    - The difference between the smallest and largest CAN IDs must be less than or equal to 2^12 - 2
        - This was just a design choice though, it probably wouldn't be all that hard to make this adapt to any range of CAN IDs

    Here is how the data is organized:

    {
        { // General Variables
            Log Date, 
            Log Time, 
            ID_Shifter, 
            Starting_Time
        }, { // First variable
            Name, 
            Time Stamp 1, 
            Value 1, 
            Time Stamp 2, 
            Value 2, ...
        }, { // Second variable
            Name, 
            Time Stamp 1, 
            Value 1, 
            Time Stamp 2, 
            Value 2, ...
        }, ...
    }

Results: compressed a 285 MB .csv into a 204 MB .skeole file, which is a reduction of roughly 30%

Time taken to run:
    Encoding (.csv to .skeole): roughly 50 seconds
    Decoding: roughly 35 seconds
    Verification: roughly 40 seconds

Time Complexity:
    Encoding: O(n), where n is the number of data points in the .csv file
        Adding a data point takes more time than adding a variable because there are type conversions that occur
    
    Decoding: O(n), where n is the number of total second-degree entries in the list corresponsing to the .skeole file
        I might not have been clear with that definition, so let me give an example: if the list corresponding to the .skeole filt is [[1, 2, 3, 4], [5, 6, 7, 8]], that would be 8 (not 2) second-degree entries

    Verification: O(n), where n is the number of data points in the .txt file
        This is the same as the time complexity of encoding, because verification is just encoding with an equality condition attached to the end. However, we use a .txt file here instead of a .csv file

Instructions to run and compile code:
    TaskC_Encoder.py:
        1. Change the name of the file where the data is found is on line 29. For me, it was in a folder called PERData, so the file name was "PERData/TaskA.csv"
        2. Change the name of the file to which you wish to write the converted .skeole file on line 69. For me, it was a file called "TaskCEncoded.skeole" in a folder called PERData, so the file name was "PERData/TaskCEncoded.skeole"
        3. The code is now ready to run!
    
    TaskC_Decoder.py
        1. Change the name of the file where the already-encoded.skeole file is found is on line 6. For me, it was in a folder called PERData, so the file name was "PERData/TaskCEncoded.skeole"
        2. Change the name of the file to which you wish to write the decoded-and-encoded file on line 53. For me, it was a file called "TaskCEncodedAndDecoded.txt" in a folder called PERData, so the file name was "PERData/TaskCEncodedAndDecoded.txt"
        3. The code is now ready to run!
    
    TaskC_Verification.py
        1. Change the name of the file where the encoded-and-decoded .txt file is found is on line 13. For me, it was in a folder called PERData, so the file name was "PERData/TaskCEncodedAndDecoded.txt"
        2. Change the name of the file where the already-encoded.skeole file is found is on line 55. For me, it was in a folder called PERData, so the file name was "PERData/TaskCEncoded.skeole"
        3. The code is now ready to run!
        4. If the code outputs "Encoding and Decoding is lossless!" once it is done running, that means the file conversion works. If it outputs "Something went wrong" instead, that means the file conversion is flawed somewhere. 