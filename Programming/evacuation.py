from __future__ import division
from ultralytics import YOLO
import cv2
from picamera2 import Picamera2
import serial
from time import sleep
import numpy as np
import board
import gpiod
import busio
import Adafruit_PCA9685
import Adafruit_GPIO.I2C as I2C
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from libcamera import Transform
chip = gpiod.Chip('gpiochip4')
line = chip.get_line(7)#20
f = gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN
line.request("p_gpio", gpiod.LINE_REQ_DIR_IN, f)
i2c = board.I2C()
i2c_bus = 1
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=i2c_bus)

pca = PCA9685(i2c)
pca.frequency = 50

define = False

pwm.set_pwm_freq(60)

left_forward_1 = 14
left_forward_2 = 15

left_back_1 = 9
left_back_2 = 8

right_forward_1 = 12
right_forward_2 = 13

right_back_1 = 10
right_back_2 = 11

high_speed = 700
turn_speed = 600
low_speed  = 525
zero_speed = 0
def forward():
    pwm.set_pwm(left_forward_1, 0, high_speed)
    pwm.set_pwm(left_forward_2, 0, zero_speed)
    pwm.set_pwm(left_back_1, 0, high_speed)
    pwm.set_pwm(left_back_2, 0, zero_speed)
    pwm.set_pwm(right_forward_1, 0, high_speed)
    pwm.set_pwm(right_forward_2, 0, zero_speed)
    pwm.set_pwm(right_back_1, 0, high_speed)
    pwm.set_pwm(right_back_2, 0, zero_speed)
def backward():
    pwm.set_pwm(left_forward_2, 0, high_speed)
    pwm.set_pwm(left_forward_1, 0, zero_speed)
    pwm.set_pwm(left_back_2, 0, high_speed)
    pwm.set_pwm(left_back_1, 0, zero_speed)
    pwm.set_pwm(right_forward_2, 0, high_speed)
    pwm.set_pwm(right_forward_1, 0, zero_speed)
    pwm.set_pwm(right_back_2, 0, high_speed)
    pwm.set_pwm(right_back_1, 0, zero_speed)
def right():
    pwm.set_pwm(left_forward_1, 0, turn_speed)
    pwm.set_pwm(left_forward_2, 0, zero_speed)
    pwm.set_pwm(left_back_1, 0, low_speed)
    pwm.set_pwm(left_back_2, 0, zero_speed)
    pwm.set_pwm(right_forward_2, 0, turn_speed)
    pwm.set_pwm(right_forward_1, 0, zero_speed)
    pwm.set_pwm(right_back_2, 0, low_speed)
    pwm.set_pwm(right_back_1, 0, zero_speed)
def right_narrow():
    pwm.set_pwm(left_forward_1, 0, high_speed)
    pwm.set_pwm(left_forward_2, 0, zero_speed)
    pwm.set_pwm(left_back_1, 0, high_speed)
    pwm.set_pwm(left_back_2, 0, zero_speed)
    pwm.set_pwm(right_forward_2, 0, high_speed)
    pwm.set_pwm(right_forward_1, 0, zero_speed)
    pwm.set_pwm(right_back_2, 0, high_speed)
    pwm.set_pwm(right_back_1, 0, zero_speed)
def right_semi():
    pwm.set_pwm(left_forward_1, 0, turn_speed)
    pwm.set_pwm(left_forward_2, 0, zero_speed)
    pwm.set_pwm(left_back_1, 0, low_speed)
    pwm.set_pwm(left_back_2, 0, zero_speed)
    pwm.set_pwm(right_forward_2, 0, zero_speed)
    pwm.set_pwm(right_forward_1, 0, zero_speed)
    pwm.set_pwm(right_back_2, 0, zero_speed)
    pwm.set_pwm(right_back_1, 0, zero_speed)
def left():
    pwm.set_pwm(left_forward_2, 0, turn_speed)
    pwm.set_pwm(left_forward_1, 0, zero_speed)
    pwm.set_pwm(left_back_2, 0, low_speed)
    pwm.set_pwm(left_back_1, 0, zero_speed)
    pwm.set_pwm(right_forward_1, 0, turn_speed)
    pwm.set_pwm(right_forward_2, 0, zero_speed)
    pwm.set_pwm(right_back_1, 0, low_speed)
    pwm.set_pwm(right_back_2, 0, zero_speed)
