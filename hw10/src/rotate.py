import os
import cv2
import math
import imageio
import numpy as np
from scipy import misc, ndimage

if __name__ == '__main__':
    allFileList = os.listdir("./111598067")
    index = 0
    for file in allFileList:
        index += 1
        img_path = './111598067/' + file
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Canny Edge Detection
        edge = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Hough Tranform
        lines = cv2.HoughLines(edge, 1, np.pi/180, 0)
        rotate_angle = 0
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            if x1 == x2 or y1 == y2:
                continue
            t = float(y2 - y1) / (x2 - x1)
            rotate_angle = math.degrees(math.atan(t))
            if rotate_angle > 45:
                rotate_angle = -90 + rotate_angle
            elif rotate_angle < -45:
                rotate_angle = 90 + rotate_angle
        print('rotate_angle : ' + str(rotate_angle))

        rotate_img = ndimage.rotate(img, rotate_angle)
        # imageio.imsave('rotated.png', rotate_img) # color will change
        cv2.imwrite('./output/rotated_{0}.png'.format(index), rotate_img)
        # cv2.imshow("img", rotate_img)
        cv2.waitKey(0)