import time
import numpy as np
import cv2
from mss import mss

from win32gui import FindWindow, GetWindowRect
from pynput.keyboard import Key, Controller

keyboard = Controller()

scale = 1.5
state = 0 # 0: entering number, 1: idle,
count = 0

check_pos = (430, 538) # WH
red_pos = [(175+i, 260+j) for i in range(0, 192+1, 48) for j in range(0, 192+1, 48)]
blue_pos = [(160+i, 550+j) for i in range(0, 192+1, 48) for j in range(0, 192+1, 48)]

# FindWindow takes the Window Class name (can be None if unknown), and the window's display text. 
window_handle = FindWindow(None, "MuMu模拟器12")
window_rect = GetWindowRect(window_handle)
print(window_rect)
bounding_box = int(window_rect[0] * scale), int(window_rect[1] * scale), int((window_rect[2]) * scale), int((window_rect[3]) * scale)
print(bounding_box)


sct = mss()

while True:
    count = 0
    sct_img = sct.grab(bounding_box)
    img = np.array(sct_img)

    # check color at check_pos. HWC
    if(abs(img[check_pos[1], check_pos[0], 2] - 180) < 15 and abs(img[check_pos[1], check_pos[0], 1] - 180) < 15):
        # print('found')
        if (state == 0):
            print('found')
            time.sleep(2)

            # grab the image again
            sct_img = sct.grab(bounding_box)
            img = np.array(sct_img)

            # check each red_pos and blue_pos. if red_pos and blue_pos is gray(150), increment count
            for pos_r, pos_b in zip(red_pos, blue_pos):
                if (abs(img[pos_r[1], pos_r[0], 0] - 150) < 15 and abs(img[pos_r[1], pos_r[0], 1] - 150) < 15) \
                    and (abs(img[pos_b[1], pos_b[0], 0] - 150) < 15 and abs(img[pos_b[1], pos_b[0], 1] - 150) < 15):
                    count += 1
            count = 25 - count
            print(count)

            if count != 0:
                # enter count
                print(f"Entering {count}")
                keyboard.press(str(count//10))
                keyboard.release(str(count//10))
                time.sleep(0.25)
                keyboard.press(str(count%10))
                keyboard.release(str(count%10))

            # change state
            state = 1
    else:
        state = 0

    # draw red_pos and blue_pos on the image
    for pos in red_pos:
        cv2.circle(img, pos, 5, (0, 0, 255), -1)
    for pos in blue_pos:    
        cv2.circle(img, pos, 5, (255, 0, 0), -1)
    # draw check_pos
    cv2.circle(img, check_pos, 5, (0, 255, 0), -1)

    cv2.imshow('window', img)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break