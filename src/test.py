#MV record module
import cv2
import time
import threading
from pypylon import pylon
import queue

img_number=-1
prev_img_number=img_number
async_q=queue.Queue()
grab_state=True
frame_ctr=0

def proc_q():
    global async_q,img_number,grab_state,frame_ctr
    while img_number==-1:
        pass
    img=cv2.cvtColor(async_q.get(),cv2.COLOR_BayerBG2RGB)
    frame_width=img.shape[1]
    frame_height=img.shape[0]
    fourcc=cv2.VideoWriter_fourcc('H','2','6','4')
    fps=100
    saved_vid_file="TEST_NEW_"+str(int(time.time()))+".avi"
    video_writer=cv2.VideoWriter(saved_vid_file,fourcc,fps,(frame_width,frame_height))    
    video_writer.write(img)
    frame_ctr+=1
    print("Video rec started")
    while not async_q.empty() or grab_state:
        if not async_q.empty():
            img=cv2.cvtColor(async_q.get(),cv2.COLOR_BayerBG2RGB)
            video_writer.write(img)
            frame_ctr+=1
            time.sleep(0.005)
        else:
            time.sleep(0.005)
            continue
    video_writer.release()
    print("Rec ended",frame_ctr)
                
 
class SGNImageEventHandler(pylon.ImageEventHandler):
    def OnImageGrabbed(self, camera, grabResult):
        global async_q,img_number
        if grabResult.GrabSucceeded() and int(grabResult.ImageNumber)!=img_number:
            async_q.put(grabResult.Array)
            img_number=int(grabResult.ImageNumber)
            #print(img_number)

def grab_cam(duration=60):
    global grab_state
    tlFactory = pylon.TlFactory.GetInstance()
    devices = tlFactory.EnumerateDevices()
    if len(devices) == 0:
        raise pylon.RUNTIME_EXCEPTION("No camera present.")
    basler = pylon.InstantCameraArray(2)
    for i, cameraBas in enumerate(basler):
        cameraBas.Attach(tlFactory.CreateDevice(devices[i]))
    camera=pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
    #camera.PixelFormat="BGR8"     # 90-100 fps (50% camera capacity)
    basler.PixelFormat="RGB8" #200 fps (max camera capability) but very cpu intencive (took approx 8-10GB running on 16 cores)
    camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll,pylon.Cleanup_Delete)    
    camera.RegisterImageEventHandler(SGNImageEventHandler(),pylon.RegistrationMode_Append, pylon.Cleanup_Delete)        
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly, pylon.GrabLoop_ProvidedByInstantCamera)
    print("Grab started-",camera.GetDeviceInfo().GetModelName())
    start_rec=int(time.time())
    while int(time.time())-start_rec<=duration and camera.IsGrabbing():
        time.sleep(0.005)
    camera.Close()
    print("Grab ended")
    grab_state=False

grab_thread=threading.Thread(target=grab_cam,args=(60,)) #60 second recording
grab_thread.start()
time.sleep(1)
q_proc_thread=threading.Thread(target=proc_q,args=())
q_proc_thread.start()
grab_thread.join()
print("Q Size:",async_q.qsize())
q_proc_thread.join()
print("Process ended")