def left_semi():
    pwm.set_pwm(left_forward_2, 0, zero_speed)
    pwm.set_pwm(left_forward_1, 0, zero_speed)
    pwm.set_pwm(left_back_2, 0, zero_speed)
    pwm.set_pwm(left_back_1, 0, zero_speed)
    pwm.set_pwm(right_forward_1, 0, turn_speed)
    pwm.set_pwm(right_forward_2, 0, zero_speed)
    pwm.set_pwm(right_back_1, 0, low_speed)
    pwm.set_pwm(right_back_2, 0, zero_speed)
def stop():
    pwm.set_pwm(left_forward_2, 0, high_speed)
    pwm.set_pwm(left_forward_1, 0, zero_speed)
    pwm.set_pwm(left_back_2, 0, high_speed)
    pwm.set_pwm(left_back_1, 0, zero_speed)
    pwm.set_pwm(right_forward_2, 0, high_speed)
    pwm.set_pwm(right_forward_1, 0, zero_speed)
    pwm.set_pwm(right_back_2, 0, high_speed)
    pwm.set_pwm(right_back_1, 0, zero_speed)
    sleep(0.1)
    pwm.set_pwm(left_forward_1, 0, zero_speed)
    pwm.set_pwm(left_forward_2, 0, zero_speed)
    pwm.set_pwm(left_back_1, 0, zero_speed)
    pwm.set_pwm(left_back_2, 0, zero_speed)
    pwm.set_pwm(right_forward_1, 0, zero_speed)
    pwm.set_pwm(right_forward_2, 0, zero_speed)
    pwm.set_pwm(right_back_1, 0, zero_speed)
    pwm.set_pwm(right_back_2, 0, zero_speed)

small_servo = servo.Servo(pca.channels[1], min_pulse=600, max_pulse=2900)
big_servo = servo.Servo(pca.channels[4],  min_pulse=500, max_pulse=2600, actuation_range=270)
door_servo = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2900)

big_servo.angle = 230
small_servo.angle = 40
door_servo.angle = 10
sleep(0.5)

model = YOLO('best_n.pt')#ball_detect_s.pt
picam2 = Picamera2(1)
picam2.vflip = True  # Flip vertically
picam2.hflip = True  # Flip horizontally
picam2.preview_configuration.main.size=(320,240) #full screen : 3280 2464
picam2.preview_configuration.main.format = "RGB888" #8 bits
picam2.start()

silver_ball = 0
black_ball = 0

ball = False
detect_balls = False
silver_max = False
black_max = False
detect_green = False
detect_red = False
silver_dropped = False
black_dropped = False
image_ = 0
def green_triangle(image):
    cropped_green_image = image[60:240, :320] #y, x
    green_blobs = []
    global detect_green
    cx = 0
    cy = 0
    w = 0
    h = 0
    area = 0
    green_lower = np.array([49, 62, 89], np.uint8)
    green_upper = np.array([90, 156, 218], np.uint8)
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
                    #cv2.rectangle(cropped_green_image,(x,y),(x+w,y+h), (255,0,0), 5)
                    green_blobs.append(green_contours[0])
                    if M["m00"] != 0:
                        cx =int(M["m10"]/M["m00"])
                        cy =int(M["m01"]/M["m00"])+170
                        #cv2.circle(cropped_green_image, (cx, cy-170), 5, (255, 255, 255), 3)
                    detect_green = True
                else:
                    detect_green = False
    else:
                detect_green = False
    return cx, cy, area, w, h, green_blobs
