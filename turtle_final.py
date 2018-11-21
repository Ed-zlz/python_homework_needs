# -*- coding: utf-8 -*-
# @Time : 2018/11/8 2:04
# @Author : Ed
# @File : turtle_final.py
import sys
import win32api

from bs4 import BeautifulSoup
import cv2
import numpy
import os
import turtle


def Bezier_1(p0, p1, t):
    """
    计算以第一个点为起点，第二个点为终点，t处的插值
    Args:
        p1:第一个点
        p2:第二个点
        t:插点

    Returns:返回插值

    """
    return (1 - t) * p0 + t * p1


# def Bezier_2(x0, y0, x1, y1, x2, y2):
#     """
#         绘制贝塞尔曲线
#     Args:
#         x1:
#         y1:
#         x2:
#         y2:
#         x3:
#         y3:
#
#     """
#     #坐标转换未实现
#     turtle.penup()
#     turtle.goto(x1, y1)
#     turtle.pendown()
#     for t in range(0, drawStep + 1):
#         x = Bezier_1(Bezier_1(x0, x1, t / drawStep),
#                      Bezier_1(x1, x2, t / drawStep),
#                      t / drawStep)
#         y = Bezier_1(Bezier_1(y0, y1, t / drawStep),
#                      Bezier_1(y1, y2, t / drawStep),
#                      t / drawStep)
#         turtle.goto(x,y)
#     turtle.penup()

def Bezier_3(x0, y0, x1, y1, x2, y2, x3, y3):
    # SVG坐标转换绝对坐标
    x0 = -Width / 2 + x0
    y0 = Height / 2 - y0
    x1 = -Width / 2 + x1
    y1 = Height / 2 - y1
    x2 = -Width / 2 + x2
    y2 = Height / 2 - y2
    x3 = -Width / 2 + x3
    y3 = Height / 2 - y3
    turtle.penup()
    turtle.goto(x0, y0)
    turtle.pendown()
    for t in range(0, drawStep + 1):
        x = Bezier_1(Bezier_1(Bezier_1(x0, x1, t / drawStep), Bezier_1(x1, x2, t / drawStep), t / drawStep),
                     Bezier_1(Bezier_1(x1, x2, t / drawStep), Bezier_1(x2, x3, t / drawStep), t / drawStep),
                     t / drawStep)
        y = Bezier_1(Bezier_1(Bezier_1(y0, y1, t / drawStep), Bezier_1(y1, y2, t / drawStep), t / drawStep),
                     Bezier_1(Bezier_1(y1, y2, t / drawStep), Bezier_1(y2, y3, t / drawStep), t / drawStep),
                     t / drawStep)
        turtle.goto(x, y)
    turtle.penup()


def Moveto(x, y):
    turtle.penup()
    turtle.goto(-Width / 2 + x, Height / 2 - y)
    turtle.pendown()


def Moveto_r(dx, dy):
    turtle.penup()
    turtle.goto(turtle.xcor() + dx, turtle.ycor() - dy)
    turtle.pendown()


def Line(x0, y0, x1, y1):
    turtle.penup()
    turtle.goto(-Width / 2 + x0, Height / 2 - y0)
    turtle.pendown()
    turtle.goto(-Width / 2 + x1, Height / 2 - y1)
    turtle.penup()


def Lineto(x, y):
    turtle.pendown()
    turtle.goto(-Width / 2 + x, Height / 2 - y)
    turtle.penup()


def Lineto_r(dx, dy):
    turtle.pendown()
    turtle.goto(turtle.xcor() + dx, turtle.ycor() - dy)
    turtle.penup()


def Curveto(x0, y0, x1, y1, x, y):
    turtle.penup()
    xNow = turtle.xcor() + Width / 2
    yNow = Height / 2 - turtle.ycor()
    Bezier_3(xNow, yNow, x0, y0, x1, y1, x, y)
    global xNote, yNote
    xNote = x - x1
    yNote = y - y1
    # ????


def Curveto_r(x0, y0, x1, y1, dx, dy):
    turtle.penup()
    xNow = turtle.xcor() + Width / 2
    yNow = Height / 2 - turtle.ycor()
    Bezier_3(xNow, yNow, xNow + x0, yNow + y0,
             xNow + x1, yNow + y1, xNow + dx, yNow + dy)
    global xNote, yNote
    xNote = dx - x1
    yNote = dy - y1


def transform(attr):
    funcs = attr.split(' ')
    for func in funcs:
        func_name = func[0: func.find('(')]
        if func_name == 'scale':
            global scale
            scale = (float(func[func.find('(') + 1: -1].split(',')[0]),
                     -float(func[func.find('(') + 1: -1].split(',')[1]))


def readPathAttrD(attr):
    ulist = attr.split(' ')
    for i in ulist:
        if i.isdigit() or i.isalpha():
            yield float(i)
        elif i[0].isalpha():
            yield i[0]
            yield float(i[1:])
        elif i[-1].isalpha():
            yield float(i[0: -1])
        elif i[0] == '-':
            yield float(i)


