from __future__ import division

script = True
turn_off_motion = False
turn_off_drawing = True
detect_red = False

import time
from ultralytics import YOLO
import board
import gpiod
import busio
from adafruit_mpu6050 import MPU6050
import Adafruit_PCA9685
import Adafruit_GPIO.I2C as I2C
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
import os
import sys
import smbus
import cv2
from picamera2 import Picamera2
import numpy as np
import math
from time import sleep
from operator import itemgetter
weights = [0.3,0.6,0.7] 
arr_higher_threshold = [np.array([149,188,176], np.uint8),np.array([149,188,176], np.uint8),np.array([149,188,176], np.uint8)]
arr_lower_threshold = [np.array([115,114,12], np.uint8), np.array([115,114,12], np.uint8), np.array([115,114,12], np.uint8)]

picam2 = Picamera2(0)
picam2.preview_configuration.main.size=(320,240) #full screen : 3280 2464
picam2.preview_configuration.main.format = "RGB888" #8 bits
picam2.start()
centroid_sum = 0
center_pos = 0


i2c = board.I2C()
i2c_bus = 1
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=i2c_bus)
try:
	OFFSET_X = 0
	OFFSET_Y = 0
	OFFSET_Z = 0

	mpu = MPU6050(i2c)
	mpu.accelerometer_offset = (OFFSET_X, OFFSET_Y, OFFSET_Z)
except:
	pass



f = gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN
chip = gpiod.Chip('gpiochip4')
led = chip.get_line(20)#20
led.request("p_gpio", gpiod.LINE_REQ_DIR_OUT, f)
led.set_value(1)
time.sleep(1)
led.set_value(0)


pca = PCA9685(i2c)
pca.frequency = 50

check_zone = False

pwm.set_pwm_freq(60)

left_front_1 = 14
left_front_2 = 15

left_back_1 = 9
left_back_2 = 8

right_front_1 = 12
right_front_2 = 13

right_back_1 = 10
right_back_2 = 11

high_speed = 900
speed2 =0
low_speed  = 700
zero_speed = 0
counter =0
model = YOLO("/home/pi/yolo/silver_classify_s.onnx", task='classify')
def entrance(im):
    global check_zone
    global counter, enter_zone
    #picam1.set_controls({"AeEnable":False, "ExposureTime":4000}) #To be tested
    results = model.predict(im, imgsz=128, conf=0.2, workers=4,verbose=False)
    result=results[0].numpy()
    confidences = result.probs.top5conf
    silver_value = confidences[0] if result.probs.top1 == 1 else confidences[1]
    print("confidance",silver_value)
    if silver_value >0.2:
        print("saw silver")
        counter+=1
    else:
        counter =0
    if counter > 0:
        enter_zone = True
        print("evacuation")
        """
        with open("/tmp/switch_script","w") as f:
            f.write("switch")
        time.sleep(2)
        """
        
     
    
def calculate_orientation():
    accel_x, accel_y, accel_z = mpu.acceleration
    # Calculate pitch and roll angles
    pitch = math.atan2(accel_x, math.sqrt(accel_y**2 + accel_z**2)) * 180 / math.pi
    roll = math.atan2(-accel_y, accel_z) * 180 / math.pi

    # Convert to range -180 to 180
    if pitch > 180:
        pitch -= 360
    if roll > 180:
        roll -= 360

    return pitch, roll

def map_value(value, from_low, from_high, to_low, to_high):
    if from_high - from_low == 0:
        return to_low  
    mapped_value = (value - from_low) / (from_high - from_low) * (to_high - to_low) + to_low
    return mapped_value

def turn_around():
    backward()
    time.sleep(0.5)
    right(1000)
    time.sleep(1.5)

def forward():
    global speed2
    pwm.set_pwm(left_front_1, 0, 500+speed2)
    pwm.set_pwm(left_front_2, 0, 0)
	
    pwm.set_pwm(left_back_1, 0, 500+speed2)
    pwm.set_pwm(left_back_2, 0, 0)
	
    pwm.set_pwm(right_front_1, 0, 500+speed2)
    pwm.set_pwm(right_front_2, 0, 0)
	
    pwm.set_pwm(right_back_1, 0, 500+speed2)
    pwm.set_pwm(right_back_2, 0, 0)
