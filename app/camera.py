import cv2
import os # to get the PATH odf the haarcascade

class VideoCamera(object):
    cas="haarcascade_frontalface_alt.xml"
    face_cascade = cv2.CascadeClassifier(str(os.getcwd())+ '/app/haarcascades/{}'.format(cas))
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
       
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_stream(self):
        success, image = self.video.read()
        faces = self.face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=3,minSize=(30, 30))
        for (x,y,w,h) in faces:                              # for all faces in the frame          
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0 , 255), 5)   # draw  red  rectangle (BGR)
# (x, y) coordinates, w : width, h:height   
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpeg', image)
        return jpeg.tobytes()
