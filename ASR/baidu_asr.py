# -*- coding:utf-8 -*-
import json
import urllib2

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=TtdyFcwHSGnG8MnQaLI0AIeD&client_secret=9b8e085ad3c21b7116a2938c9faa12f0'
request = urllib2.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib2.urlopen(request)
content = response.read()
data = json.loads(content)
token = data["access_token"]


import base64, requests
d = open('D:\\FFOutput\\16k.pcm', 'rb').read()
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
print data_result['err_msg']
if data_result['err_msg']=='success.':
    print "语音结果：" + data_result['result'][0].encode('utf-8')
else:
    print data_result