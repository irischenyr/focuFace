#coding:utf-8
import time
import sys
import signal
from mywork import light,yuntai,vadSound,BaiduSDK,tulingRobot,motivation
from Snowboy import snowboydecoder

smp_car = motivation.Motor()  # 初始化电机控制实例
smp_car.setup()     # 初始化引脚

ENA_pwm = smp_car.pwm(smp_car.ENA)  # 初始化使能信号PWM，A为左边车轮

smartcar = motivation.MovingControl(smp_car,ENA_pwm)  # 初始化车辆运动控制实例

infrared = light.Infrared()  # 初始化红外避障实例
infrared.setup()       # 初始化红外避障引脚

handler = light.SIGINT_handler()  #初始化中断程序实例
signal.signal(signal.SIGINT, handler.signal_handler)

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def infra_control(infra_value):
    """红外避障传感器控制"""
    if infra_value == 0:  # 值为0时，表示检测到障碍物
        smartcar.brake()
        time.sleep(0.5)
    if infra_value == 1:  #值为1时，表示没有障碍物，前进
        smartcar.forward()
        time.sleep(0.5)
    print(infra_value)

def call_back_chat():  #自定义回调函数
    global detector
    vadSound.play_sound('resources/zaine.wav')
    print('小佛：在呢')
    #detector.terminate()  #释放资源
    while True:
        vadSound.record_sound()
        ret, text_inputs = BaiduSDK.sound2text()
        if text_inputs == '关机':
            vadSound.play_sound('resources/guanji.wav')
            break
        if text_inputs == '开启识别':
            tulingRobot.tuling_chat()

        if text_inputs == '开启跟随':
            while True:
                infra_value = infrared.infra_detect()
                infra_control(infra_value)
                time.sleep(0.5)
                if handler.SIGINT:
                    break
                else:
                    continue
        if text_inputs == '远程控制':
            print('按键启动')
            while True:
                ps=ps2.PS2KEY(19,13,6,5)
                if ps.ps2_key():
                    print(ps.ps2_key())
                    if ps.ps2_key() == 16:
                        yuntai.setcarAngle_back()  #按下粉色方格键，复原舵机初始位置
                    if ps.ps2_key() == 5:  #控制小车前进
                        while True:
                            smartcar.forward()
                            if handler.SIGINT:
                                break
                            else:
                                continue
                    if ps.ps2_key() == 7:  #控制小车后退
                        while True:
                            smartcar.reverse()
                            if handler.SIGINT:
                                break
                            else:
                                continue
                    if ps.ps2_key() == 15:  #控制小车停止
                        while True:
                            smartcar.brake()
                            if handler.SIGINT:
                                break
                            else:
                                continue

                    if ps.ps2_key() == 8: #控制小车右转
                        yuntai.turn_right()
                    
                    if ps.ps2_key() == 6: #控制小车左转
                        yuntai.turn_left()

                    if ps.ps2_key() == 11: #控制小车直走
                        yuntai.straight()

                    if handler.SIGINT:
                        break
                    else:
                        continue
        else:
            tuling_text = tulingRobot.tuling(text_inputs)
            print('小佛：{}'.format(tuling_text))

            if BaiduSDK.text2sound(tuling_text):
                vadSound.play_sound()
            else:
                vadSound.play_sound('home/pi/Documents/focuface/resources/fail_TTS.wav')
                print('语音合成出错。。。')

            if handler.SIGINT:
                break
            else:
                continue

def wake_up():
    global detector
    model = 'resources/xiaofo.pmdl'
    # capture SIGINT signal, e.g., Ctrl+C
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    print('Listening... Press Ctrl+C to exit')
    detector.start(detected_callback=call_back_chat,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)
    detector.terminate()

if __name__ == '__main__':
    call_back_chat()
    '''while True:
        infra_value = infrared.infra_detect()
        infra_control(infra_value)
        time.sleep(0.5)
        if handler.SIGINT:
            break
        else:
            continue'''

#python smartcar.py xiaofo.pmdl 运行语句