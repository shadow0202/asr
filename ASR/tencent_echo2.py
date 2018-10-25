# -*- coding: utf-8 -*-
"""
# @Author  : huxw 
# @Update  : 2018/10/23 16:35 
# @Software: PyCharm
"""
import base64
import random
import wave
from re import DEBUG
import time
import json
import urllib
import hashlib

import os
import requests


def urlencode(args):
    tuples = [(k, args[k]) for k in sorted(args.keys()) if args[k]]
    query_str = urllib.urlencode(tuples)
    return query_str

def signify(args, app_key):
    query_str = urlencode(args)
    query_str = query_str + '&app_key=' + app_key
    signiture = md5(query_str)
    return signiture


def md5(string):
    md = hashlib.md5()
    md.update(string)
    md5 = md.hexdigest().upper()
    return md5


def http_post(api_url, args):
    resp = requests.post(url=api_url, data=args)
    resp = json.loads(resp.text)
    return resp

class BaseASR(object):
    ext2idx = {'pcm': '1', 'wav': '2', 'amr': '3', 'slk': '4'}

    def __init__(self, api_url, app_id, app_key):
        self.api_url = api_url
        self.app_id = app_id
        self.app_key = app_key

    def stt(self, audio_file, ext, rate):
        print "异常"

class BasicASR(BaseASR):
    """ Online ASR from Tencent
    https://ai.qq.com/doc/aaiasr.shtml
    """
    def __init__(self, api_url='https://api.ai.qq.com/fcgi-bin/aai/aai_asr',
                 app_id=1106965956, app_key='p2gf4Ji1cXxwKPCF'):
        super(BasicASR, self).__init__(api_url, app_id, app_key)

    def stt(self, audio_file, ext='wav', rate=16000):
        if ext == 'wav':
            wf = wave.open(audio_file)
            nf = wf.getnframes()
            audio_data = wf.readframes(nf)
            wf.close()
        else:
            raise Exception("Unsupport audio file format!")

        args = {
            'app_id': self.app_id,
            'time_stamp': str(int(time.time())),
            'nonce_str': '%.x' % random.randint(1048576, 104857600),
            'format': self.ext2idx[ext],
            'rate': str(rate),
            'speech': base64.b64encode(audio_data),
        }

        signiture = signify(args, self.app_key)
        args['sign'] = signiture
        resp = http_post(self.api_url, args)
        text = resp['data']['text'].encode('utf-8')

        # if DEBUG:
        #     print('msg: %s, ret: %s, format: %s' %
        #           (resp['msg'], resp['ret'], resp['data']['format']))

        return text

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


def test_basic_asr():
    asr_engine = BasicASR()
    l = file_name(r'C:\Users\huxw\Desktop\ch')
    for audio_file in l:
        text = asr_engine.stt('C:\\Users\\huxw\\Desktop\\ch\\'+audio_file)
        print(text)
        time.sleep(1)

if __name__ == '__main__':
    test_basic_asr()