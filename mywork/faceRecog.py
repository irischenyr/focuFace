# coding=utf-8
'''
实现三个功能：1.拍摄照片；2.编码；3.上传百度人脸识别
'''
from aip import AipFace
import cv2
import os
import numpy as np
import urllib.request
import RPi.GPIO as GPIO
import base64
import time
import sys
sys.path.append("..")
import mywork.vadSound as vadSound
import mywork.BaiduSDK as BaiduSDK
import mywork.light as light
import mywork.yuntai as yuntai

#百度人脸识别API账号信息
APP_ID = '25176827'
API_KEY = '26n5bGyUr7QK2IBeFrDq1ile'
SECRET_KEY ='Gqu8U16GL6Z8WtbH8xWvE4Y9wZOgGx8w'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)#创建一个客户端用以访问百度云
#图像编码方式
IMAGE_TYPE='BASE64'

#用户组
GROUP = 'person'
no_time = 0
c_light = light.control_light()  #初始化状态灯控制实例
image_path = r'/Documents/focuface/faceimage.jpg'

def getimage():
    cap = cv2.VideoCapture(0)
    cv2.waitKey(5)
    while True:
        if cap.isOpened():
            cap.set(3,640)
            cap.set(4,480)
            ret, frame = cap.read()
            cv2.imwrite("faceimage.jpg", frame)
            cap.release()
            break
        else:
            continue

def transimage():
    f = open('faceimage.jpg', 'rb')
    img = base64.b64encode(f.read())
    return img

def go_api(image):
    global no_time
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP)#在百度云人脸库中寻找有没有匹配的人脸
    if result['error_msg'] == 'SUCCESS':
        vadSound.play_sound('resources/beep_lo.wav')
        name = result['result']['user_list'][0]['user_id']#获取名字
        score = result['result']['user_list'][0]['score']#获取相似度
        print(score)
        if score >= 60:#如果相似度大于60
            c_light.light_green()  #绿灯亮
            if name == 'yurong':
                print("你好%s !" % name)
                vadSound.play_sound('resources/yurong.wav')  #是否开启拍摄
                time.sleep(1)
            if name == 'qiuping':
                print("你好%s !" % name)
                vadSound.play_sound('resources/qiuping.wav')  #是否开启拍摄
                time.sleep(1)
            return 2  #为2
        if 30 < score < 60:
            print("对不起，我还不认识你！可以告诉我你的名字吗")
            vadSound.play_sound('resources/newpeople.wav')
            return 1  #为1

    if result['error_msg'] == 'pic not has face':
        c_light.light_red()  #红灯亮
        return 0
    else:
        print(result['error_code']+' ' + result['error_code'])
        c_light.light_red()  #红灯亮
        return 0

#测试主函数
if __name__ == '__main__':
    while True:
        print('准备')
        if True:
            getimage()#拍照
            img = transimage()#转换照片格式
            res = go_api(img)#将转换了格式的图片上传到百度云
            time.sleep(3)