def drawSVG(filename, now_color):
    SVGFile = open(filename, 'r')
    SVG = BeautifulSoup(SVGFile.read(), 'lxml')
    Height = float(SVG.svg.attrs['height'][0: -2])
    Width = float(SVG.svg.attrs['width'][0: -2])
    transform(SVG.g.attrs['transform'])
    global flag
    if flag:
        turtle.setup(width=Width, height=Height)
        turtle.setworldcoordinates(-Width / 2, 300,
                                   Width - Width / 2, -Height + 300)  # 自定义坐标系，坐标转换
        flag = False
    turtle.tracer(100)
    turtle.pensize(1)
    turtle.speed(drawSpeed)
    turtle.penup()
    turtle.color(now_color)

    for i in SVG.find_all('path'):
        attr = i.attrs['d'].replace('\n', ' ')
        f = readPathAttrD(attr)
        lastI = ''
        for i in f:
            if i == 'M':
                turtle.end_fill()
                Moveto(f.__next__() * scale[0], f.__next__() * scale[1])
                turtle.begin_fill()
            elif i == 'm':
                turtle.end_fill()
                Moveto_r(f.__next__() * scale[0], f.__next__() * scale[1])
                turtle.begin_fill()
            elif i == 'C':
                Curveto(f.__next__() * scale[0], f.__next__() * scale[1],
                        f.__next__() * scale[0], f.__next__() * scale[1],
                        f.__next__() * scale[0], f.__next__() * scale[1])
                lastI = i
            elif i == 'c':
                Curveto_r(f.__next__() * scale[0], f.__next__() * scale[1],
                          f.__next__() * scale[0], f.__next__() * scale[1],
                          f.__next__() * scale[0], f.__next__() * scale[1])
                lastI = i
            elif i == 'L':
                Lineto(f.__next__() * scale[0], f.__next__() * scale[1])
            elif i == 'l':
                Lineto_r(f.__next__() * scale[0], f.__next__() * scale[1])
                lastI = i
            elif lastI == 'C':
                Curveto(i * scale[0], f.__next__() * scale[1],
                        f.__next__() * scale[0], f.__next__() * scale[1],
                        f.__next__() * scale[0], f.__next__() * scale[1])
            elif lastI == 'c':
                Curveto_r(i * scale[0], f.__next__() * scale[1],
                          f.__next__() * scale[0], f.__next__() * scale[1],
                          f.__next__() * scale[0], f.__next__() * scale[1])
            elif lastI == 'L':
                Lineto(i * scale[0], f.__next__() * scale[1])
            elif lastI == 'l':
                Lineto_r(i * scale[0], f.__next__() * scale[1])
    turtle.penup()
    turtle.update()
    SVGFile.close()


def getSVG(image):
    temp = image.reshape((-1, 3))  # 转换为3列二维数组
    kmeans_data = numpy.float32(temp)  # 转换为numpy.float32，速度快
    kmeans_K = 32  # 分类数
    kmeans_bestLabel = None  # 无分类标签
    kmeans_criteria = (cv2.TERM_CRITERIA_EPS, 10, 1.0)  # 迭代停止的模式选择，精确度满足1.0时停止
    kmeans_attempt = 10  # 重复试验kmeans算法10次，返回最好结果
    kmeans_flag = cv2.KMEANS_RANDOM_CENTERS  # 初始中心随机选择
    compactness, label, center = cv2.kmeans(
        kmeans_data, kmeans_K, kmeans_bestLabel, kmeans_criteria, kmeans_attempt, kmeans_flag)
    center = numpy.uint8(center)
    response = center[label.flatten()]  # 折叠成一维数组
    response = response.reshape(image.shape)
    print('2')
    for i in center:
        response2 = cv2.inRange(response, i, i)
        response2 = cv2.bitwise_not(response2)
        cv2.imwrite('.tmp.bmp', response2)
        os.system('potrace.exe .tmp.bmp -s --flat')  # 矢量化图片，Aurhor：Peter Selinger
        drawSVG('.tmp.svg', '#%02x%02x%02x' % (i[2], i[1], i[0]))
    os.remove('.tmp.bmp')
    os.remove('.tmp.svg')
    turtle.done()


if __name__ == "__main__":
    drawStep = 15  # 贝塞尔函数插值取样次数（越大越平滑）
    drawSpeed = 1000  # 画图速度
    # 贝塞尔函数手柄记录
    xNote = 0
    yNote = 0
    scale = (1, 1)
    flag = True
    Width = 600
    Height = 600
    image = cv2.imread('01.jpg')
    if image.shape[0] > win32api.GetSystemMetrics(1):
        print('1')
        bitmap = cv2.resize(image, (int(image.shape[1] * (
            (win32api.GetSystemMetrics(1) - 50) / image.shape[0])), win32api.GetSystemMetrics(1) - 50))
    getSVG(image)
