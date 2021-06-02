import cv2
import mediapipe as mp
import time
from pypylon import pylon

class camera():
    def __init__(self, cameras=[], width=1280, height=512):
        self.cameras = cameras
        self.grabRes = []
        self.images = []
        self.width = width
        self.height = height

        tlFactory = pylon.TlFactory.GetInstance()
        devices = tlFactory.EnumerateDevices()
        if len(devices) == 0:
            raise pylon.RUNTIME_EXCEPTION("No camera present.")
        self.basler = pylon.InstantCameraArray(2)
        for i, self.cameras in enumerate(self.basler):
            self.cameras.Attach(tlFactory.CreateDevice(devices[i]))
        print(self.cameras)
        self.basler.StartGrabbing(pylon.GrabStrategy_LatestImageOnly, 
                pylon.GrabLoop_ProvidedByUser)

        for i, basler in enumerate(self.basler):

            self.grabRes.append(basler.RetrieveResult(5000, 
                    pylon.TimeoutHandling_ThrowException))

            if self.grabRes[i].GrabSucceeded():
                img = self.grabRes[i].GetArray()
                self.images.append(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)) 
            self.grabRes[i].Release()
        self.basler.StopGrabbing()

    def record(self):
        self.basler.StartGrabbing(pylon.GrabStrategy_LatestImageOnly, 
                pylon.GrabLoop_ProvidedByUser)
        #while self.cameras.IsGrabbing():
        for i, self.cameras in enumerate(self.basler):
            self.grabRes[i] = self.basler.RetrieveResult(5000, 
                                pylon.TimeoutHandling_ThrowException)
            if self.grabRes[i].GrabSucceeded():
                img1 = self.grabRes[i].GetArray()
                self.images[i] = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB)
            self.grabRes[i].Release()
        self.basler.StopGrabbing()
            