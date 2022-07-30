import pytesseract
import cv2
import numpy as np
import os
from library.contour import contour_run
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])

def zoom_center(img, zoom_factor=1.5):

    y_size = img.shape[0]
    x_size = img.shape[1]
    
    # define new boundaries
    x1 = int(0.5*x_size*(1-1/zoom_factor))
    x2 = int(x_size-0.5*x_size*(1-1/zoom_factor))
    y1 = int(0.5*y_size*(1-1/zoom_factor))
    y2 = int(y_size-0.5*y_size*(1-1/zoom_factor))

    # first crop image then scale
    img_cropped = img[y1:y2,x1:x2]
    return cv2.resize(img_cropped, None, fx=zoom_factor, fy=zoom_factor)

def convert(img,i):
    # Preprocessing the image starts
    # Convert the image to gray scale
    # img = contour_run(frame)
    myfile = open("library/static/counter.txt",'r')
    counter = myfile.read(1)
    myfile.close()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2. imwrite("samples.jpg", img)
    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    
    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    
    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    
    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)
    
    # Creating a copy of image
    im2 = img.copy()
    
    # A text file is created and flushed
    # file = open("recognized.txt", "w+")
    # file.write("")
    # file.close()
    
    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
        
        # Open the file in append mode
        file = open("library/static/pdf/"+counter+".txt", "a")
        
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)
        
        # Appending the text into file
        file.write(text)
        file.write("\n")
        # Close the file
        file.close()
    print("Page "+str(i)+" done!")
    

def ocr():
    path = "library/static/img/" 
    img_list = os.listdir(path)
    
    if len(img_list):
        
        for i in range(0,len(img_list)):
            frame = cv2.imread(path+img_list[i])
            frame = cv2.filter2D(frame, -1, kernel)
            frame = contour_run(frame)
            convert(frame,i)
    else:  
        pass