def backward():
    pwm.set_pwm(left_front_2, 0, 600)
    pwm.set_pwm(left_front_1, 0, 0)
	
    pwm.set_pwm(left_back_2, 0, 600)
    pwm.set_pwm(left_back_1, 0, 0)
	
    pwm.set_pwm(right_front_2, 0, 600)
    pwm.set_pwm(right_front_1, 0, 0)
	
    pwm.set_pwm(right_back_2, 0, 600)
    pwm.set_pwm(right_back_1, 0, 0)
def right(speed):
    pwm.set_pwm(left_front_1, 0, speed)
    pwm.set_pwm(left_front_2, 0, 0)
	
    pwm.set_pwm(left_back_1, 0, 400)
    pwm.set_pwm(left_back_2, 0, 0)
    
    pwm.set_pwm(right_front_2, 0, speed)
    pwm.set_pwm(right_front_1, 0, 0)
	
    pwm.set_pwm(right_back_2, 0, 400)
    pwm.set_pwm(right_back_1, 0, 0)
def left(speed):
    pwm.set_pwm(left_front_2, 0, speed)
    pwm.set_pwm(left_front_1, 0, 0)
	
    pwm.set_pwm(left_back_2, 0, 400)
    pwm.set_pwm(left_back_1, 0, 0)
	
    pwm.set_pwm(right_front_1, 0, speed)
    pwm.set_pwm(right_front_2, 0, 0)
	
    pwm.set_pwm(right_back_1, 0, 400)
    pwm.set_pwm(right_back_2, 0, 0)
def stop():
    pwm.set_pwm(left_front_2, 0, 900)
    pwm.set_pwm(left_front_1, 0, 0)
    pwm.set_pwm(left_back_2, 0, 900)
    pwm.set_pwm(left_back_1, 0, 0)
    pwm.set_pwm(right_front_2, 0, 900)
    pwm.set_pwm(right_front_1, 0, 0)
    pwm.set_pwm(right_back_2, 0, 900)
    pwm.set_pwm(right_back_1, 0, 0)
    time.sleep(0.1)
    pwm.set_pwm(left_front_1, 0, 0)
    pwm.set_pwm(left_front_2, 0, 0)
    pwm.set_pwm(left_back_1, 0, 0)
    pwm.set_pwm(left_back_2, 0, 0)
    pwm.set_pwm(right_front_1, 0, 0)
    pwm.set_pwm(right_front_2, 0, 0)
    pwm.set_pwm(right_back_1, 0, 0)
    pwm.set_pwm(right_back_2, 0, 0)

def obstacle_left():
	left(1000)
	time.sleep(0.6)
	stop()
	time.sleep(0.2)
	forward()
	time.sleep(0.9)
	stop()
	time.sleep(0.2)
	right(1000)
	time.sleep(0.7)
	stop()
	time.sleep(0.2)
	forward()
	time.sleep(1.3)
	stop()
	time.sleep(0.2)
	right(1000)
	time.sleep(0.7)
	stop()
	time.sleep(0.2)
	forward()
	time.sleep(0.7)
	stop()
	time.sleep(0.2)
	left(1000)
	time.sleep(0.7)
	stop()
	time.sleep(5)
	
def obstacle_right():
	right(1000)
	time.sleep(0.6)
	stop()
	time.sleep(0.2)
	forward()
	time.sleep(0.9)
	stop()
	time.sleep(0.2)
	left(1000)
	time.sleep(0.7)
	stop()
	time.sleep(0.2)
	forward()
	time.sleep(1.3)
	stop()
	time.sleep(0.2)
	left(1000)
	time.sleep(0.7)
	stop()
	time.sleep(0.2)
	forward()
	time.sleep(0.7)
	stop()
	time.sleep(0.2)
	right(1000)
	time.sleep(0.7)
	stop()
	time.sleep(5)

