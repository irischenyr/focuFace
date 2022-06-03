#coding:utf-8
'''
1.控制马达,；2.手柄
'''
import time
import RPi.GPIO as GPIO
import sys
sys.path.append("..")
import mywork.yuntai as yuntai


#import ps2

class Motor:
    ENA = 22  #使能信号A
    IN1 = 16  #信号输入1
    IN2 = 18  #信号输入2
    GPIO.setwarnings(False)  #关闭警告信息

    def setup(self):
        '''初始化引脚'''
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(Motor.ENA, GPIO.OUT)
        GPIO.setup(Motor.IN1, GPIO.OUT)
        GPIO.setup(Motor.IN2, GPIO.OUT)
        
    def pwm(self,pwm): 
        '''初始化PWM（脉宽调制）,返回PWM对象'''   
        EN_pwm = GPIO.PWM(pwm, 500)
        EN_pwm.start(0)
        return EN_pwm

    def changespeed(self,pwm,speed):
        '''通过改变占空比改变马达转速'''
        pwm.ChangeDutyCycle(speed)
        
    def clockwise(self,in1_pin,in2_pin):
        '''马达顺时针转的信号'''
        GPIO.output(in1_pin, 0)    
        GPIO.output(in2_pin, 1)
    
    def counter_clockwise(self,in1_pin,in2_pin):
        '''马达逆时针转的信号'''
        GPIO.output(in1_pin, 1)
        GPIO.output(in2_pin, 0)
        
    def brake(self,in1_pin,in2_pin):
        '''马达制动的信号'''
        GPIO.output(in1_pin, 0)
        GPIO.output(in2_pin, 0)
        #使能信号为高电平，IN1和IN2都为0或1时马达制
        
    def destroy(self,A):
        '''结束程序时清空GPIO状态，
        若不清空状态，再次运行时会有警告'''
        A.stop()
        GPIO.cleanup()    # Release resource

class MovingControl():
    def __init__(self,smpcar,pwm1):
        self.smpcar=smpcar
        self.ENA_pwm=pwm1
        self.rudder_value = 0
        self.acc_value = 0
	
    def straight(self):
        yuntai.straight()
        
    def leftTurn(self):
        '''原地左转弯'''
        yuntai.turn_left()
        
    def rightTurn(self):
        '''原地右转弯'''
        yuntai.turn_right()

    def forward(self):
        '''直线前进'''
        self.smpcar.counter_clockwise(self.smpcar.IN1,self.smpcar.IN2)
        self.smpcar.changespeed(self.ENA_pwm,20)
    
    def reverse(self):
        '''直线后退'''
        self.smpcar.clockwise(self.smpcar.IN1,self.smpcar.IN2)
        self.smpcar.changespeed(self.ENA_pwm,20)
       
    def brake(self):
        '''刹车'''
        self.smpcar.brake(self.smpcar.IN1,self.smpcar.IN2)


if __name__ == '__main__':     # Program start from here
    try:
        motor = Motor() #创建树莓派小车对象
        motor.setup()  #初始化引脚
        ENA_pwm = motor.pwm(motor.ENA) #初始化使能信号PWM

        while True:
            '''通过输入的命令改变马达转动
            这里是考虑到后期，远程控制也是发送控制代码实现控制，
            这里采用这种方式也很方便'''
            cmd = input("Command, E.g. ff30:")
            direction = cmd[0] #只输入字母b时，小车刹车
            A_direction = cmd[0:2] #字符串0/1两位为控制A（左边车轮）方向信号
        
            A_speed = cmd[2:4] #字符串2/3两位为控制A（左边车轮占空比）速度信号
            print (A_direction,A_speed) #测试用
        
            if A_direction == "ff": #控制A（左边车轮）顺时针信号
                motor.clockwise(motor.IN1,motor.IN2)
            if A_direction == "00": #控制A（左边车轮）逆时针信号
                motor.counter_clockwise(motor.IN1,motor.IN2)
            if direction == "b": #小车刹车，IN1和IN2都为0，马达制动
                motor.brake(motor.IN1,motor.IN2)
                continue #跳出本次循环
            # 通过输入的两位数字设置占空比(0~100)，改变马达转速
            motor.changespeed(ENA_pwm,int(A_speed))

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        motor.destroy(ENA_pwm)
    finally:
        motor.destroy(ENA_pwm)
