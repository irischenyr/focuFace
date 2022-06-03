# coding = utf-8
'''
实现一个功能：1.控制二轴云台
'''
import face_recognition
import numpy as np
import cv2
import time
import signal
import RPi.GPIO as GPIO
import sys
sys.path.append("..")
import mywork.PCA9685 as PCA9685
import mywork.yuntai as yuntai
import mywork.light as light
#import PCA9685

pwm=PCA9685.PCA9685(0x40)#对地址初始化
pwm.set_pwm_freq(50)#对频率初始化

#人脸初始中心位置
x0, y0 = 83, 76

def setServoAngle(channel, angle):  #上下舵机3 左右舵机7  
    pulse = int(4096*((angle*11)+500)/20000)
    pwm.set_pwm(channel, 0, pulse)

def setcarAngle_back(): #按下手柄粉色方格键,复原舵机函数
    setServoAngle(3,90)
    time.sleep(0.5)
    setServoAngle(7,90)
    time.sleep(0.5)
    setServoAngle(11,90)

def turn_left():  #按下手柄左键，小车转向函数
    setServoAngle(11,70)
def turn_right():  #按下手柄右键，小车转向函数
    setServoAngle(11,110)
def straight():   #按下手柄右键，小车转向函数
    setServoAngle(11,90)

def face_recog():
    setcarAngle_back()
    print("Capturing image.")
    while True:
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        video_capture.release()
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        output = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(output)

        if face_locations:
            x = (face_locations[0][1] + face_locations[0][3])/2
            y = (face_locations[0][0] + face_locations[0][2])/2
            #print(x, y)
        else:
            x, y = 83, 76  #x的范围10（右）~~ 83 ~~156（左）, y的范围20（上）~~ 76 ～132（下）
                            #dx的范围-73 ～～ 0 ～～ 73 ，dy的范围 -56 ～～ 0 ～～ 56
                            #x的50 ～～ 90 ～～ 130， y的角度范围 70 ～～ 90 ～～ 110
        global x0, y0
        dx = x-x0 
        dy = y-y0
        dx0 = int(90-dx/1.825)
        dy0 = int(90+dy/1.87)
        print(dx0, dy0)
        print('————————————————')
        if dx >= 3 or dx <= -3: 
            if dx0 > 130:
                dx0 = 130
            elif dx0 < 50:
                dx0 = 50
            setServoAngle(7, dx0)
        if dy >= 3 or dy <=-3:
            if dy0 > 110:
                dy0 = 110
            elif dy0 < 70:
                dy0 = 70
            setServoAngle(3, dy0)
        time.sleep(1)

def face_quit():
    # decide when to quit
    time.sleep(4.21)
    setcarAngle_back()

if __name__ == '__main__':
    face_recog()

    '''setServoAngle(7,90)
    time.sleep(1)
    setServoAngle(3,90)
    time.sleep(1)
    setServoAngle(11,90)'''
