# -*- coding: utf-8 -*-
# @Time : 2018/11/20 2:01
# @Author : Ed
# @File : rr.py
# -*- coding: utf-8 -*-
# @Time : 2018/11/20 1:47
# @Author : Ed
# @File : as.py


import numpy as np
import cv2
import os#

bitmap = cv2.imread("pencil_drawing12.jpg")
cv2.imwrite('.tmp.bmp', bitmap)
os.system('potrace.exe .tmp.bmp -s --flat')
# criteria = (cv2.TERM_CRITERIA_EPS, 10, 1.0)
# K =32
# Z = bitmap.reshape((-1, 3))
#
# Z = np.float32(Z)
# ret, label, center = cv2.kmeans(
#     Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
#
#
# center = np.uint8(center)
# res = center[label.flatten()]
# res = res.reshape(bitmap.shape)
# no = 1
# for i in center:
#     no += 1
#     res2 = cv2.inRange(res, i, i)
#     res2 = cv2.bitwise_not(res2)
#     cv2.imwrite(str(no)+'.tmp.bmp', res2)
#     os.system('potrace.exe '+str(no)+'.tmp.bmp -s --flat')
#     print(no)