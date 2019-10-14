#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, hunan CLB Tech
    * @file        speech-recognition
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""
from aip import AipSpeech
#这里需要填你自己的id和密钥
APP_ID='16226519'
API_KEY='5KVxQVES4LSja0u2G4y8m1O9'
SECRET_KEY='KhaXYwGLSmQYgnwHkuXKpV9MO2ta0bQ8'
#初始化
aipSpeech=AipSpeech(APP_ID,API_KEY,SECRET_KEY)
#读文件
def get_file_content(filePath):
    with open(filePath,'rb') as fp:
        return fp.read()
#参数请查阅技术文档，格式是amr，语言是中文
result=aipSpeech.asr(get_file_content('/home/pi/CLBDEMO/_8_speech/8k.amr'),'amr',8000,{
        'lan':'zh',
        })
print(result['result'][0])