#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 02:46:03 2018

@author: pi
"""

from __future__ import division
import cv2
import time 
import numpy as np
import socket

ip_port=('127.0.0.1',7779)
sk=socket.socket()
sk.bind(ip_port)
sk.listen(5)

cap=cv2.VideoCapture(0)
print(00)
cap.set(3,320)
cap.set(4,160)
face_cascade=cv2.CascadeClassifier('123.xml')

x=0
conn,add=sk.accept()

while 1:
    print(00)
    
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray)
    
    if len(faces)>0:
        for(x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+h,y+w),(0,255,0),2)
            result=(x,y,w,h)
            x=result[0]
            y=result[1]
        print('x',x)
        data=str(x)+','+str(y)
        conn.sendall(data.encode('utf-8'))
        #s.sendto(data.encode('utf-8'),addr)
    cv2.imshow("capture",frame)
    if cv2.waitKey(1)==119:
        break
cap.release()
cv2.destroyAllWindows()
#s.close()