"""
hoigher =  (179, 106, 101)
lower =  (91, 27, 12)


"""
black_lower = np.array([91, 27, 12], np.uint8)
black_upper =np.array([179, 106, 101], np.uint8)
def detect_triangles(im):
    cropped_image = im[140:200, 15:305] #140:230,:320
    cx, cy, w, h =0,0,0,0
    triangle_area = 0
    right_zigzag, left_zigzag = False, False
    theta = 0
    global black_lower
    global black_upper
    hsvf = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
    black_mask = cv2.inRange(hsvf, black_lower, black_upper)
    black_result = cv2.bitwise_and(cropped_image, cropped_image, mask=black_mask)
    black_contours, black_hierarchy = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(black_contours)>0:
        largest_black = max(black_contours, key=cv2.contourArea)
        if not(turn_off_drawing):
            cv2.drawContours(cropped_image,largest_black,-1,(255, 0, 0), 3)
        approx = cv2.approxPolyDP(largest_black, 0.021*cv2.arcLength(largest_black, True), True)#0.025, 0.23
        x, y, w, h = cv2.boundingRect(largest_black)
        print("len approx", len(approx))
        if len(approx) ==3:
            triangle_area = cv2.contourArea(largest_black)
            print("triangle area = ", triangle_area)
            print("approx", approx[0][0][0])
            p1 = (approx[0][0][0], approx[0][0][1])
            p2 = (approx[1][0][0], approx[1][0][1])
            p3 = (approx[2][0][0], approx[2][0][1])
            point_array = [p1, p2, p3]
            point_array = sorted(point_array, key = itemgetter(1))
            print(point_array)
            a = point_array[0]
            b = point_array[1] #down left point
            c = point_array[2] #down right point
            
            distance_ab = math.dist(a, b)
            distance_ac = math.dist(a, c)
            
            vector_AB = (b[0]-a[0], b[1]-a[1])
            vector_AC = (c[0]-a[0], c[1]-a[1])
            dot_AB_AC = vector_AB[0]*vector_AC[0] + vector_AB[1]*vector_AC[1]
            theta = math.acos((dot_AB_AC)/(distance_ab*distance_ac))
            cv2.circle(cropped_image, a, 5, (255, 255, 255), 3)
            cv2.circle(cropped_image, b, 5, (0, 0, 255), 3)
            cv2.circle(cropped_image, c, 5, (255, 0, 0), 3)
            
            if theta <5 and triangle_area > 50 :
                
                if distance_ab > distance_ac:    # >
                    triangle_x = b[0]
                    print("left zigzag test")
                    left_zigzag = True
                    '''
                    if triangle_x >160:
                        #print("right zigzag")
                        right_zigzag = True
                    elif triangle_x < 160:
                        #print("left zigzag")
                        left_zigzag = True
                    '''
                elif distance_ac> distance_ab: #>
                    triangle_x = c[0]
                    print("right zigzag test")
                    right_zigzag = True
                    '''
                    if triangle_x >160:
                        right_zigzag = True
                        #print("right zigzag")
                    elif triangle_x < 160:
                        left_zigzag = True
                        #print("left zigzag")
                    '''
                print("distance of AB", distance_ab)
                print("distance of AC", distance_ac)
                #if not(turn_off_drawing):
                cv2.drawContours(cropped_image,largest_black,0,(255, 255, 0), 3)
    
            else:
                left_zigzag = False
                right_zigzag = False
        else:
            left_zigzag = False
            right_zigzag = False
        #cx = int(x) + int(w/2)
        #cy = int(y) + int(h/2)
    return right_zigzag, left_zigzag, theta, triangle_area

"""
hoigher =  (175, 80, 92)
lower =  (3, 0, 29)
""" 
right_array = []
left_array = []
is_black =0
omar_right_counter =0 
omar_left_counter =0
readings_range=75
def omar_function(live):
    cropped_image = [live[140:200, 15:55],live[140:200,265:305]] 
    cx, y, w, h =0,0,0,0
    global right_array
    global omar_right_counter
    global omar_left_counter 
    global left_array 
    global is_black
    global black_lower
    global black_upper
    for i,region in enumerate(cropped_image):
        
        hsvf = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        black_mask = cv2.inRange(hsvf, black_lower, black_upper)
        black_result = cv2.bitwise_and(region, region, mask=black_mask)
        black_contours, black_hierarchy = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        is_black =0
        if black_contours:
            largest_black = max(black_contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_black)
            x, y, w, h = cv2.boundingRect(largest_black)
            
            if area >150:
                cv2.rectangle(region,(x,y),(x+w,y+h), (255,0,0), 2)
                is_black = 1
        if i == 1:
            if len(right_array)==readings_range:
                omar_right_counter += -1 if right_array[0] else 1
                del right_array[0]
            right_array.append(is_black)
            omar_right_counter +=1 if is_black else -1
        elif i == 0:
            if len(left_array)==readings_range:
                omar_left_counter += -1 if left_array[0] else 1
                del left_array[0]
            left_array.append(is_black)
            omar_left_counter += 1 if is_black else -1
            
    omar_left_counter = readings_range if omar_left_counter >readings_range else omar_left_counter
    omar_left_counter = -readings_range if omar_left_counter <-readings_range else omar_left_counter
    
    omar_right_counter = readings_range if omar_right_counter >readings_range else omar_right_counter
    omar_right_counter = -readings_range if omar_right_counter <-readings_range else omar_right_counter
        
    

