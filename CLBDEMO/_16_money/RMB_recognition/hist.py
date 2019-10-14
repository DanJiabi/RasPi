#-*- encoding:utf-8 -*-
# @author: zdl
# 绘制图像直方图

import cv2
import numpy as np
from scipy.misc import imresize
from matplotlib import pyplot as plt


# 基于轮廓定位QR位置
def find_ROI(img):
    
    # 高斯滤波
    blur = cv2.GaussianBlur(img,(5,5),0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret,th = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # 形态学操作
    mask=cv2.erode(th,None,iterations=4)
    mask=cv2.dilate(mask,None,iterations=4)
    # 图像反色
    cv2.bitwise_not(mask, mask)

    # 寻找轮廓
    _,contours,hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
    # 寻找ROI的位置
    if len(contours)>0:
        cnt = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(cnt)
        #img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
		
        img_ROI = img[y:y+h, x:x+w]
        '''
         寻找旋转的边界矩形
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = list(box)
        print box
        cv2.line(img,(box[0][0],box[0][1]),(box[1][0],box[1][1]),(0,0,255),3)
        cv2.line(img,(box[0][0],box[0][1]),(box[3][0],box[3][1]),(0,0,255),3)
        cv2.line(img,(box[1][0],box[1][1]),(box[2][0],box[2][1]),(0,0,255),3)
        cv2.line(img,(box[2][0],box[0][1]),(box[3][0],box[3][1]),(0,0,255),3)
        '''
       
    else:
        img_ROI = img

    return img_ROI

def RMB_distinguish(bgr):
    if 200<=bgr[0]<= 224 and 170<=bgr[1]<=200 and 208<=bgr[2]<=240:
        print ('RMB: 100')
    elif 60<=bgr[0]<= 100 and 130<=bgr[1]<=180 and 140<=bgr[2]<=185:
        print ('RMB: 50')
    elif 60<=bgr[0]<= 100 and 180<=bgr[1]<=220 and 208<=bgr[2]<=255:
        print ('RMB: 20')
    elif 140<=bgr[0]<= 190 and 110<=bgr[1]<=160 and 100<=bgr[2]<=150:
        print ('RMB: 10')
    elif 180<=bgr[0]<= 224 and 180<=bgr[1]<=220 and 200<=bgr[2]<=230:
        print ('RMB: 5')
    elif 120<=bgr[0]<= 170 and 160<=bgr[1]<=210 and 170<=bgr[2]<=210:
        print ('RMB: 1')
    else:
        print ('None')


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
    bgr =([])
    while True:

        ret, img = cap.read()

        imgRoi = find_ROI(img)
        imgRoi = img[40:120, 30:90]
#img = imresize(img, (240,320))

        color = ('b', 'g', 'r')

        for i, col in enumerate(color):
            hist = cv2.calcHist([imgRoi],[i],None,[256],[0,256])
            hist_max = np.where(hist == np.max(hist)) # 获取直方图最大的值及其索引
            print (hist_max[0])
            bgr.append(hist_max[0])
            
        RMB_distinguish(bgr)
    #plt.plot(hist, color = col)
    #plt.xlim([0,256])

        cv2.imshow('image', img)
        cv2.imshow('Roi', imgRoi)
        if cv2.waitKey(1) & 0xFF == 27:
            break

# pyplot 绘图
 
#plt.show()

    cap.release()
    cv2.destroyAllWindows()