def red_triangle(image):
    cropped_green_image = image[60:240, :320] #y, x
    green_blobs = []
    global detect_red
    cx = 0
    cy = 0
    w = 0
    h = 0
    area = 0
    green_lower = np.array([0, 173, 129], np.uint8)
    green_upper = np.array([23, 235, 224], np.uint8)
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
                
                if(area > 1900):
                
                    print("largest",area)
                    x, y, w, h = cv2.boundingRect(largest_green)
                    #cv2.drawContours(cropped_green_image, largest_green, -1, (255, 0, 0), 3)
                    #cv2.rectangle(cropped_green_image,(x,y),(x+w,y+h), (255,0,0), 5)
                    green_blobs.append(green_contours[0])
                    if M["m00"] != 0:
                        cx =int(M["m10"]/M["m00"])
                        cy =int(M["m01"]/M["m00"])+170
                        #cv2.circle(cropped_green_image, (cx, cy-170), 5, (255, 255, 255), 3)
                    detect_red = True
                else:
                    detect_red = False
    else:
                detect_red = False
    return cx, cy, area, w, h, green_blobs
def silver_detection(image):
    global image_
    image_ = image[60:240, :320] #y, x
    results = model.track(image_, conf=0.15, verbose=False)
    image_ = results[0].plot()
    cx = 0
    cy = 0
    c = 0,0,0,0
    h = 0
    w = 0
    max_cx = 0
    max_cy = 0
    max_ball = 0
    global detect_balls, silver_max, black_max
    for result in results:
        c = result.boxes.xywh.ravel().tolist()# To get the coordinates
        if len(c)>3:
            detect_silver = True
            cx, cy, w, h = c[0], c[1], c[2], c[3]
            area = w * h
            if area > max_ball:
                max_ball = area
    for result in results:
        #print(result.boxes.xywh)
        c = result.boxes.xywh.ravel().tolist()# To get the coordinates
        if len(c)>3:
            detect_balls = True
            cx, cy, w, h = c[0], c[1], c[2], c[3]
            area = w * h
            #print('area', max_ball)
            #print("x = ", cx,"y = ", cy,"w = ", w,"h = ", h)
            center_point=(int(cx), int(cy))
            start_x = int(cx) - int(w/2)
            start_y = int(cy) - int(h/2)
            end_x = int(cx) + int(w/2)
            end_y = int(cy) + int(h/2)
            start_point=(start_x,start_y)
            end_point=(end_x,end_y)
            if area == max_ball:
                max_cx = cx
                max_cy = cy
                #print(result.boxes.cls[0])
                #cv2.circle(image_, center_point, 8, (0, 0, 255), -1)
            if result.boxes.cls[0] == 1:
                cv2.circle(image_, center_point, 5, (255, 0, 0), -1)
            if  result.boxes.cls[0]== 0:
                cv2.circle(image_, center_point, 5, (255, 255, 255), -1)
            #cv2.circle(image_, center_point, 5, (255, 255, 255), -1)
            #cv2.rectangle(image_, start_point, end_point, (0, 0, 255), 8)
        else:
            detect_balls = False
    return max_cx, max_cy, image_, h, result.boxes.cls
def grab():
    global silver_ball
    x = 0
    stop()
    sleep(0.4)
    backward()
    sleep(0.1)
    stop()
    sleep(0.2)
    big_servo.angle = 120
    sleep(0.2)
    small_servo.angle = 0
    sleep(0.3)
    '''
    while line.get_value() == 1:
        forward()
        x += 1
        if x == 400:
            silver_ball=0
            break
    '''
    forward()
    sleep(0.8)
    small_servo.angle = 60
    sleep(0.2)
    backward()
    sleep(0.5)
    big_servo.angle = 230
    stop()
    sleep(0.5)
    
def drop_green():
    silver_dropped = True
    silver_max = False
    black_max = False
    forward()
    sleep(1.3)
    stop()
    sleep(0.1)
    backward()
    sleep(0.7)
    right_narrow()
    sleep(1.6)
    stop()
    sleep(0.1)
    backward()
    sleep(0.8)
    stop()
    door_servo.angle = 35
    sleep(0.5)
    forward()
    sleep(0.1)
    backward()
    sleep(0.1)
    stop()
    sleep(0.3)
    forward()
    sleep(1.4)
    stop()
    sleep(0.1)