def black(live):
    #cropped_image = [live[70:110,15:305],live[120:160,15:305],live[170:240, 15:305]] #y, x
    #cropped_image = [live[90:130,15:305],live[140:180,15:305],live[190:240, 15:305]] #y, x
    cropped_image = [live[80:110,15:305],live[120:160,15:305],live[170:200, 15:305]] #y, x
    global detect_black #cropped_image = [live[90:130,15:305],live[140:180,15:305],live[190:240, 15:305]] y, x
    #cropped_image = [live[80:120,15:305],live[130:170,15:305],live[180:230, 15:305]] #y, x 2adema sh8al kelaby
    centroid_sum = 0 
    cy = 0
    cx_array =[]
    cy_correction_array = [80, 120, 170]
    cy_array = []
    area_array = []
    black_contour_list = []
    deflection_angle = 0
    w = 0
    center_pos = 0
    main_x =0
    cx = 0
    h = 0
    last_width = 0
    last_area = 0
    info_tuple = []
    area = 0
    gap_counter =0
    weight_sum=0
    
    for i,region in enumerate(cropped_image):
        cx_diff = 160
        last_cy = 0
        global black_lower
        global black_upper
        hsvf = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        black_mask = cv2.inRange(hsvf, black_lower, black_upper)
        black_result = cv2.bitwise_and(region, region, mask=black_mask)
        black_contours, black_hierarchy = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(black_contours) > 0:
            largest_black = max(black_contours, key=cv2.contourArea)
            selected_black=largest_black
            area = cv2.contourArea(selected_black)
            if(area > 800):
       
                print("area",area)
                #cv2.drawContours(region, largest_black, -1, (255, 0, 0), 3)
                #print("x of black line", x)
                print("height of black",h)
                #return cx, cy
                black_contours = sorted(black_contours, key = cv2.contourArea, reverse=True)
                for blacks in black_contours:
                    area = cv2.contourArea(blacks)
                    if area < 800:
                        break
                    M = cv2.moments(blacks)
                    if M["m00"] != 0:
                        cx =int(M["m10"]/M["m00"])
                        cy =int(M["m01"]/M["m00"]) + cy_correction_array[i]
                        
                    if i ==2:
                        print("cx ", cx)
                        print("cy ", cy)
                        
                        print("last cy ", last_cy)
                        print("cx diffrence ", cx_diff)
                        
                        if cy > last_cy and abs(cx-160) <cx_diff:
                            selected_black = blacks
                            last_cy = cy
                            
                            cx_diff=abs(cx-160)
                            print("last cy", last_cy)
                        x, y, w, h = cv2.boundingRect(selected_black)
                        main_x = x
                        last_width = w
                    else:
                        if abs(cx-160) <cx_diff:
                            selected_black = blacks
                            cx_diff=abs(cx-160)
                area = cv2.contourArea(selected_black)
                M = cv2.moments(selected_black)
                if M["m00"] != 0:
                    cx =int(M["m10"]/M["m00"])
                    cy =int(M["m01"]/M["m00"]) + cy_correction_array[i]
                    
                    if len(cx_array) and i==1 and abs(cx-cx_array[0])>100:
                        cx_array[0]=0
                    cx_array.append(cx)
                    info_tuple.append((cx,cy, area))
                    cv2.circle(region, (cx, cy- cy_correction_array[i]), 2, (255, 0, 0), 1)
                x, y, w, h = cv2.boundingRect(selected_black)
                #cv2.rectangle(region,(x,y),(x+w,y+h), (220,220,220), 2)
            else:
                cx_array.append(0)
        else:
            cx_array.append(0)
    detect_black =False
    for reg in cx_array:
        if reg:
            detect_black = True
            break
    if detect_black:
        for f in range(0,len(cx_array)):
            #print("cx array", cx_array[f])
            centroid_sum += cx_array[f] * weights[f] # r[4] is the roi weight.
            weight_sum += weights[f]*bool(cx_array[f])
        center_pos = (centroid_sum / weight_sum)
        print("center position = ", center_pos)
        deflection = (center_pos-145)/(100)
        deflection_angle = math.degrees(math.atan(deflection))
            
    return cx, cy, last_area, last_width, h, deflection_angle, gap_counter, center_pos, info_tuple, main_x
