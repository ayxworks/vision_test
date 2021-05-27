import time
from pypylon import pylon
from threading import Thread
import numpy as np
import cv2

class ThreadedCamera():
    def __init__(self):
        tlFactory = pylon.TlFactory.GetInstance()
        devices = tlFactory.EnumerateDevices()
        self.converter = pylon.ImageFormatConverter()
        self.cameras = pylon.InstantCameraArray(2)
        self.cameras.MaxNumBuffer = 20
        self.cameras.PixelFormat = "RGB8"

        if len(devices) == 0:
            raise pylon.RUNTIME_EXCEPTION("No camera present.")

        for i, camera in enumerate(self.cameras):
            camera.Attach(tlFactory.CreateDevice(devices[i]))

        #self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        #self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned      

        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)

        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            self.cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly, 
                        pylon.GrabLoop_ProvidedByUser)
            while self.cameras.IsGrabbing():
                grabResult1 = self.cameras[0].RetrieveResult(5000, 
                                pylon.TimeoutHandling_ThrowException)
            
                grabResult2 = self.cameras[1].RetrieveResult(5000, 
                                    pylon.TimeoutHandling_ThrowException)
                
                if grabResult1.GrabSucceeded() & grabResult2.GrabSucceeded():
                    #self.im1 = self.converter.Convert(grabResult1).GetArray()
                    #self.im2 = self.converter.Convert(grabResult2).GetArray()
                    self.im1 = grabResult1.GetArray()
                    self.im2 = grabResult2.GetArray()
                grabResult1.Release()
                grabResult2.Release()
            time.sleep(self.FPS)

    def show_frame(self, name):
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name, 1280, 512)
        cv2.imshow(name, np.hstack([self.im1,self.im2]))
        cv2.waitKey(self.FPS_MS)

if __name__ == '__main__':
   
    threaded_camera = ThreadedCamera()
    while True:
        try:
            threaded_camera.show_frame("live")

        except AttributeError:
            pass