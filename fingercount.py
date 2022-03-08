import cv2
import time
import os
import handTrackingModule as htm
wCam,hCam=640,480
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
folderpath= "Finger"
myList = os.listdir(folderpath)
#print(myList)
overLayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderpath}/{imPath}')
    overLayList.append(image)

    #print(f'{folderpath}/{imPath}')
#print(len(overLayList))
pTime=0
detector=htm.handDetector(detectionCon=0.75)
tip=[4,8,12,16,20]
while True:
    success,img = cap.read()
    img=detector.findHands(img)
    lmList= detector.findPosition(img,draw=False)
    #print(lmList)
    if len(lmList) != 0:
        fingers=[]
        if lmList[tip[0]][1]<lmList[tip[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for i in range(1,5):
            if lmList[tip[i]][2]<lmList[tip[i]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        tfinger=fingers.count(1)
        print(tfinger)
        h,w,c=overLayList[tfinger-1].shape
        img[0:h,0:w]=overLayList[tfinger-1]
            
  
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(210,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
