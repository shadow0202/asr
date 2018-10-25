# -*- coding:utf-8 -*-
import base64
import hashlib
import random
import string
import urllib
import requests
import time

# 单次请求中，语音时长上限15秒。
# 只支持中文普通话语音识别，后续开放更多语种的识别能力。


# 申请账号后分配的appid和appkey，都是起一个对用户以及所使用模块的标识作用
appid = 1106965956
appkey = 'p2gf4Ji1cXxwKPCF'

# 读取音频文件
d = open(r'C:\Users\huxw\Desktop\222.wav','rb').read()

# 组装调用接口时，需要携带的信息。
def get_params():
    #请求时间戳
    timestamp = int(time.time())
    #随机字符串
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits,16))

    #请求接口时候需要携带的信息
    params = {
        'app_id':appid,
        "format": 2,    # 语音格式对应的标识
                        # PCM	1
                        # WAV	2
                        # AMR	3
                        # SILK	4
        "rate": 16000,
        "speech": base64.b64encode(d),  # base64编码
        "time_stamp": timestamp,
        "nonce_str": nonce_str,
        #'sign': '',
    }

    # get_token  先获取调接口时需要验证的sign， 这个sign在他们网站上已经给出获取的步骤
    # 1、字典排序
    sort_dict = sorted(params.items(),key=lambda item:item[0],reverse=False)
    # 2、尾部添加appkey
    sort_dict.append(('app_key',appkey))
    # 3、urlcode编码
    rawtext = urllib.urlencode(sort_dict).encode()
    # 4、md5加密计算
    sha = hashlib.md5()
    sha.update(rawtext)
    md5text = sha.hexdigest().upper()

    # 然后将sign添加到params
    params['sign'] = md5text
    return params


#发出请求
url = "https://api.ai.qq.com/fcgi-bin/aai/aai_asr"
heads = {}
heads[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
result = requests.post(url,headers = heads,data=get_params())
data_result = result.json()
print data_result['data']['text']

