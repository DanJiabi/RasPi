#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file        socket server
    * @version      V1.0
    * @details
    * @par History
    
    @author: zhulin
"""
import socket
import threading
#设置socket的模式是tcp/ip
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#这里我们用就用到了静态ip
#请根据自身情况自行修改port
address='192.168.100.66'        #wifi
port =9902
#绑定地址和端口号
s.bind((address,port))
#设置允许接入的服务器的个数
s.listen(2)
sock,addr=s.accept()
true=True

#把收写到线程中，避免拥塞
def rec(sock):
    global true
    while true:
        #设置编码格式为utf-8
        t=sock.recv(1024).decode('utf8')
        #当输入内容为exit的时候退出
        if t=='exit':
            true=False
        print('recieve: '+t)
trd=threading.Thread(target=rec,args=(sock,))
trd.start()
while true:
    t=raw_input()
    sock.send(t.encode('utf8'))
    if t=='exit':
        true=False
s.close()
