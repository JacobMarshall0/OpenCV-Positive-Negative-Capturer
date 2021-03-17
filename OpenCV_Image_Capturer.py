import cv2 as cv
import os

cap = cv.VideoCapture(0)

# ensures that images can be placed into correct folders
def generateDirectories():
    try:
        os.mkdir("positives")
        os.mkdir("negatives")
    except OSError as error:
        print("Directory already exists")
    
generateDirectories()

# gets current amount of files - also assigns an ID to each file created later, avoiding overwriting
positive_count = len(os.listdir("positives"))
negative_count = len(os.listdir("negatives"))

while True:
    # reads the current frame from the webcam
    ret, frame = cap.read()

    # flips camera horizontally
    frame = cv.flip(frame, 1)

    # creates a cv2 window to show webcam feed
    cv.imshow("Capture", frame)
    
    pressed_key = cv.waitkey(1)
    
    if pressed_key == ord('q'): # if user presses 'q' it closes cv windows and leaves the while loop
        cv.destroyAllWindows() 
        break

    elif pressed_key == ord('p'): # if p the program saves the current frame to the positives folder
        positive_count += 1 # increments number of files created assuming files are not overwritten
        cv.imwrite('positives/{}.jpg'.format(positive_count), frame)

        print("Positives captured: " + str(positive_count)) # tells user how many positives they have created

    elif pressed_key == ord('n'): # if n the program saves the current frame to the negatives folder
        negative_count += 1 # increments number of files created assuming files are not overwritten
        cv.imwrite('negatives/{}.jpg'.format(negative_count), frame)
 
        print("Negatives captured: " + str(negative_count)) # tells user how many negatives they have created
    

cap.release() # stops camera feed


