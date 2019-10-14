#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    * @par Copyright (C): 2010-2019, Hunan CLB Tech
    * @file        motion_detected_simple
    * @version      V1.0
    * @details
    * @par History
    @author: zhulin
"""
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
 
# 使用参数解释器简化对参数的控制
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
 
# 我们将使用usb摄像头，而不是自带picam，picam的配置方法请看教程
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
 
#如果没有找到camera，查看是否本地有video
else:
	vs = cv2.VideoCapture(args["video"])
# 初始化
firstFrame = None

while True:
    #把第一帧设置为比较帧
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	text = "Unoccupied"
	if frame is None:
		break
 
	# 重定义frame的大小，灰度图转换
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	if firstFrame is None:
		firstFrame = gray
		continue
	# 计算第一针和当前帧的差
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
    #对图像进行膨胀，找到差值所在位置
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	for c in cnts:
		# 过滤过小的领域
		if cv2.contourArea(c) < args["min_area"]:
			continue
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"
	# 时间戳，显示在视频上
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break
 
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
