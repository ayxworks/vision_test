"""
Hand Tracing Module
By: Murtaza Hassan
Youtube: http://www.youtube.com/c/MurtazasWorkshopRoboticsandAI
Website: https://www.computervision.zone
"""

import cv2
import mediapipe as mp
import time
from myLib import camera
from pypylon import pylon
import numpy as np

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList


def main():
    #cv2.namedWindow('live', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('live', 2056, 1028)
    detector = handDetector()
    cameras = camera.camera()
    

    pTime = 0
    cTime = 0

    paTime = 0
    caTime = 0

    while True:
        cameras.record()
        img = detector.findHands(cameras.img1)
         
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
            (255, 0, 255), 3)
        #cv2.imshow("live", img)
        ########################################################################################
        caTime = time.time()
        fpsa = 1 / (caTime - paTime)
        paTime = caTime
        
        imgThresh = cameras.skinMask(cameras.img2)
        cv2.imshow("thresh", imgThresh)

        contours = cameras.contours(cameras.img2, imgThresh)
        hull = cv2.convexHull(contours)
        cv2.drawContours(cameras.img2, [hull], -1, (0, 255, 255), 2)

        cv2.putText(hull, str(int(fpsa)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("hull", cameras.img2)

        

        #hull = cv2.convexHull(contours, returnPoints=False)
        #defects = cv2.convexityDefects(contours, hull)       
        
        ########################################################################################

        k = cv2.waitKey(10)
        if k == 27:
            break

        #cv2.imshow("live", np.hstack([img,img2]))
        cv2.waitKey(1)


if __name__ == "__main__":
    main()