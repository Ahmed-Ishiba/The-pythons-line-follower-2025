import cv2
from picamera2 import Picamera2
import numpy as np
import math
import serial
from time import sleep

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0)
sleep(2)
ser.reset_input_buffer()
print("serial ok")
weights = [0.1,0.7,0.6] 
arr_higher_threshold = [np.array([149,188,176], np.uint8),np.array([149,188,176], np.uint8),np.array([149,188,176], np.uint8)]
arr_lower_threshold = [np.array([115,114,12], np.uint8), np.array([115,114,12], np.uint8), np.array([115,114,12], np.uint8)]

picam2 = Picamera2()
picam2.preview_configuration.main.size=(320,240) #full screen : 3280 2464
picam2.preview_configuration.main.format = "RGB888" #8 bits
picam2.start()
centroid_sum = 0
center_pos = 0
def black(live):
    cropped_image = [live[95:140,25:295],live[145:190,25:295],live[200:245, 25:295]] #y, x
    global detect_black
    centroid_sum = 0
    cy = 0
    cx_array =[]
    deflection_angle = 0
    w = 0
    center_pos = 0
    cx = 0
    h = 0
    area = 0
    gap_counter =0
    weight_sum=0

    #main_contours = max()
    for i,region in enumerate(cropped_image):
        black_lower = np.array([40, 21, 4], np.uint8)
        black_upper = np.array([197, 182, 139], np.uint8)
        hsvf = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        black_mask = cv2.inRange(hsvf, black_lower, black_upper)
        black_result = cv2.bitwise_and(region, region, mask=black_mask)
        black_contours, black_hierarchy = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(black_contours) > 0:
            largest_black = max(black_contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_black)
            M = cv2.moments(largest_black)
            if(area > 500):
                #print(area)
                #cv2.drawContours(region, largest_black, -1, (255, 0, 0), 3)
                x, y, w, h = cv2.boundingRect(largest_black)
                cv2.rectangle(region,(x,y),(x+w,y+h), (0,0,255), 5)
                #print("x of black line", x)
                #print("width of black",w)
                    
                if M["m00"] != 0:
                    cx =int(M["m10"]/M["m00"])
                    cy =int(M["m01"]/M["m00"])
                    cx_array.append(cx)
                    cv2.circle(region, (cx, cy), 5, (255, 255, 255), 3)
                #return cx, cy
                detect_black = True
            else:
                detect_black = False
        else:
            detect_black = False
    if detect_black:
        for f in range(0,len(cx_array)):
            #print("cx array", cx_array[f])
            centroid_sum += cx_array[f] * weights[f] # r[4] is the roi weight.
            weight_sum += weights[f]
        center_pos = (centroid_sum / weight_sum)
        print("center position = ", center_pos)
        deflection = (center_pos-135)/(120)
        deflection_angle = math.degrees(math.atan(deflection))
            
    return cx, cy, area, w, h, deflection_angle, gap_counter

while True:
    im = picam2.capture_array()
    black_cx, black_cy, black_area, black_width, black_height ,deflection_angle, gap_counter = black(im)
    #print("black cx = ",black_cx)
    #print("black area = ", black_area)
    #print("black cy = ",black_cy)
    #cv2.circle(im, (90, 200), 5, (255, 255, 255), 3)

    print("deflection angle = ",deflection_angle)
    print("gap counter = ",gap_counter)
    print(" ")
    ser.write((str(int(deflection_angle))+"\n").encode('utf-8'))
    """
    #if gap_counter ==3:
     #   ser.write("forward\n".encode('UTF-8'))
      #  print("forward gap")
    #else:
    #if detect_black:
        
        if black_width > 600 and black_area > 9000:
            #ser.write("forward\n".encode('utf-8'))
            print('forward intersection')
        else:    
            if deflection_angle <= 10 and deflection_angle >= -10:
                ser.write("forward\n".encode('utf-8'))
                print('forward')
            elif deflection_angle >=-30 and deflection_angle <-10:
                print("left slowly")
                ser.write("left slowly\n".encode('utf-8'))
            elif deflection_angle < -30:
                ser.write("left\n".encode('utf-8'))
                print('left')
            elif deflection_angle >10 and deflection_angle <=30:
                ser.write("right slowly\n".encode('utf-8'))
            elif deflection_angle > 60:
                ser.write("right\n".encode('utf-8'))
                print('right')
            """
                    
    cv2.imshow('detection', im)
    if cv2.waitKey(1)==ord('q'):
        break
    
    
picam2.stop()
cv2.destroyAllWindows()
