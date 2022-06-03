#coding:utf-8
'''
实现三个功能：1.灯光显示状态；2.红外模块调节距离；3.键盘中断
'''
import RPi.GPIO as GPIO
import time
import sys

class control_light():
    
    R,G,B = 12,13,11
    GPIO.setwarnings(False)

    # 对要使用的引脚进行初始化
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(R,GPIO.OUT)
    GPIO.setup(G,GPIO.OUT)
    GPIO.setup(B,GPIO.OUT)
    
    # 使用PWM脉冲宽度调制
    pR = GPIO.PWM(R, 50)
    pG = GPIO.PWM(G, 50)
    pB = GPIO.PWM(B, 50)

    # 开启脉冲，默认的占空比为0，灯不亮
    pR.start(0)      
    pG.start(0)
    pB.start(0)

    def light_white(self):  #初始状态
        control_light().pR.ChangeDutyCycle(100)
        control_light().pG.ChangeDutyCycle(100)
        control_light().pB.ChangeDutyCycle(100)
        time.sleep(2)

    def light_red(self):  #识别不到人脸
        control_light().pR.ChangeDutyCycle(0)
        control_light().pG.ChangeDutyCycle(100)
        control_light().pB.ChangeDutyCycle(100)
        time.sleep(2)

    def light_green(self): #正常工作
        control_light().pR.ChangeDutyCycle(100)
        control_light().pG.ChangeDutyCycle(0)
        control_light().pB.ChangeDutyCycle(100)
        time.sleep(2)

    def light_blue(self): #
        control_light().pR.ChangeDutyCycle(100)
        control_light().pG.ChangeDutyCycle(100)
        control_light().pB.ChangeDutyCycle(0)
        time.sleep(2)

    def light_yellow(self):  #识别到不是设定对象
        control_light().pR.ChangeDutyCycle(0)
        control_light().pG.ChangeDutyCycle(0)
        control_light().pB.ChangeDutyCycle(100)
        time.sleep(2)

    def light_off(self):
        control_light().pR.stop()
        control_light().pG.stop()
        control_light().pB.stop()

class Infrared():
    InfraredPin = 32  #信号针脚连接树莓派26号针脚

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(Infrared.InfraredPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def infra_detect(self):
        infra_value = 1
        if (0 == GPIO.input(Infrared.InfraredPin)):  #当检测到障碍物时，输出低电平信号
            infra_value = 0
        return infra_value
 
    def destroy(self):
        GPIO.cleanup()

class SIGINT_handler():  #信号中断
    def __init__(self):
        self.SIGINT = False
 
    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        self.SIGINT = True


