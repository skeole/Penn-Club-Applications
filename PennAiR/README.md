# PennAiR Software Challenge

I created two versions of the code: one that specifically solves this puzzle (to find shapes with a solid or gradient color on a noisy background) and a second, more general one that attempts to find any shape against a background, regardless of if the shapes are noisy as well. 

Note: because the general challenge is so much more difficult, it isn't completed (I might continue to work on it after I submit my club applications because it seems interesting to me). It struggles when there is a break in the continuity of the contrast between shape and background (i.e. when one part of the shape camouflages well into the background). To finish this extension of the challenge I need to figure out how to extend a line in opencv. 

To run the code:
1. Make sure the OpenCv is installed on the machine (run "pip3 install opencv-python" in terminal)
2. Change the variables in lines 4 (setting alternate to 'True' will make the code analyze the video with gradient shapes on a rocky background, while setting it to 'False' will make the code analyze the video with solid shapes on a grassy background), 6 (make sure the strings correspond with the file names of the two videos), and 8 (same as 6, but for where you want the resulting video to output) of whichever file you wish to run
3. The code is now ready to run!