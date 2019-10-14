#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, hunan CLB Tech
    * @file        socket_bigprograme
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""
from flask import Flask, render_template, Response
import cv2
import sys
import numpy as np
import socket
import threading
import time
import random
from PIL import Image
import Adafruit_PCA9685
import RPi.GPIO as GPIO
from aip import AipSpeech
import pygame

import base64
import hashlib
reload(sys)
sys.setdefaultencoding('utf-8')

_charset = 'utf-8'
_delim = '#'
#初始化baidu speech（填入自己的信息，没有填入信息之前不能用） 
APP_ID='XXXX'
API_KEY='XXXX'
SECRET_KEY='XXXX'
aipSpeech=AipSpeech(APP_ID,API_KEY,SECRET_KEY)



leftrightpulse=500
updownpulse=390
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

pwm.set_pwm(1,0,leftrightpulse)
time.sleep(0.1)
pwm.set_pwm(2, 0,updownpulse)
time.sleep(0.1)


R,G,B=9,10,11
buzzer=16
GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer,True)
pwmR = GPIO.PWM(R, 2000)
pwmG = GPIO.PWM(G, 2000)
pwmB = GPIO.PWM(B, 2000)
pwmR.start(0)
pwmG.start(0)  
pwmB.start(0)

pwmG.ChangeDutyCycle(0)
pwmB.ChangeDutyCycle(0)
pwmR.ChangeDutyCycle(0)

secondFunctiondetectedColor=''
secondFunctiondetectedRmbNoSpeech=''

app = Flask(__name__)

color_lower=np.array([156,43,46])
color_upper=np.array([180,255,255])


DELAY=0.02

IS_FOUND=0
MORPH=7
CANNY=250
_width=600.0
_height=420.0    
_margin=0.0

def get_headers(data):
    """
    将请求头格式化成字典
    :param data:
    :return:
    """
    header_dict = {}
    data = str(data.encode('utf-8'))
 
    header, body = data.split('\r\n\r\n', 1)
    header_list = header.split('\r\n')
    for i in range(0, len(header_list)):
        if i == 0:
            if len(header_list[i].split(' ')) == 3:
                header_dict['method'], header_dict['url'], header_dict['protocol'] = header_list[i].split(' ')
        else:
            k, v = header_list[i].split(':', 1)
            header_dict[k] = v.strip()
    return header_dict
 

def send_msg(conn, msg_bytes):
    """
    WebSocket服务端向客户端发送消息
    :param conn: 客户端连接到服务器端的socket对象,即： conn,address = socket.accept()
    :param msg_bytes: 向客户端发送的字节
    :return:
    """
    import struct
 
    token = b"\x81"
    length = len(msg_bytes)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)
 
    msg = token + msg_bytes
    conn.send(msg)
    return True

def send(sock, data):
    global sendLock
    sendLock.acquire()
    # print("send %s" % data)
    sock.send((data + _delim).encode(_charset))
    sendLock.release()

def getTemperature(sock):
    x1 = random.randint(0, 9)
    return x1

def getHumperature(sock):
    y1 = random.randint(0, 9)
    return y1

def function4(sock):
    data = random.randint(100, 999)
    print(data)

    time.sleep(1)

def function5(sock):
    data = random.randint(1000, 9999)
    print(data)

    time.sleep(1)

def function6(sock):
    data = random.randint(10000, 99999)
    print(data)

    time.sleep(1)

def functionxy(sock):
    x = getTemperature(sock)
    y = getHumperature(sock)
    data = "x:%d,y:%d" % (x, y)
    send(sock, data) 

    time.sleep(1)

def waringfunction(sock):
    data = random.randint(0, 25)
    # print("data = %d" % data)
    if data == 25:
        print('z')
        #send(sock, 'z')
    time.sleep(2)

def movingForwardFunction():
    print('moving forward')

def movingBackFunction():
    print('moving back')

def movingLeftFunction():
    print('moving left')

def movingRightFunction():
    print('moving right')

def camUpFunction():
    print('cam up')

def camDownFunction():
    print('cam down')

def camLeftFunction():
    print('cam left')

def camRightFunction():
    print('cam right')

def dispatch(sock,cmd):
    global func4, func5, func6, funcxy
    send(sock,cmd)


