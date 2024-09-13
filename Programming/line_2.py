import cv2
import numpy as np
from time import sleep

cap = cv2.VideoCapture(0)
detect_black = False
detect_red = False
detect_green = False
cap.set(3, 480)
cap.set(4, 720)
#ROI= np.array([[(120,height),(120,220),(750,220),(750,height)]], dtype= np.int32)
def black(live):
    cropped_image = live[450:480, 1:720]
    global detect_black
    cx = 0
    cy = 0
    hsvf = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
    black_lower = np.array([69, 100, 79], np.uint8)
    black_upper = np.array([87, 200, 114], np.uint8)
    black_mask = cv2.inRange(hsvf, black_lower, black_upper)
    black_result = cv2.bitwise_and(cropped_image, cropped_image, mask=black_mask)
    black_contours, black_hierarchy = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, black_contour in enumerate(black_contours):
        area = cv2.contourArea(black_contour)
        if(area > 1000):
            x, y, w, h = cv2.boundingRect(black_contour)
            live = cv2.rectangle(live, (x, y),
                                       (x + w, y + h),
                                       (0, 0, 255), 2)

            cv2.putText(cropped_image, "black", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))

        if len(black_contours) > 0:
            detect_black = True
            c = max(black_contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx =int(M["m10"]/M["m00"])
                cy =int(M["m01"]/M["m00"])
                cv2.circle(cropped_image, (cx, cy), 5, (255, 255, 255), 3)
                #return cx, cy
        if len(black_contours) == 0:
            detect_black = False
        cv2.rectangle()
        cv2.drawContours(cropped_image, black_contours, -1, (255, 0, 0), 3)
    return cx, cy


def green(live):
    global detect_green
    cx = 0
    cy = 0
    hsvf = cv2.cvtColor(live, cv2.COLOR_BGR2HSV)
    green_lower = np.array([69, 100, 79], np.uint8)
    green_upper = np.array([87, 200, 114], np.uint8)
    green_mask = cv2.inRange(hsvf, green_lower, green_upper)
    green_result = cv2.bitwise_and(live, live, mask=green_mask)
    green_contours, green_hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, green_contour in enumerate(green_contours):
        area = cv2.contourArea(green_contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(green_contour)
            live = cv2.rectangle(live, (x, y),
                                       (x + w, y + h),
                                       (0, 0, 255), 2)

            cv2.putText(live, "red", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))

        if len(green_contours) > 0:
            detect_green = True
            c = max(green_contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx =int(M["m10"]/M["m00"])
                cy =int(M["m01"]/M["m00"])
                cv2.circle(live, (cx, cy), 5, (255, 255, 255), 3)
                #return cx, cy
        else:
            detect_green = False
        cv2.drawContours(live, green_contours, -1, (255, 0, 0), 3)
    return cx, cy


def red(live):
    global detect_red
    cx = 0
    cy = 0
    hsvf = cv2.cvtColor(live, cv2.COLOR_BGR2HSV)
    red_lower = np.array([69, 100, 79], np.uint8)
    red_upper = np.array([87, 200, 114], np.uint8)
    red_mask = cv2.inRange(hsvf, red_lower, red_upper)
    red_result = cv2.bitwise_and(live, live, mask=red_mask)
    red_contours, red_hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, red_contour in enumerate(red_contours):
        area = cv2.contourArea(red_contour)
        if(area > 300):
            x, y, w, h = cv2.boundingRect(red_contour)
            live = cv2.rectangle(live, (x, y),
                                       (x + w, y + h),
                                       (0, 0, 255), 2)

            cv2.putText(live, "red", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))

        if len(red_contours) > 0:
            detect_red = True
            c = max(red_contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx =int(M["m10"]/M["m00"])
                cy =int(M["m01"]/M["m00"])
                cv2.circle(live, (cx, cy), 5, (255, 255, 255), 3)
                #return cx, cy
        else:
            detect_red = False
        cv2.drawContours(live, red_contours, -1, (255, 0, 0), 3)
    return cx, cy

while (True):
    ret, frame =cap.read()
    black_cx, black_cy=black(frame)
    green_cx, green_cy = green(frame)
    red_cx, red_cy = red(frame)
    if black_cx > 0 and black_cy > 0:
        if black_cx < 280:
            print('left')

        elif black_cx > 280 and black_cx < 330:
            print('forward')

        elif black_cx > 330:
            print('right')
    else:
        pass
    '''
    if detect_green == True:
        if green_cx < 280:
            print('left')

        elif green_cx > 280 and green_cx < 330:
            print('forward')

        elif green_cx > 330:
            print('right')

    if detect_red == True:
        if red_cx < 280:
            print('left')

        elif red_cx > 280 and red_cx < 330:
            print('forward')

        elif red_cx > 330:
            print('right')
    '''


    cv2.imshow('detection', frame)

    if cv2.waitKey(1) & 0xff == 27:
        break

cap.release()
cv2.destroyAllWindows()


    
