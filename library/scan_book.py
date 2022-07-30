import cv2
from datetime import datetime
import os, shutil
from PIL import Image
from library.ocr_convertor import zoom_center

camera = cv2.VideoCapture(0)
start_scan=0
capture=0
stop_scan=0

def get_now_string():

    # Return the current date time in this format: "YYYYMMDD_HHMMSS_microsecond".

    now = datetime.now()
    now_string = now.strftime("%Y") + now.strftime("%m") + now.strftime("%d") + '_' + now.strftime("%H") + now.strftime("%M") + now.strftime("%S") + '_' + now.strftime("%f")
    return now_string

def write_frame(frame):

    # Write the video frame to a JPEG file.

    now_string = get_now_string()
    cv2.imwrite("%s_%s.jpg" % ('library\\static\\img\\', now_string), frame)

def gen_frames(): 
    global capture 
    if not (camera.isOpened()):
        print("Could not open camera.")
        return 1
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame= zoom_center(frame,1.5)
            frame = cv2.rotate(frame, cv2.ROTATE_180)

            ret, buffer = cv2.imencode('.jpg', frame)
            if capture:
                write_frame(frame)
                capture=0
            
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
    camera.release()
    
def capture_frame():
    global capture
    capture=1

def startscan():
    path = "library/static/"
    try: 
        os.mkdir(path+"img") 
    except OSError as error: 
        print(error)

def img_to_pdf():

    path = "library/static/"
    
    img_list = os.listdir(path+"img/")
    images=[]

    myfile = open(path+"counter.txt",'r')
    counter = myfile.read(1)
    myfile.close()
    
    
    if len(img_list):
        img1=Image.open(path+"img/"+img_list[0])
        im_1 = img1.convert('RGB')
        
        for i in range(1,len(img_list)):
            img=Image.open(path+"img/"+img_list[i])
            im = img.convert('RGB')
            images.append(im)
        # print(images)
        im_1.save(path+"pdf/"+counter+".pdf", save_all=True, append_images=images)
        
        counter=str(int(counter)+1)
        myfile = open(path+"counter.txt",'w')
        myfile.write(counter)
        myfile.close()

        shutil.rmtree(path+"img/")

    else:  
        pass

