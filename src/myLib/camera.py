import cv2
import mediapipe as mp
import time
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
            