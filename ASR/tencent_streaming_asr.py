# -*- coding: utf-8 -*-
"""
# @Author  : huxw 
# @Update  : 2018/10/23 16:44 
# @Software: PyCharm

使用方法：需要穿两个参数，第一个为音频文件夹路径，第二个是结果存储路径

"""
import base64
import random
import urllib
import wave
import time
import json
import hashlib
import os
from sys import argv
import requests
from websocket._core import create_connection


def urlencode(args):
    tuples = [(k, args[k]) for k in sorted(args.keys()) if args[k]]
    query_str = urllib.parse.urlencode(tuples)
    return query_str

def signify(args, app_key):
    query_str = urlencode(args)
    query_str = query_str + '&app_key=' + app_key
    signiture = md5(query_str)
    return signiture

def md5(string):
    md = hashlib.md5()
    md.update(string.encode("utf8"))
    md5 = md.hexdigest().upper()
    return md5

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files

def http_post(api_url, args):
    resp = requests.post(url=api_url, data=args)
    # print resp.text
    resp = json.loads(resp.text)
    return resp

class BaseASR(object):
    ext2idx = {'pcm': '1', 'wav': '2', 'amr': '3', 'slk': '4'}

    def __init__(self, api_url, app_id, app_key):
        self.api_url = api_url
        self.app_id = app_id
        self.app_key = app_key

    def stt(self, audio_file, ext, rate):
        print ("异常")

class BasicStreamASR(BaseASR):
    """ Online ASR from Tencent AI Lab
    https://ai.qq.com/doc/aaiasr.shtml
    """
    def __init__(self, api_url='https://api.ai.qq.com/fcgi-bin/aai/aai_asrs',
                 app_id=1106965956, app_key='p2gf4Ji1cXxwKPCF'):
        super(BasicStreamASR, self).__init__(api_url, app_id, app_key)

    def stt(self, audio_file, ext='wav', rate=16000, chunk=6400):
        if ext == 'wav':
            wf = wave.open(audio_file)
        else:
            raise Exception("Unsupport audio file format!")

        total_len = wf.getnframes() * wf.getsampwidth()
        seq, end = 0, '0'
        nowTime = lambda: int(round(time.time() * 1000))
        total_startTime = nowTime()
        total_useTime = ''
        while end != '1':
            data = wf.readframes(chunk)
            length = len(data)
            end = '0' if length + seq < total_len else '1'
            args = {
                'app_id': self.app_id,
                'time_stamp': str(int(time.time())),
                'nonce_str': '%.x' % random.randint(1048576, 104857600),
                'format': self.ext2idx[ext],
                'rate': str(rate),
                'seq': str(seq),
                'len': str(length),
                'end': end,
                'speech_id': '0',
                'speech_chunk': base64.b64encode(data),
            }

            signiture = signify(args, self.app_key)
            args['sign'] = signiture
            startime = nowTime()
            resp = http_post(self.api_url, args)
            endtime = nowTime()
            seq += length
            usetime = endtime - startime

            # 按照规定  200ms发送一次请求，超过200毫秒的不用管
            if(usetime <= 200):
                time.sleep((200 - usetime) / 1000)

            # TODO QPS限制，待申请企业账号，消除QPS限制，然后统计时长。
            time.sleep(1)


            if end == '1':
                total_endTime = nowTime()
                total_useTime = str(total_endTime - total_startTime)
                return resp['data']['speech_text'].encode('utf-8'),total_useTime

        return resp['data']['speech_text'].encode('utf-8'),total_useTime


def main():
    asr_engine = BasicStreamASR()
    wav_path = argv[1]
    res_path = argv[2]
    l = file_name(wav_path)
    # 追加格式化文本结果
    txt_file = open(res_path,'a')
    for audio_file in l:
        try:
            text,usertime = asr_engine.stt(wav_path +'\\'+ audio_file)
            print(wav_path +'\\'+ audio_file)
            # 记录文本结果和识别时长
            # res_file = open("C:\\Users\\huxw\\Desktop\\tencent\\" + audio_file.replace("wav","txt"),'w')
            # print "C:\\Users\\huxw\\Desktop\\tencent\\" + audio_file.replace("wav","txt")
            # res_file.write(text + '\n' + str(usertime))
            text = bytes.decode(text)
            print(text)
            txt_file.write(wav_path +'\\'+ audio_file +"###"+ text +'\n')
            print('------------------------------------------')
        except Exception as e:
            print (wav_path + '\\' + audio_file)
            print('请求超时',e)
            txt_file.write(wav_path +'\\'+ audio_file + "###" + '请求超时' + '\n')
            print('------------------------------------------')

    txt_file.close()


if __name__ == '__main__':
    main()


