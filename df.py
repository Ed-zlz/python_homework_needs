# -*- coding: utf-8 -*-
# @Time : 2018/11/20 2:37
# @Author : Ed
# @File : df.py
# -*- coding: utf-8 -*-            555555
"""
Created on Thu Mar 23 19:14:31 2017

@author: Administrator
"""

from PIL import Image

old = Image.open('5.jpg')
new = Image.new('L', old.size, 255)
w, d = old.size

old = old.convert('L')

# Define the size of the pencil:
PEN_SIZE = 2
COLOR_DIFF = 30

for i in range(PEN_SIZE + 1, w - PEN_SIZE - 1):
    for j in range(PEN_SIZE + 1, d - PEN_SIZE - 1):
        originalcolor = 255
        lcolor = sum([old.getpixel((i - r, j))
                      for r in range(PEN_SIZE)]) // PEN_SIZE
        rcolor = sum([old.getpixel((i + r, j))
                      for r in range(PEN_SIZE)]) // PEN_SIZE
        if abs(lcolor - rcolor) > COLOR_DIFF:
            originalcolor -= (255 - old.getpixel((i, j))) // 2
            new.putpixel((i, j), 0)

        ucolor = sum([old.getpixel((i, j - r))
                      for r in range(PEN_SIZE)]) // PEN_SIZE
        dcolor = sum([old.getpixel((i, j + r))
                      for r in range(PEN_SIZE)]) // PEN_SIZE
        if abs(ucolor - dcolor) > COLOR_DIFF:
            originalcolor -= (255 - old.getpixel((i, j))) // 2
            new.putpixel((i, j), 0)

new.save('pencil_drawing12.jpg')