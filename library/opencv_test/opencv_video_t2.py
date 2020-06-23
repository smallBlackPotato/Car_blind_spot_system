import cv2
import numpy as np
 
# VideoCapture()用来捕获视频设备的ID，device = 0表示只有一个摄像头
device = 1
cap = cv2.VideoCapture(device)
 
# fourcc(Four-Character-Codes)：独立显示视频数据流格式的四字符编码
# 定义视频编码器为XVID
fourcc = cv2.VideoWriter_fourcc(*'XVID') 
 
# 设定输出视频的名称和格式，以及帧率和分辨率
out = cv2.VideoWriter('output12.mp4', fourcc, 24.0, (640, 480))
 
while True:
    # ret的返回值为True或者False，表示有没有读取到图片；frame表示一帧图片
    ret,frame = cap.read() 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 灰度视频流的参数设置
    out.write(frame) # 将视频保存
    cv2.imshow('frame', frame) # 显示原视频流
    cv2.imshow('gray', gray) # 显示灰度格式的视频流
 
    if cv2.waitKey(1) == ord('q'): # 按下q后退出条件成立
            break
 
# 释放内存
cap.release()
out.release()
cv2.destroyAllWindows()