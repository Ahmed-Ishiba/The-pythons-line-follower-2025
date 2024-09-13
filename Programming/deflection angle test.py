import cv2
from picamera2 import Picamera2
import numpy as np
import math
import serial
from time import sleep

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1.0)
sleep(2)
ser.reset_input_buffer()
print("serial ok")
weights = [0.7,0.3,0.1]
picam2 = Picamera2()
picam2.preview_configuration.main.size=(640,480) #full screen : 3280 2464
picam2.preview_configuration.main.format = "RGB888" #8 bits
picam2.start()
centroid_sum = 0


def black(live):
    cropped_image = [live[180:280,:640],live[280:380,:640],live[380:480,:640]] #y, x
    global detect_black
    cx = 0
    centroid_sum = 0
    cy = 0
    deflection_angle = 0
    w = 0
    h = 0
    area = 0
    gap_counter =0
    black_lower = np.array([86,58,36], np.uint8)
    black_upper = np.array([176, 172, 127], np.uint8)
    
    #main_contours = max()
    for i,region in enumerate(cropped_image):
        hsvf = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        black_mask = cv2.inRange(hsvf, black_lower, black_upper)
        black_result = cv2.bitwise_and(region, region, mask=black_mask)
        black_contours, black_hierarchy = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        
        if len(black_contours) > 0:
            
            largest_black = max(black_contours, key=cv2.contourArea)
            detect_black = True
            area = cv2.contourArea(largest_black)
            M = cv2.moments(largest_black)
            if(area > 30000):
                
                #print(area)
                cv2.drawContours(region, black_contours, -1, (255, 0, 0), 3)
                x, y, w, h = cv2.boundingRect(largest_black)
                #print(w)
                #if weights[i] ==
            if M["m00"] != 0:
                cx =int(M["m10"]/M["m00"])
                cy =int(M["m01"]/M["m00"])
                cv2.circle(region, (cx, cy), 5, (255, 255, 255), 3)
                #return cx, cy
                centroid_sum += cx * weights[i]
                deflection = (cx-320)/(240)
                deflection_angle = math.degrees(math.atan(deflection))
        if len(black_contours) != 0:
            detect_black = True
        else:
            detect_black = False
    return cx, cy, area, w, h, deflection_angle

while True:
    im = picam2.capture_array()
    black_cx, black_cy, black_area, black_width, black_height ,deflection_angle = black(im)
    
    print("black cx = ",black_cx)
    print("black area = ", black_area)
    print("black cy = ",black_cy)
    print("deflection angle = ",deflection_angle)
    print(" ")
    if detect_black:
        if black_width > 470:
            ser.write("forward\n".encode('utf-8'))
            print('forward intersection')
        if deflection_angle <= 10 and deflection_angle >= -10:
            ser.write("forward\n".encode('utf-8'))
            print('forward')
        elif deflection_angle < -10:
            ser.write("left\n".encode('utf-8'))
            print('left')
        elif deflection_angle > 10:
            ser.write("right\n".encode('utf-8'))
            print('right')
    cv2.imshow('detection', im)
    if cv2.waitKey(1)==ord('q'):
        break
    
    
picam2.stop()
cv2.destroyAllWindows()