def drop_red():
    black_dropped = True
    silver_max = False
    black_max = False
    forward()
    sleep(1.3)
    stop()
    sleep(0.1)
    backward()
    sleep(0.7)
    right_narrow()
    sleep(1.6)
    stop()
    sleep(0.1)
    backward()
    sleep(0.8)
    stop()
    door_servo.angle = 70
    sleep(0.8)
    forward()
    sleep(0.5)
    door_servo.angle = 0
    stop()
    sleep(0.2)
    right()
    sleep(1.1)
    stop()
    sleep(0.2)
def drop_silver_box():
    global silver_ball
    ball = False
    #silver_ball = silver_ball + 1
    silver_max = False
    black_max = False
    stop()
    sleep(0.2)
    big_servo.angle = 270
    sleep(0.4)
    small_servo.angle = 0
    sleep(0.4)
    small_servo.angle = 5
    sleep(0.2)
    big_servo.angle = 240
    sleep(0.7)
    #small_servo.angle = 40
def drop_black_box():
    global black_ball
    ball = False
    #black_ball = black_ball + 1
    silver_max = False
    black_max = False
    stop()
    sleep(0.1)
    big_servo.angle = 230
    sleep(0.2)
    small_servo.angle = 10
    sleep(0.4)
    small_servo.angle = 0
    sleep(0.2)
    big_servo.angle = 240
    sleep(0.4)
    #small_servo.angle = 40

entered_eva = False
while True:
    image = picam2.capture_array()
    image = cv2.flip(image, -1)
    green_triangle_cx, green_triangle_cy, green_triangle_area, green_triangle_width, green_triangle_height, green_blobs = green_triangle(image)
    red_triangle_cx, red_triangle_cy, red_triangle_area, red_triangle_width, red_triangle_height, red_blobs = red_triangle(image)
    #if detect_silver:
        #print("silver_cx",silver_cx,"silver_cy",silver_cy)
    #print(ball_height)
    #print(results)
    if entered_eva == False:
        forward()
        sleep(2)
        stop()
        sleep(0.1)
        left()
        sleep(0.7)
        stop()
        sleep(0.1)
        backward()
        sleep(0.8)
        stop()
        sleep(1)
        entered_eva = True
    elif silver_ball >= 2 and black_ball >= 1:
        if silver_dropped == False and black_dropped == False:
            pwm.set_pwm(5, 0, 4000)
            if detect_green:
                if green_triangle_area >= 25000 and green_triangle_cx > 140 and green_triangle_cx < 180:
                    #silver_ball = 0
                    silver_max = False
                    black_max = False
                    drop_green()
                    silver_dropped = True
                elif green_triangle_cx > 140 and green_triangle_cx < 180:
                    forward()
                elif green_triangle_cx < 140:
                    left_semi()
                elif green_triangle_cx > 180:
                    right_semi()
            else:
                right_narrow()
        if silver_dropped == True and black_dropped == False:
            pwm.set_pwm(5, 0, 0)
            if detect_red:
                if red_triangle_area >= 25000 and red_triangle_cx > 140 and red_triangle_cx < 180:
                    #silver_ball = 0
                    silver_max = False
                    black_max = False
                    drop_red()
                    black_dropped = True
                elif red_triangle_cx > 140 and red_triangle_cx < 180:
                    forward()
                elif red_triangle_cx < 140:
                    left_semi()
                elif red_triangle_cx > 180:
                    right_semi()
            else:
                right_narrow()
    elif ball == False:
        ball_cx, ball_cy, image_, ball_height, results=silver_detection(image)
        pwm.set_pwm(5, 0, 0)
        if detect_balls:
            if ball_height >= 75 and ball_cx > 130 and ball_cx < 190:
                #ball = True
                grab()
                if results[0] == 1:
                    silver_ball = silver_ball + 1
                    drop_silver_box()
                    silver_max = True
                    black_max = False
                elif results[0] == 0:
                    black_ball = black_ball+1
                    drop_black_box()
                    silver_max = False
                    black_max = True
            elif ball_cx > 140 and ball_cx < 180:
                forward()
            elif ball_cx < 140:
                left_semi()
            elif ball_cx > 180:
                right_semi()
        else:
            right()
    # visualize
    cv2.imshow('frame', image_)
    if cv2.waitKey(1) == 27:
        break









