import cv2
import mediapipe as mp
import time
from pypylon import pylon
import numpy as np

cv2.namedWindow('live', cv2.WINDOW_NORMAL)
cv2.resizeWindow('live', 1280, 512)
tlFactory = pylon.TlFactory.GetInstance()
devices = tlFactory.EnumerateDevices()
if len(devices) == 0:
    raise pylon.RUNTIME_EXCEPTION("No camera present.")

cameras = pylon.InstantCameraArray(2)

for i, camera in enumerate(cameras):
    camera.Attach(tlFactory.CreateDevice(devices[i]))
# Starts grabbing for all cameras
cameras.PixelFormat = "RGB8"
cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly, 
                    pylon.GrabLoop_ProvidedByUser)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
while True:

    while cameras.IsGrabbing():
        grabResult1 = cameras[0].RetrieveResult(5000, 
                            pylon.TimeoutHandling_ThrowException)
        
        grabResult2 = cameras[1].RetrieveResult(5000, 
                            pylon.TimeoutHandling_ThrowException)
        
        if grabResult1.GrabSucceeded() & grabResult2.GrabSucceeded():
            img1 = grabResult1.GetArray()
            img2 = grabResult2.GetArray()

        imgRGB = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB)
        #imgRGB.flags.writeable = False
        results = hands.process(imgRGB)
        #imgRGB.flags.writeable = True
        #print(results.multi_hand_landmarks)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # print(id, lm)
                    #h, w, c = img1.shape
                    #cx, cy = int(lm.x * w), int(lm.y * h)
                    h, w, c = imgRGB.shape
                    if len(imgRGB.shape)<3:
                        #dim = np.zeros((28,28))
                        #img1.shape = np.stack((img1.shape,dim, dim), axis=3)
                        print("not rgb")
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    #print(id, cx, cy)
                    # if id == 4:
                    cv2.circle(imgRGB, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                mpDraw.draw_landmarks(imgRGB, handLms, mpHands.HAND_CONNECTIONS)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(imgRGB, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
        
        ############################################################
        
        imgRGB2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)
        results2 = hands.process(imgRGB2)
        # print(results.multi_hand_landmarks)

        if results2.multi_hand_landmarks:
            for handLms in results2.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    # print(id, lm)
                    
                    h, w, c = imgRGB2.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    #print(id, cx, cy)
                    # if id == 4:
                    cv2.circle(imgRGB2, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                mpDraw.draw_landmarks(imgRGB2, handLms, mpHands.HAND_CONNECTIONS)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(imgRGB2, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
        

        cv2.imshow('live', np.hstack([imgRGB,imgRGB2]))
        cv2.waitKey(1)