"""
hoigher =  (10, 203, 255)
lower =  (0, 89, 174)


"""

def red(im):
    cropped_red_image = im[90:240, :] #y, x
    green_blobs = []
    global detect_red
    cx = 0
    cy = 0
    w = 0
    h = 0
    area = 0
    red_lower = np.array([0, 89, 174], np.uint8)
    red_upper = np.array([10, 203, 255], np.uint8)
    hsvf_red = cv2.cvtColor(cropped_red_image, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsvf_red, red_lower, red_upper)
    red_result = cv2.bitwise_and(cropped_red_image, cropped_red_image, mask=red_mask)
    red_contours, red_hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    red_contours=sorted(red_contours,key=cv2.contourArea, reverse=True)
    if len(red_contours) >0:
        largest_red = max(red_contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_red)
        print("area:",area)
        if area >1150:
            detect_red = True



"""
hoigher =  (88, 187, 178)
lower =  (59, 109, 122)

"""
def green(live):
    cropped_green_image = live[140:200, :] #y, x
    green_blobs = []
    global detect_green
    cx = 0
    cy = 0
    w = 0
    h = 0
    area = 0
    green_lower = np.array([59, 109, 122], np.uint8)
    green_upper = np.array([88, 187, 178], np.uint8)
    hsvf_green = cv2.cvtColor(cropped_green_image, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(hsvf_green, green_lower, green_upper)
    green_result = cv2.bitwise_and(cropped_green_image, cropped_green_image, mask=green_mask)
    green_contours, green_hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(green_contours) > 0:
                green_contours=sorted(green_contours,key=cv2.contourArea, reverse=True)
                largest_green = max(green_contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_green)
                M = cv2.moments(largest_green)
                print("sorted area",area)
                #print("area ",cv2.contourArea(green_contours[2]))
                
                if(area > 2800):
                
                    print("largest",area)
                    x, y, w, h = cv2.boundingRect(largest_green)
                    #cv2.drawContours(cropped_green_image, largest_green, -1, (255, 0, 0), 3)
                    cv2.rectangle(cropped_green_image,(x,y),(x+w,y+h), (255,0,0), 5)
                    green_blobs.append(green_contours[0])
                    if len(green_contours)>1:
                        second_contour_area = cv2.contourArea(green_contours[1])
                        print("second green area : ", second_contour_area)
                        if second_contour_area>2000 :
                            x, y, w, h = cv2.boundingRect(green_contours[1])
                            cv2.rectangle(cropped_green_image,(x,y),(x+w,y+h), (255,0,0), 5)                        
                            #print("number of green blobs", len(green_contours))
                            green_blobs.append(green_contours[1])
                    
                    if M["m00"] != 0:
                        cx =int(M["m10"]/M["m00"])
                        cy =int(M["m01"]/M["m00"])+170
                        cv2.circle(cropped_green_image, (cx, cy-170), 5, (255, 255, 255), 3)
                    detect_green = True
                else:
                    detect_green = False
    else:
                detect_green = False
    print("array of green blobs", len(green_blobs))
    return cx, cy, area, w, h, green_blobs , len(green_blobs)
final_width =0
final_x = 0
final_z_right = False
final_z_left = 0
zigzag_angle = 0
turn_flag = False
triangle_area = 0
left_zigzag = False
right_zigzag = False
numberofgreens = 0
turning = False
pwm.set_pwm(5, 0, 4000)
while True:
    im = picam2.capture_array()
    im = cv2.flip(im, -1)
    im = im[ :200 ,:] 
    try:
        pitch, roll = calculate_orientation()
    except:
        pitch, roll =0,0
    print("pitch", pitch)
    if pitch <-10:
        speed2=500
        print("accelerate")
        print("pitch",pitch)
    else:
        speed2=0
    red(im)
    if detect_red:
        stop()
        time.sleep(6)
        detect_red=False
    black_cx, black_cy, black_area, black_width, black_height ,deflection_angle, gap_counter, cy_firstregion , black_info_tuple, main_x= black(im)
    green_cx, green_cy, green_area, green_width, green_height, greens, numberofgreens= green(im)
    if not(turning):
        omar_function(im)
    #print("omar right counter = ", omar_right_counter)
    #print("omar left counter = ", omar_left_counter)
    #print("omar function right region array = ",right_array)
    #print("omar function left region array = ", left_array)
    print(black_info_tuple)
    region_counter = len(black_info_tuple)
    #print("black area = ", black_area)
    print("zigzag angle = ", zigzag_angle)
    print("green cy = ",green_cy)
    #print("relative position of green y = ", relative_pos_y)
    #cv2.circle(im, (90, 200), 5, (255, 255, 255), 3)
    left_mapped_speed = int(map_value(deflection_angle, -5,-50,720,3000))
    right_mapped_speed = int(map_value(deflection_angle,50,5,3000,720))
    if numberofgreens>1:
        print("turn around")
        print("number of green blobs", len(greens))
        turn_around()
    else:
        if detect_green and detect_black:
            largest_black = max(black_info_tuple, key=itemgetter(2))
            black_cy=largest_black[1]
            largest_area_black=largest_black[2]
            relative_line_x = max(black_info_tuple, key=itemgetter(1))[0]
            black_cx=relative_line_x
            print("largest black cy  = ", largest_black)
            print("largest black area  = ", largest_area_black)
            print("cy  = ", green_cy)
            relative_pos_y = green_cy -  black_cy
            print("relative pos y", relative_pos_y)
            print("greencx ",green_cx)
            print("blackcx ",black_cx)
            #black_cx=largest_black
            if relative_pos_y > 10 and largest_area_black>2000:        
                if green_cx > black_cx:
                    print("green right")
                    if not turn_off_motion:
                        forward()
                        sleep(0.1)
                        right(800)
                        sleep(0.5)                     
                elif green_cx < black_cx:
                    print("green left")
                    if not turn_off_motion:
                        forward()
                        sleep(0.1)
                        left(800)
                        sleep(0.5)                    
            else:
                if not turn_off_motion:
                    print("green above line")
                    forward()
    print("deflection angle = ",deflection_angle)
    print("final width: ", final_width)
    if region_counter >= 2:
        turn_flag = False
        right_zigzag, left_zigzag , zigzag_angle, triangle_area= detect_triangles(im)

    if right_zigzag or left_zigzag:  
        if region_counter == 1:  
            turn_flag = True
    '''
    if not(detect_black) and final_width<70:
        print("Gap")
        if -7<=deflection_angle and deflection_angle <=7:
            if not turn_off_motion:
                forward()
            print("forwrd")
        elif deflection_angle <-7:
            if not turn_off_motion:
                left(left_mapped_speed)
                #time.sleep(0.1)
            print("left")
        elif deflection_angle>7:
            if not turn_off_motion:
                right(right_mapped_speed)
                #time.sleep(0.1)
            print("right")
        turn_flag=False
    '''
    print("turn flag ",turn_flag)
    print("how many regions have black: ", region_counter)
    if turn_flag:
        print("right zigzag flag: ", right_zigzag)
        print("left zigzag flag: ", left_zigzag)
        if right_zigzag and omar_right_counter > omar_left_counter:
            if not turn_off_motion:
                print("omar right counter >0")
                turning = True
                print("right zigzag")
                right(900)
                #sleep(0.1)
        elif left_zigzag and omar_left_counter >omar_right_counter:
            if not turn_off_motion:
                print("omar left counter >0")
                print("left zigzag")
                turning = True    
                left(900)
                #sleep(0.1)
        elif omar_left_counter < 0 and omar_right_counter<0:
            print("omar forward")
            if not turn_off_motion:
                forward()
                turning = False
            
    else:
        turning = False
        right_zigzag, left_zigzag , zigzag_angle, triangle_area= detect_triangles(im)
        if -5<deflection_angle and deflection_angle <5:
            if not turn_off_motion:
                forward()
            print("forwrd")
            entrance(im)
        elif deflection_angle <=-5:
            if not turn_off_motion:
                left(left_mapped_speed)
                #time.sleep(0.1)
            print("left")
        elif deflection_angle>=5:
            if not turn_off_motion:
                right(right_mapped_speed)
                #time.sleep(0.1)
            print("right")                    
        if detect_black:
            final_x = main_x
            final_width = black_width

    
    #cv2.imshow('cropped detection', im_cropped)
    print(" ")
    if not script:
        cv2.imshow('detection', im)
        if cv2.waitKey(1)==ord('q'):
            break
picam2.stop()
if not script:
    cv2.destroyAllWindows()



