import time
from pypylon import pylon
from threading import Thread
import numpy as np
import cv2

class ThreadedCamera(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

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
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(self.FPS)

    def show_frame(self, name):
        cv2.imshow(name, self.frame)
        cv2.waitKey(self.FPS_MS)

if __name__ == '__main__':
    src = "https://video2archives.earthcam.com/archives/_definst_/MP4:permanent/3275/2019/01/30/1300.mp4/chunklist_w581738193.m3u8"
    src2 = "https://video-cam.bitcom.psi.br/CSL-CLIMA-AO-VIVO-LESTE/CSL-CLIMA-AO-VIVO-LESTE.stream/chunklist_w1088673527.m3u8"
    src3 = "http://160.111.252.72:1935/live_edge_panda/smil:panda02_all.smil/playlist.m3u8"
    threaded_camera = ThreadedCamera(src)
    threaded_camera2 = ThreadedCamera(src2)
    threaded_camera3 = ThreadedCamera(src3)
    while True:
        try:
            threaded_camera.show_frame("bay")
            threaded_camera2.show_frame("Los santos")
            threaded_camera3.show_frame("Pandas")
        except AttributeError:
            pass