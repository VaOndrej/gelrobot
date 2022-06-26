import tkinter
from tkinter import filedialog
import cv2
import math

def save_file():
    root = tkinter.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    vs = cv2.VideoCapture(str(file_path))
    success, frame = vs.read()

    while success:
        success, frame = vs.read()
        cv2.imwrite("robot.jpg", frame)  # save frame as JPEG
        break

# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell

        i = 0
        # Change this value if needed
        r = 36
        PI = 3.14
        # displaying circle
        while i < 360:
            angle = i
            x1 = r * math.cos(angle * PI / 180)
            y1 = r * math.sin(angle * PI / 180)
            # this should be moved and checked against chaned.jpg.
            img[int(y + y1), int(x + x1)] = i, 0, 0
            i = i + 1    
            
        print(f"X axis robot coordinate: {x}")
        print(f"Y axis robot coordinate: {y}")
        print(f"Chosen diameter for circle: {r}")
        cv2.imshow('image', img)
 
 
    # checking for right mouse clicks    
    if event==cv2.EVENT_MBUTTONDBLCLK:
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        print(f"R={r}, G={g}, B={b}")
    
 
if __name__=="__main__":
    print("Please choose video file")
    save_file()    
    print("Saved robot file for further processing named -> robot.jpg")
    print("In this step please choose middle of the gel robot")
        # reading the image
    img = cv2.imread('robot.jpg', 1)
 
    # displaying the image
    cv2.imshow('image', img)


    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)
    
    print("To exit press any key")
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
 
    # close the window
    cv2.destroyAllWindows()
    
    