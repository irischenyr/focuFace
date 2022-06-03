# coding=utf-8
import requests
import json
import signal
import sys
sys.path.append("..")
#import Snowboy.snowboydecoder as snowboydecoder
import mywork.vadSound as vadSound
import mywork.BaiduSDK as BaiduSDK
import mywork.faceRecog as faceRecog
import mywork.light as light
import mywork.yuntai as yuntai
import mywork.motivation as motivation

c_light = light.control_light()  #初始化状态灯控制实例

handler = light.SIGINT_handler()  #初始化实例
signal.signal(signal.SIGINT, handler.signal_handler)

def tuling(text='I said nothing'):
    tuling_url = 'http://www.tuling123.com/openapi/api'
    tuling_data = {
        'key': '63ff2b08b1de4f94a97fb8f94cb35014',
        'info': text
    }  # 当你申请了自己的图灵机器人后，请将key换为你自己的
    r = requests.post(tuling_url, data=tuling_data)
    # print(r.text)
    return json.loads(r.text)['text']

def tuling_chat():
    #chat with tulingrobot
    no_time= 0
    while True:
        faceRecog.getimage()
        img = faceRecog.transimage()
        result = faceRecog.go_api(img)
        if result == 0: #识别不到对象
            no_time += 1
            if no_time >=  7:
                vadSound.play_sound('resources/result0.wav')   #多次检测不到对象
                print('检测不到人脸')
                break
            else:
                continue
        if result == 1: #识别到不是设定对象
            no_time += 1
            while True:
                if no_time >= 4:
                    break
                if no_time < 4:
                    vadSound.play_sound('resources/ding.wav')  
                    vadSound.record_sound()
                    print('语音识别中....')
                    ret, content = BaiduSDK.sound2text()
                    if not content:
                        no_time += 1
                        continue
                    if ret:
                        print('你好'+ content)
                        light.light_yellow()  #黄灯亮
                        vadSound.play_sound('resources/result2.wav')  #识别到非拍摄对象进入待机状态
                        break
                    else:
                        continue
            break
        if result == 2:  #识别到特定对象
            yuntai.face_recog() #舵机开始运动
        else:
            continue

if __name__ == '__main__':
    #测试snowboy程序
    tuling_chat()
    '''while True:
        vadSound.record_sound()
        ret, text_inputs = BaiduSDK.sound2text()
        tuling_text = tuling(text_inputs)
        print('小佛：{}'.format(tuling_text))

        if BaiduSDK.text2sound(tuling_text):
            vadSound.play_sound()
        else:
            vadSound.play_sound('resources/fail_TTS.wav')
            print('语音合成出错。。。')'''
            


    
    
