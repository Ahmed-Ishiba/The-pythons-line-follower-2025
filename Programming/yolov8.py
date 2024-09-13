from ultralytics import YOLO
import cv2


# load yolov8 model
model = YOLO('bestn.pt')

# load video
video_path = './test.mp4'
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
#cap.set(cv2.CAP_PROP_FPS, 20)

ret = True
# read frames
while ret:
    ret, frame = cap.read()

    if ret:

        # detect objects
        # track objects
        results = model.track(frame, conf=0.4)

        # plot results
        # cv2.rectangle
        # cv2.putText
        frame_ = results[0].plot()

        # visualize
        cv2.imshow('frame', frame_)
        if cv2.waitKey(1) == 27:
            break