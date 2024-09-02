import cv2 # import OpenCV Library
import math # import math Library

alternate = True # set this to True to use the rocky background as opposed to the grassy background

video_name = "PennAiR/PennAiR Video Alternate.mp4" if alternate else "PennAiR/PennAiR Video.mp4"

output_video_name = "PennAiR/PennAiR Video Alternate Output.mp4" if alternate else "PennAiR/PennAiRVideo Output.mp4"

window = cv2.VideoCapture(video_name) # creates window from video file

if not window.isOpened():
    raise Exception("Error opening video file") # if there's something wrong when opening file, throw an error

scale = 0.25 # Scaled down to improve processing speed. Note: variables must be tuned for scale
fps = 20     # Target FPS. FPS is also limited by processing speed

output = cv2.VideoWriter(output_video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(window.get(3) * scale), int(window.get(4) * scale)))
    # output video writer

size_threshold = 100 # minimum pixel area for contour to be registered as significant

fx = 2564.3186869 * scale # fx and fy must be scaled for video scaling
fy = 2569.70273111 * scale

f_pixel = math.sqrt(fx * fy) # geometric mean is my favorite way to mean out variables like this

# focal length * real length / pixel length = depth # definition of focal length
# f * (inches per pixel) = depth # inches per pixel is real length / pixel length

# Circle has a pixel area of roughly 29696 * scale^2
# Actual area is 314.159265359
# This means the ratio (inches per pixel) is 0.10285513039 / scale # calculations

pixels_to_inches = 0.10285513039 / scale
depth = f_pixel * pixels_to_inches # flat background so this is a constant

while window.isOpened(): # iterate over all frames in video

    frame_exists, frame_data = window.read()
    
    if frame_exists: # make sure the frame actually exists

        frame_data_modified = cv2.resize(frame_data, (int(window.get(3) * scale), int(window.get(4) * scale)))
            # resizes frame

        t_lower = 100   # Pixels whose neighboring contrast is below here are auto-rejected as not-lines
        t_upper = 145   # pixels above here are auto-accepted as lines
                        # Pixels in are accepted if touching one above upper threshold

        filter = cv2.Canny(frame_data_modified, t_lower, t_upper) # Canny edge filter
        
        filter = cv2.GaussianBlur(filter, (3, 3), 0) # Gaussian blur helps filter out noise

        for i in range(len(filter)):
            for j in range(len(filter[i])):
                if i == 0 or i == len(filter) - 1 or j == 0 or j == len(filter[i]) - 1:
                    filter[i][j] = 255 # put edge as white so we can detect shapes on edge
                elif filter[i][j] < 16:
                    filter[i][j] = 0
                else:
                    filter[i][j] = 255 # binary filter everything to filter out noise

        contours, hierarchies = cv2.findContours(filter, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # binary filter is needed to identify useful contours

        filter.fill(0)
        centers = []
        areas = []
        for contour in contours:
            if size_threshold < cv2.contourArea(contour) < 5000: # < 5000 needed so the background doesn't count as a contour
                M = cv2.moments(contour)
                centers.append([int(M['m10']/M['m00']), int(M['m01']/M['m00'])]) # (x, y) of centroid
                cv2.drawContours(frame_data_modified, [contour], 0, (0, 255, 0), thickness = 2)
                # print(cv2.contourArea(contour)) - this was used to find the circle area to find pixels per inch
    
        for i in centers: # draw the center and the x, y of all contours
            cv2.circle(frame_data_modified, (i[0], i[1]), 3, (255, 255, 255), -1)
            cv2.putText(frame_data_modified, "center", (i[0] - 10, i[1] + 10), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 255, 255), 1)
            cv2.putText(frame_data_modified, "coords: (" + str(int((i[0] - int(window.get(3) * scale * 0.5)) * pixels_to_inches)) + ", " + 
                        str(int((i[1] - int(window.get(4) * scale * 0.5)) * -pixels_to_inches)) + ") inches", (i[0] - 10, i[1] - 10), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 255, 255), 1)
        
        # draw the origin and the image depth
        cv2.circle(frame_data_modified, (int(window.get(3) * scale * 0.5), int(window.get(4) * scale * 0.5)), 3, (255, 255, 255), -1)
        cv2.putText(frame_data_modified, "origin", (int(window.get(3) * scale * 0.5) - 20, int(window.get(4) * scale * 0.5) + 10), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 255, 255), 1)
        cv2.putText(frame_data_modified, "depth: " + str(int(depth)) + " inches", (int(window.get(3) * scale * 0.5) - 20, int(window.get(4) * scale * 0.5) + 20), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 255, 255), 1)

        output.write(frame_data_modified) # write the modified frame to the output video
        cv2.imshow('Shapes', frame_data_modified) # show frame
        
        if (cv2.waitKey(int(1000 / fps)) & 255) == ord('q'):
            break # exit out of loop if q key pressed

    else: # exit out of loop if frame doesn't exist (video is over)
        break

output.release()
window.release()
cv2.destroyAllWindows() # cleanup
