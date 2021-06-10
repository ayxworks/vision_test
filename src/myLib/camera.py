import cv2
import time
import numpy as np
import mediapipe as mp

from pypylon import pylon

class camera():
    def __init__(self, cameras=[], width=1280, height=512):
        self.cameras = cameras
        self.img1 = None
        self.img2 = None
        self.width = width
        self.height = height

        tlFactory = pylon.TlFactory.GetInstance()
        devices = tlFactory.EnumerateDevices()
        if len(devices) == 0:
            raise pylon.RUNTIME_EXCEPTION("No camera present.")
        self.basler = pylon.InstantCameraArray(2)
        for i, self.cameras in enumerate(self.basler):
            self.cameras.Attach(tlFactory.CreateDevice(devices[i]))
        self.basler.StartGrabbing(pylon.GrabStrategy_LatestImageOnly, 
            pylon.GrabLoop_ProvidedByUser)

    def record(self):
        
        #while self.cameras.IsGrabbing():
        grabResult1 = self.basler[0].RetrieveResult(5000, 
                            pylon.TimeoutHandling_ThrowException)
        
        grabResult2 = self.basler[1].RetrieveResult(5000, 
                            pylon.TimeoutHandling_ThrowException)
        
        if grabResult1.GrabSucceeded() & grabResult2.GrabSucceeded():
            img1 = grabResult1.GetArray()
            img2 = grabResult2.GetArray()
            self.img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB)
            self.img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)
        grabResult1.Release()
        grabResult2.Release()

    def stopGrab(self):
        self.basler.StopGrabbing()

    def grabOne(self, cam=0):
        self.basler[cam].Open()
        self.basler[cam].MaxNumBuffer = 5
        result = self.basler[cam].GrabOne(5000)
        self.basler[cam].Close()
        return result
    
    def skinMask(self, img):
        """
        # Convert the grayscale image to binary
        gray = cv2.cvtColor(cameras.img2, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU)
        
        # Display the binary image
        cv2.imshow('Binary image', binary)

        inverted_binary = ~binary
        cv2.imshow('Inverted binary image', inverted_binary)
        """
        hsvim = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 0, 10], dtype = "uint8")
        upper = np.array([10, 100, 60], dtype = "uint8")
        skinRegionHSV = cv2.inRange(hsvim, lower, upper)
        blurred = cv2.blur(skinRegionHSV, (2,2))
        ret,thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY)
        return thresh

    

    def contours(self, img, imgThresh):
        contours, hierarchy = cv2.findContours(imgThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = max(contours, key=lambda x: cv2.contourArea(x))
        #cv2.drawContours(img, [contours], -1, (255,255,0), 2)
        #cv2.imshow("thresh", img)
        return contours

"""
gray = cv2.cvtColor(cameras.img2,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
        contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        drawing = np.zeros(img.shape,np.uint8)

        max_area=0
    
        for i in range(len(contours)):
                cnt=contours[i]
                area = cv2.contourArea(cnt)
                if(area>max_area):
                    max_area=area
                    ci=i
        cnt=contours[ci]
        hull = cv2.convexHull(cnt)
        prev_hull = cv2.convexHull(cnt)
        prev_cnt = cnt
        moments = cv2.moments(cnt)
        if moments['m00']!=0:
                    cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                    cy = int(moments['m01']/moments['m00']) # cy = M01/M00
                
        centr=(cx,cy)
        cv2.circle(img,centr,5,[0,0,255],2)       
        cv2.drawContours(drawing,[cnt],0,(0,255,0),2) 
        cv2.drawContours(drawing,[hull],0,(255,0,255),2) 
            
        cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt,returnPoints = False)
        
        if(1):
                defects = cv2.convexityDefects(cnt,hull)
                mind=0
                maxd=0
                for i in range(defects.shape[0]):
                        s,e,f,d = defects[i,0]
                        start = tuple(cnt[s][0])
                        end = tuple(cnt[e][0])
                        far = tuple(cnt[f][0])
                        dist = cv2.pointPolygonTest(cnt,centr,True)
                        cv2.line(img,start,end,[0,255,0],2)
                        cv2.circle(img,far,5,[0,0,255],-1)
                #print "i=",i,"area=",area,"hull",hull,"prev_hull",prev_hull
                #print "Points=",prev_hull
                i=0
        #change_image[hull] = Clear[hull]
        #cv2.imshow('final_game',change_image)
        cv2.imshow('output',drawing)
        cv2.imshow('input',cameras.img2)
                    
        k = cv2.waitKey(10)
        if k == 27:
            break

"""