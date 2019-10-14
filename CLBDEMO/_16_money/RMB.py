# -*- coding: UTF-8 -*-
# find_contour.py
"""
    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file         RMB.py
    * @version      V1.0
    * @details
    * @par History
    @author: zhulin
"""
import cv2
import time 
import numpy as np
import threading
from aip import AipSpeech
import pygame
#初始化baidu speech（填入自己的信息，没有填入信息之前不能用） 
APP_ID='XXXX'
API_KEY='XXXX'
SECRET_KEY='XXXX'

aipSpeech=AipSpeech(APP_ID,API_KEY,SECRET_KEY)
def xx(RMB):
    print('111111111111')
    text=RMB
    result = aipSpeech.synthesis(text = text, 
                             options={'spd':5,'vol':9,'per':0,})
    if not isinstance(result,dict):
        with open('audio.mp3','wb') as f:
            f.write(result)  
    else:print(result)

    pygame.mixer.init()
    pygame.mixer.music.load('audio.mp3')
    pygame.mixer.music.play()
def thr(RMB):
    tid=threading.Thread(target=xx,args=(RMB,))
    tid.setDaemon(True)
    tid.start()
    
DELAY=0.02
USE_CAM=1
IS_FOUND=0
MORPH=7
CANNY=250
_width=600.0
_height=420.0    
_margin=0.0

if USE_CAM:
    video_capture=cv2.VideoCapture(0)
"""
def find_ROI(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    ret,th = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)#+cv2.THRESH_OTSU)

    mask=cv2.erode(th,None,iterations=4)
    mask=cv2.dilate(mask,None,iterations=4)
 
    cv2.bitwise_not(mask, mask)

    _,contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	

    if len(contours)>0:
        cnt = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(cnt)
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
		
        img_ROI = img
    else:
        img_ROI = img

    return img_ROI
"""

def color_hist(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hist_mask = cv2.calcHist([hsv], [0], None, [180], [0, 180])
    object_H = np.where(hist_mask==np.max(hist_mask)) 
    print (object_H[0])
    
    return object_H[0]

corners=np.array(
        [
		[[  		_margin, _margin 			]],
		[[ 			_margin, _height + _margin  ]],
		[[ _width + _margin, _height + _margin  ]],
		[[ _width + _margin, _margin 			]],
	]
        )
pts_dst=np.array(corners,np.float32)

sendTime=0
while True:

    if USE_CAM:
        ret, rgb= video_capture.read()
    else:
        ret=1
        rgb=cv2.imread("opencv.jpg",1)
    if (ret):
        gray=cv2.cvtColor(rgb,cv2.COLOR_BGR2GRAY)
        gray=cv2.bilateralFilter(gray,1,10,120) 
        edges=cv2.Canny(gray,10,CANNY)
        
        kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(MORPH,MORPH))
        closed=cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel)       
        image,contours,_=cv2.findContours(closed,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for cont in contours:

            if cv2.contourArea(cont)>5000:
                arc_len=cv2.arcLength(cont,True)
                approx=cv2.approxPolyDP(cont,0.1*arc_len,True)
                if(len(approx)==4):
                    IS_FOUND=1
                    pts_src=np.array(approx,np.float32)
                    h,status=cv2.findHomography(pts_src,pts_dst)
                    out=cv2.warpPerspective(rgb,h,(int(_width+_margin*2),int(_height+_margin*2)))
                    cv2.drawContours(rgb,[approx],-1,(255,0,0),2)
                else:
                    pass                

        cv2.namedWindow('edges',cv2.WINDOW_AUTOSIZE)
        cv2.imshow('edges',edges)
        cv2.namedWindow('rgb',cv2.WINDOW_AUTOSIZE)
        cv2.imshow('rgb',rgb)
        if IS_FOUND:
            cv2.namedWindow('out',cv2.WINDOW_AUTOSIZE)
            cv2.imshow('out',out)
            cv2.imwrite('out.png',out)
            img = cv2.imread('out.png', 1)

            """
            img_ROI = find_ROI(img)    
            object_H=color_hist(img_ROI)
            """
            object_H = color_hist(img)            
            try:
                print (object_H)
                currentTime=time.time()
                if object_H > 11 and object_H < 25: 
                    RMB = 20
                    if currentTime-sendTime>5:
                        thr(RMB)
                        sendTime=time.time()
                elif object_H > 35 and object_H < 43: 
                    RMB = 1
                    if currentTime-sendTime>5:
                        thr(RMB)
                        sendTime=time.time()
                elif object_H > 50 and object_H < 80: 
                    RMB = 50
                    if currentTime-sendTime>5:
                        thr(RMB)
                        sendTime=time.time()
                elif object_H > 100 and object_H < 124: 
                    RMB = 10
                    if currentTime-sendTime>5:
                        thr(RMB)
                        sendTime=time.time()
                elif object_H > 125 and object_H < 155: 
                    RMB = 5
                    if currentTime-sendTime>5:
                        thr(RMB)
                        sendTime=time.time()
                elif object_H > 156 and object_H < 180: 
                    RMB = 100
                    if currentTime-sendTime>5:
                        thr(RMB)
                        sendTime=time.time()
                else: RMB = 'none'
                print ('RMB:',RMB ,'yuan')

            except:
                pass
            

            cv2.imshow('image', img)
            
            
        if cv2.waitKey(27)& 0xFF==ord('q'):
            break
        time.sleep(DELAY)
    else: 
        print("Stopped")
        break
if USE_CAM:
    video_capture.release()
cv2.destroyAllWindows()
