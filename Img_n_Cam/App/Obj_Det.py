import cv2, time
from datetime import datetime
import pandas as pd

first_frame = None
video = cv2.VideoCapture(0)
status_lst = [None, None]
timeStamp = []

check, first_frame = video.read()
if check:
    first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    first_frame = cv2.GaussianBlur(first_frame, (21,21), 0)
    # Adding Gaussian Blur using gaussian kernel to remove noise and increase accuracy in calculating the difference
    # The tuple represents the size of the kernel and the 3rd parameter is the standard deviation
    # Now that the reference frame is captured we go on to do our job

    while True:
        check, frame = video.read()
        status = 0  # Motion in frame (0 = no motion in the frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21,21), 0)     

        # Lets calculate delta frame using absolute difference
        delta_frame = cv2.absdiff(first_frame, gray)
        # Lets use an intensity of 30 as our threshold, and set those above to 255 using threshold method of cv2
        threshhold_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
        # The threshold function returns a tuple with first value
        # just in case some other threshold metod is used

        # Now one thing we should do is, get rid of those black holes in the big white regions
        # We can do this by dilate those 
        threshhold_frame = cv2.dilate(threshhold_frame, None, iterations = 2)
        # If we had a kernel array and wanted for this process to be a sophisticated one
        # we'd pass it instead of None. But we don;t need it over here
        # Higher the number of iterations smoother the image. Defines the number of times it goes through the image to remove the holes

        # Next we find the contours of the dilated threshold frames
        # Contour detection in openCV can be done using findContours or drawContours
        # findContours finds and stores contours in a tuple while the draw one draws
        (cnts, _) = cv2.findContours(threshhold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #p1 = frame to find contour from
        #p2 = method to find. Here we want to draw the external contours
        #p3 = Approximation method that openCV will apply to retrieve the contours
        
        # Now we filter out some contours (larger than certain area)

        for cont in cnts:
            if cv2.contourArea(cont) < 10000:
                continue
            #If the contours are small, skip them
            #else draw a rectangle around it
            status = 1

            (x, y, w, h) = cv2.boundingRect(cont)    #Rectangle bounding the contour
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)
        
        status_lst.append(status)
        if status_lst[-1] == 1 and status_lst[-2] == 0:
            timeStamp.append(datetime.now())
        
        elif status_lst[-1] == 0 and status_lst[-2] == 1:
            timeStamp.append(datetime.now())
            
        cv2.imshow("The Detecting Frame", frame)
        cv2.imshow("Capturing_gray", gray)
        cv2.imshow("Delta Frame", delta_frame)
        cv2.imshow("ThresholdFrame", threshhold_frame)

        key = cv2.waitKey(1)
        #print(delta_frame)
        print(status)
        
        if key == ord('q'):
            cv2.destroyAllWindows()
            video.release()
            if status == 1:
                timeStamp.append(datetime.now())
            break
else:
    print("Failed: Maybe there was a camera issue")

# Now lets store the list of timestamp into a DataFrame
df = pd.DataFrame(columns = ["Start", "End"])
for i in range(0, len(timeStamp), 2):
    df = df.append({"Start" : timeStamp[i], "End": timeStamp[i+1]}, ignore_index = True)
df.to_csv("Times_Stamps.csv")