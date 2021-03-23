import cv2 as cv
import random, string, os

cap = cv.VideoCapture(0)
BB_coordinates = [] # bounding box coordinates list, [top left corner, bottom right corner] - # needed for creating samples later

def getImageLabel():
    return input("Enter your name and the object you will be capturing/handling (in the format 'objectName'): ")
    

# ensures that images can be placed into correct folders
def generateDirectories():
    try: 
        os.mkdir("{}_data".format(prefix))
        try:
            os.mkdir("{}_data/{}_positives".format(prefix, prefix))
            os.mkdir("{}_data/{}_negatives".format(prefix, prefix))
            print("Image directories created")
        except OSError as error:
            print("Image directories found")

    except OSError as error:
        print("Image data directory found")
    

# generates description for each negative image in the required format - https://docs.opencv.org/4.2.0/dc/d88/tutorial_traincascade.html
def generateNegativesDescription():
    with open("{}_data/negativesDescription.txt".format(prefix),"w") as f:
        files = os.listdir("{0}_data/{0}_negatives".format(prefix))
        for file in files:
            f.write("{}_negatives/".format(prefix) + file + "\n")
    f.close()

# procedure to capture positive and negative images
def imageCapturer():

    # gets current amount of files - also assigns an ID to each file created later, avoiding overwriting
    positive_count = len(os.listdir("{}_data/{}_positives".format(prefix, prefix)))
    negative_count = len(os.listdir("{}_data/{}_negatives".format(prefix, prefix)))

    print("""Press P to capture a positive
N to capture a negative
Q to quit""")
    while True:
        # reads the current frame from the webcam
        ret, frame = cap.read()

        # flips camera horizontally
        frame = cv.flip(frame, 1)

        # creates a cv2 window to show webcam feed
        cv.imshow("Capture", frame)
    
        pressed_key = cv.waitKey(1)

        if pressed_key == ord('q'): # if user presses 'q' it closes cv windows and leaves the while loop
            cv.destroyAllWindows() 
            break

        elif pressed_key == ord('p'): # if p the program saves the current frame to the positives folder
            positive_count += 1 # increments number of files created assuming files are not overwritten
            cv.imwrite('{0}_data/{0}_positives/{1}.jpg'.format(prefix, prefix + str(positive_count)), frame)

            print("Positives captured: " + str(positive_count)) # tells user how many positives they have created

        elif pressed_key == ord('n'): # if n the program saves the current frame to the negatives folder
            negative_count += 1 # increments number of files created assuming files are not overwritten
            cv.imwrite('{0}_data/{0}_negatives/{1}.jpg'.format(prefix, prefix + str(negative_count)), frame)
 
            print("Negatives captured: " + str(negative_count)) # tells user how many negatives they have created
    
    cap.release() # stops camera feed

#def drawBoundingBox(event, x, y, flags, param):

def generatePositiveDescription(imagesData):
    with open("positivesDescription.txt","w") as f:
        for data in imagesData:
            f.write(data + "\n")
    f.close()

def positiveAnnotation():
    images = [] # list of image and box data - "positives/image.jpg 0 1 1 640 480" - necessary format for opencv_createsamples
    for file in os.listdir("positives"): # cycles through positive images
        imageData = "" # creates empty string for image data
        image = cv.imread(os.path.join("positives", file)) # sets current frame to current image
        if image is not None: # if the image exists 
            imageData += "positives/{}".format(file) # adds the filename to the imageData
            imageAnnotated = False # control variable for while loop
            cv.imshow(file, image) # creates window of current image
            cv.moveWindow(file,100, 100) # opens all windows in this position - even if dragged elsewhere, !! could be fixed

            while imageAnnotated == False: # loop until the user is happy with their bounding box
                pressed_key = cv.waitKey(1)
                if pressed_key == ord("q"): # if the user presses q quit the program
                    cv.destroyAllWindows()
                    break
                    
                elif pressed_key == ord("n"): # if the user presses n handle the necessary data and change to the next image
                    cv.destroyWindow(file)
                    imageAnnotated = True

                    images.append(imageData)
                    print(images)
            if pressed_key == ord("q"): # quits out of for loop
                break
    generatePositiveDescription(images)




def main():
    userQuit = False

    while userQuit == False:
        global prefix
        prefix = getImageLabel()

        if prefix is not "":
            generateDirectories()

            if input("Enter 'C' to enter Image Capturer mode: ") == "C":
                imageCapturer()
                generateNegativesDescription()

            #if input("Enter 'A' to enter annotation mode: ") == "A":
                #positiveAnnotation()
        else:
            print("Enter a label")

        if input("Enter Q to quit or nothing to capture more images: ") == "Q":
            userQuit = True
    

main()
