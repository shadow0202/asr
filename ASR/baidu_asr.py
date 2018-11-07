# -*- coding:utf-8 -*-
import json
import urllib2
import base64, requests
from sys import argv

import os

import time


def getRes(d):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=TtdyFcwHSGnG8MnQaLI0AIeD&client_secret=9b8e085ad3c21b7116a2938c9faa12f0'
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()
    data = json.loads(content)
    token = data["access_token"]

    data = {
        "format": "pcm",
        # "format": "wav",
        "rate": 16000,
        "channel": 1,
        "token": token,
        "cuid": "huxw",
        "len": len(d),
        "speech": base64.encodestring(d).replace('\n', '')
    }

    result = requests.post('http://vop.baidu.com/server_api', json=data, headers={'Content-Type': 'application/json'})
    data_result = result.json()

    # print data_result['err_msg']

    if data_result['err_msg']=='success.':
        return  data_result['result'][0].encode('utf-8')
    else:
        return data_result


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files

if __name__ == '__main__':
    wav_path = argv[1]
    res_path = argv[2]
    l = file_name(wav_path)
    txt_file = open(res_path, 'a')
    for audio_file in l:
        d = open(wav_path + '\\' + audio_file, 'rb').read()
        try:
            text = getRes(d)
            print (wav_path + '\\' + audio_file)
            print(text)
            txt_file.write(wav_path + '\\' + audio_file + "###" + text + '\n')
            print('------------------------------------------')
        except Exception as e:
            print (wav_path + '\\' + audio_file)
            print('请求超时', e)
            txt_file.write(wav_path + '\\' + audio_file + "###" + '请求超时' + '\n')
            print('------------------------------------------')

        time.sleep(1)
