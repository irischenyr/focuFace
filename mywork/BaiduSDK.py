# coding=utf-8
'''
文字与语音转换功能
'''
import sys
sys.path.append("..")
import mywork.vadSound as vadSound
#import vadSound
from aip import AipSpeech

APP_ID = '25091886'  # 百度AI平台申请后换为自己的，下同
API_KEY = 'mO54t8zHDfNxlRzRKckbQ2vx'
SECRET_KEY = 'pEvqOUiLfXXfsRbt4Y1btpcRNOykuEKO'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def text2sound(words='sorry'):  #文字转语音
    # text to sound function
    result = client.synthesis(words, 'zh', 1, {
        'vol': 5, 'aue': 6, 'per': 4
    })

    if not isinstance(result, dict):
        with open('/home/pi/Documents/focuface/temp.wav', 'wb') as f:
            f.write(result)
        return True
    else:
        return False


def sound2text(file_path='/home/pi/Documents/focuface/temp.wav'):   #语音转文字
    # sound to text function
    with open(file_path, 'rb') as fp:
        recog = client.asr(fp.read(), 'wav', 16000, {'dev_pid': 1536})
        if recog['err_no'] not in [0, 3301]:
            return False, recog['err_no']
        elif recog['err_no'] == 3301:
            return True, ''
        return True, recog['result'][0]

if __name__ == '__main__':
    text2sound('语音合成出错')
    vadSound.play_sound()
    # result = sound2text()
