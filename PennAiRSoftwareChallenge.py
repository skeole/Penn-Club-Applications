import cv2 # importing OpenCV Library

alternate = False # set this to True to use the rocky background as opposed to the grassy background

video_name = "PennAiR Video Alternate.mp4" if alternate else "PennAiR Video.mp4"

window = cv2.VideoCapture(video_name) # creates window from "PennAiR Video.mp4" file

if not window.isOpened():
    raise Exception("Error opening video file") # if there's something wrong with opening file

scale = 0.25 # note: changing the scale requires other variables to be re-tuned. 
            # currently tuned for scale = 0.25
fps = 25

size_threshold = 100

fx = 2564.3186869 * scale
fy = 2569.70273111 * scale

while window.isOpened(): # over all frames in video

    frame_exists, frame_data = window.read()
    frame_data_modified = cv2.resize(frame_data, (int(window.get(3) * scale), int(window.get(4) * scale)))
        # resizes OpenCV frame
    
    if frame_exists:

        t_lower = 100    # Pixels below here are auto-rejected as not-lines
                        # Pixels between are accepted if touching one above upper threshold
        t_upper = 145   # pixels above here are auto-accepted as lines

        # Applying the Canny Edge filter
        filter = cv2.Canny(frame_data_modified, t_lower, t_upper)
        
        filter = cv2.GaussianBlur(filter, (3, 3), 0)

        for i in range(len(filter)):
            for j in range(len(filter[i])):
                if i == 0 or i == len(filter) - 1 or j == 0 or j == len(filter[i]) - 1:
                    filter[i][j] = 255 # this is so we can detect shapes on the edge
                elif filter[i][j] < 16:
                    filter[i][j] = 0
                else:
                    filter[i][j] = 255

        contours, hierarchies = cv2.findContours(filter, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        filter.fill(0)
        centers = []
        for contour in contours:
            if size_threshold < cv2.contourArea(contour) < 5000:
                M = cv2.moments(contour)
                centers.append([int(M['m10']/M['m00']), int(M['m01']/M['m00'])])
                cv2.drawContours(filter, [contour], 0, 255, thickness = 2)

        for i in range(len(filter)):
            for j in range(len(filter[i])):
                if filter[i][j] == 255:
                    frame_data_modified[i][j] = (0, 255, 0)
        
        x_scale = 1
        y_scale = 1

        # how does length relate to pixels: pixels = length *
        # true length = depth *  
        for i in centers:
            cv2.circle(frame_data_modified, (i[0], i[1]), 3, (255, 255, 255), -1)
            cv2.putText(frame_data_modified, "center", (i[0] - 10, i[1] + 10), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 255, 255), 1)
            cv2.putText(frame_data_modified, "coords: [" + str(int((i[0] - int(window.get(3) * scale * 0.5)) / x_scale)) + ", " + 
                        str(int((i[1] - int(window.get(4) * scale * 0.5)) / -y_scale)) + "]", (i[0] - 10, i[1] - 10), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 255, 255), 1)
        
        cv2.circle(frame_data_modified, (int(window.get(3) * scale * 0.5), int(window.get(4) * scale * 0.5)), 3, (255, 255, 255), -1)
        cv2.putText(frame_data_modified, "origin", (int(window.get(3) * scale * 0.5) - 20, int(window.get(4) * scale * 0.5) + 10), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 255, 255), 1)

        cv2.imshow('Shapes', frame_data_modified) # show frame
        
        if (cv2.waitKey(int(1000 / fps)) & 255) == ord('q'):
            break # exit out of loop if q key pressed

    else: # exit out of loop if frame doesn't exist (video is over)
        break

window.release()
cv2.destroyAllWindows() # cleanup
