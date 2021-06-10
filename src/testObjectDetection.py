import cv2
import time
import mediapipe as mp
from myLib import camera

def main():
    cameras = camera.camera()
    mp_drawing = mp.solutions.drawing_utils
    mp_objectron = mp.solutions.objectron

    pTime = 0
    cTime = 0

    with mp_objectron.Objectron(static_image_mode=False,
                                max_num_objects=5,
                                min_detection_confidence=0.5,
                                min_tracking_confidence=0.99,
                                model_name='Cup') as objectron:

        while True:
            cameras.record()

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            cameras.img1.flags.writeable = False
            results = objectron.process(cameras.img1)

            # Draw the box landmarks on the image.
            cameras.img1.flags.writeable = True
            #cameras.img1 = cv2.cvtColor(cameras.img1, cv2.COLOR_RGB2BGR)
            if results.detected_objects:
                for detected_object in results.detected_objects:
                    mp_drawing.draw_landmarks(
                    cameras.img1, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                    mp_drawing.draw_axis(cameras.img1, detected_object.rotation,
                                        detected_object.translation)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(cameras.img1, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
            cv2.imshow('MediaPipe Objectron', cameras.img1)
            if cv2.waitKey(5) & 0xFF == 27:
                break

if __name__ == "__main__":
    main()