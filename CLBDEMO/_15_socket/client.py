#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file        socket_client
    * @version      V1.0
    * @details
    * @par History
    @author: zhulin
"""

import socket
import threading

#设置socket的工作模式是tcp/ip
#请根据自身情况自行修改ip地址
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('192.168.100.14',9999))                    #wifi
true=True
#同样的我们将rec数据写在线程中
def rec(s):
    global true
    while true:
        t=s.recv(1024).decode('utf8')
        if t=='exit':
            true=False
        print('client recieved: '+t)
trd=threading.Thread(target=rec,args=(s,))

trd.start()
while true:
    #请注意raw_input()和input的区别
    t=raw_input()
    #send
    s.send("client said: "+t.encode('utf8'))
    if t=='exit':
        true=False
s.close()
