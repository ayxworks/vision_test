import os
import cv2
import numpy as np
from myLib import camera

thres = 0.60 # Threshold to detect object
nms_threshold = 0.1

classNames= []
classFile = os.getcwd() + "coco.names"

with open(classFile,"rt") as f:
    classNames = f.read().rstrip("n").split("n")

#print(classNames)
configPath = os.getcwd() + "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = os.getcwd() + "frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
cameras = camera.camera()

while True:
    
    cameras.record()

    img = cameras.img1
    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1,-1)[0])
    confs = list(map(float,confs))
    #print(type(confs[0]))
    #print(confs)

    indices = cv2.dnn.NMSBoxes(bbox,confs,thres,nms_threshold)
    #print(indices)

    for i in indices:
        i = i[0]
        box = bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]
        cv2.rectangle(img, (x,y),(x+w,h+y), color=(0, 255, 0), thickness=2)
        try:
            cv2.putText(img,classNames[classIds[i][0]-1].upper(),(box[0]+10,box[1]+30), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        except IndexError:   
            pass

        #cv2.imshow("Output",img)

    ##################################################################################################
    img2 = cameras.img2
    classIds, confs, bbox = net.detect(img2,confThreshold=thres)

    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1,-1)[0])
    confs = list(map(float,confs))
    #print(type(confs[0]))
    #print(confs)

    indices = cv2.dnn.NMSBoxes(bbox,confs,thres,nms_threshold)
    print(indices)

    for i in indices:
        i = i[0]
        box = bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]
        cv2.rectangle(img2, (x,y),(x+w,h+y), color=(0, 255, 0), thickness=2)
        try:
            cv2.putText(img2,classNames[classIds[i][0]-1].upper(),(box[0]+10,box[1]+30), cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        except IndexError:   
            pass

        #cv2.imshow("Output",img2)

    ##################################################################################################
        cv2.imshow('live', np.hstack([img,img2]))
        cv2.waitKey(1)