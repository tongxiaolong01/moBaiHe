# coding=utf-8
import uiautomator2 as u2

import cv2
image = d.screenshot(format='opencv')
cv2.imwrite('updateResult\home.jpg', image)