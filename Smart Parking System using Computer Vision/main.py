import cv2
import pickle
from cv2 import cvtColor
from cv2 import COLOR_BGR2GRAY
from cv2 import adaptiveThreshold
from cv2 import FONT_HERSHEY_SIMPLEX
import numpy as np

#video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPos','rb') as f:
     posList = pickle.load(f)
     
width,height=107,48
def checkParkingSpace(imgprocessed):
    spaceCounter = 0
    for pos in posList:
        x,y = pos
        
        imgCrop = imgprocessed[y:y+height,x:x+width]
       # cv2.imshow(str(x*y),imgCrop)
        count = cv2.countNonZero(imgCrop)
        cv2.putText(img,str(count), (x,y+height-5),cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(0,0,255), thickness=2)
        if count<850:
            color = (0,255,0)
            thickness = 3
            spaceCounter +=1
        else:
            color = (0,0,255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    cv2.putText(img,f'free:{spaceCounter}/{len(posList)}', (45,73),cv2.FONT_HERSHEY_TRIPLEX, fontScale=1.2, color=(255,55,50), thickness=3)
       
while True:
    
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        
    success, img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur =cv2.GaussianBlur(imgGray,(3,3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3),np.uint8)
    imgDilates = cv2.dilate(imgMedian, kernel, iterations=1)
    
    checkParkingSpace(imgDilates)        
    cv2.imshow("image",img)
    #cv2.imshow("imgBlur",imgBlur)
    #cv2.imshow("imgThreshold",imgMedian)
    cv2.waitKey(10)