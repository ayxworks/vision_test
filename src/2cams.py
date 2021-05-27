import time
from pypylon import pylon
from threading import Thread
import numpy as np
import cv2
import matplotlib.pyplot as plt

#cv2.VideoCapture.set(cv2.CAP_PROP_BUFFERSIZE , 3);
#cv2.namedWindow('live', cv2.WINDOW_NORMAL)
#cv2.resizeWindow('live', 1280, 512)
if __name__ == '__main__':
    tlFactory = pylon.TlFactory.GetInstance()
    devices = tlFactory.EnumerateDevices()
    if len(devices) == 0:
        raise pylon.RUNTIME_EXCEPTION("No camera present.")

    cameras = pylon.InstantCameraArray(2)

    for i, camera in enumerate(cameras):
        camera.Attach(tlFactory.CreateDevice(devices[i]))
    # Starts grabbing for all cameras
    cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly, 
                        pylon.GrabLoop_ProvidedByUser)


    while cameras.IsGrabbing():
        grabResult1 = cameras[0].RetrieveResult(5000, 
                            pylon.TimeoutHandling_ThrowException)
        
        grabResult2 = cameras[1].RetrieveResult(5000, 
                            pylon.TimeoutHandling_ThrowException)
        
        if grabResult1.GrabSucceeded() & grabResult2.GrabSucceeded():
            im1 = grabResult1.GetArray()
            im2 = grabResult2.GetArray()

            # If ESC is pressed exit and destroy window
            cv2.imshow('Acquisition', np.hstack([im1,im2]))
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cv2.destroyAllWindows()