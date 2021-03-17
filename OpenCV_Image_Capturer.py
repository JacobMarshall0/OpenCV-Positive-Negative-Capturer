import cv2 as cv
import random, string, os

cap = cv.VideoCapture(0)

# ensures that images can be placed into correct folders
def generateDirectories():
    try:
        os.mkdir("positives")
        os.mkdir("negatives")
        print("Image directories created")
    except OSError as error:
        print("Image directories found")

# generates description for each negative image in the required format - https://docs.opencv.org/4.2.0/dc/d88/tutorial_traincascade.html
def generateNegativesDescription():
    with open("negativesDescription.txt","w") as f:
        files = os.listdir("negatives")
        for file in files:
            f.write("negatives/" + file + "\n")

# procedure to capture positive and negative images
def imageCapturer():

    prefix = input("Enter a prefix for the image names: ")
    # gets current amount of files - also assigns an ID to each file created later, avoiding overwriting
    positive_count = len(os.listdir("positives"))
    negative_count = len(os.listdir("negatives"))

    print("Press P to capture a positive, N to capture a negative, and Q to quit")
    while True:
        # reads the current frame from the webcam
        ret, frame = cap.read()

        # flips camera horizontally
        frame = cv.flip(frame, 1)

        # creates a cv2 window to show webcam feed
        cv.imshow("Capture", frame)
    
        char = cv.waitKey(1)

        if char == ord('q'): # if user presses 'q' it closes cv windows and leaves the while loop
            cv.destroyAllWindows() 
            break

        elif char == ord('p'): # if p the program saves the current frame to the positives folder
            positive_count += 1 # increments number of files created assuming files are not overwritten
            cv.imwrite('positives/{}.jpg'.format(prefix + str(positive_count)), frame)

            print("Positives captured: " + str(positive_count)) # tells user how many positives they have created

        elif char == ord('n'): # if n the program saves the current frame to the negatives folder
            negative_count += 1 # increments number of files created assuming files are not overwritten
            cv.imwrite('negatives/{}.jpg'.format(prefix + str(negative_count)), frame)
 
            print("Negatives captured: " + str(negative_count)) # tells user how many negatives they have created
    
    cap.release() # stops camera feed

def main():
    generateDirectories()
    imageCapturer()
    generateNegativesDescription()

main()