# 创建新的后台子线程，并且可以暂停
class FuncWrapper:
    def __init__(self, func, sock, *args):
        self.cond = threading.Condition()
        self.running = False
        self.sock = sock
        self._func = func
        self.tid = threading.Thread(target = self.func, args = args)
        self.tid.setDaemon(True)
        self.tid.start()

    # 开始执行线程
    def run(self):
        if not self.running:
            tid = threading.Thread(target = self._run)
            tid.setDaemon(True)
            tid.start()

    def _run(self):
        while True:
            self.cond.acquire()
            if not self.running:
                self.cond.notify()
                self.cond.release()
            else:
                self.cond.release()
                break
    # 暂停线程
    def stop(self):
        if self.running:
            tid = threading.Thread(target = self._stop)
            tid.setDaemon(True)
            tid.start()

    def _stop(self):
        self.cond.acquire()
        self.running = False
        self.cond.release()

    # 线程执行的函数,注意此函数必须包含一个sock函数
    def func(self, *args):
        while True:
            self.cond.acquire()
            if not self.running:
                self.cond.wait()
                self.running = True
            self.cond.release()
            self._func(self.sock, *args)

def serveFunc(sock):
    lastCmd = ''
    while True:
        data = sock.recv(4096)
        
        
        headers = get_headers(data)
        response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                       "Upgrade:websocket\r\n" \
                       "Connection:Upgrade\r\n" \
                       "Sec-WebSocket-Accept:%s\r\n" \
                       "WebSocket-Location:ws://%s%s\r\n\r\n"
 
        value = headers['Sec-WebSocket-Key'] + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
        response_str = response_tpl % (ac.decode('utf-8'), headers['Host'], headers['url'])
        sock.send(bytes(response_str.encode('utf-8')))
        
        
        try:
            info = sock.recv(8096)
        except Exception as e:
            info = None
        if not info:
            break
        payload_len = ord(info[1]) & 127
        if payload_len == 126:
            extend_payload_len = info[2:4]
            mask = info[4:8]
            decoded = info[8:]
        elif payload_len == 127:
            extend_payload_len = info[2:10]
            mask = info[10:14]
            decoded = info[14:]
        else:
            extend_payload_len = None
            mask = info[2:6]
            decoded = info[6:]
 
        bytes_list = bytearray()
        for i in range(len(decoded)):
            chunk = ord(decoded[i]) ^ ord(mask[i % 4])
            bytes_list.append(chunk)
        body = str(bytes_list)

        
        data=body
        send_msg(sock,body.encode('gb2312'))
        
        
        
        
        
        tforspeech=str(data)
        if tforspeech.find('#speech')!=-1:
            
            word=data[7:]
        
            result = aipSpeech.synthesis(text = word, 
                                         options={'spd':3,'vol':9,'per':1,})
            if not isinstance(result,dict):
                with open('audio.mp3','wb') as f:
                    f.write(result)
        
            else:print(result)
            pygame.mixer.init()
            pygame.mixer.music.load('audio.mp3')
            pygame.mixer.music.play()
            print('recieve: '+word)
        
        
        if not data:
            # print("client Close.")
            break
        # print("recv data is : %s" % data)
        if data[-1] != '#':
            cmdList = data.split('#')
            cmdList[0] = lastCmd + cmdList[0]
            #lastCmd = opt.pop()
        else:
            cmdList = data.split('#')
            cmdList[0] = lastCmd + cmdList[0]
            lastCmd = ''
        for cmd in cmdList:
            dispatch(sock,cmd)

# 为了避免直接关闭sock，而其他线程还在发送而产生错误，所以延迟关闭sock
def waitClose(sock):
    # print(sock)
    time.sleep(10)
    sock.close()

def init(ip, port):
    listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSock.bind((ip, port))
    listenSock.listen(5)
    global func4, func5, func6, funcxy
    func4 = FuncWrapper(function4, None)
    func5 = FuncWrapper(function5, None)
    func6 = FuncWrapper(function6, None)
    funcxy = FuncWrapper(functionxy, None)
    waringfunc = FuncWrapper(waringfunction, None)

    global sendLock
    sendLock = threading.Lock()

    try:
        while True:
            connsock, address = listenSock.accept()

            func4.sock = connsock
            func5.sock = connsock
            func6.sock = connsock
            funcxy.sock = connsock
            waringfunc.sock = connsock
            waringfunc.run()

            serveFunc(connsock);

            waringfunc.stop();
            func4.stop()
            func5.stop()
            func6.stop()
            funcxy.stop()

            closeTid = threading.Thread(target = waitClose, args = [connsock])
            closeTid.setDaemon(True)
            closeTid.start()
    finally:
        listenSock.close()

if __name__ == '__main__':
    ip = '192.168.100.66'
    port = 4021
    init(ip, port)
