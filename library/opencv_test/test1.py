#控制视频大小
import cv2
import numpy as np
 
"""
函数名：cv2.VideoCapture()
功  能：通过摄像头捕获实时图像数据
返回值：有
参数一：摄像头代号，0为默认摄像头，笔记本内建摄像头一般为 0
       或者填写视频名称直接加载本地视频文件
"""
cap = cv2.VideoCapture(1)#创建一个 VideoCapture 对象
 
"""
函数名：cap.set( propId , value )
功  能：设置视频参数。设置视频的宽高值和摄像头有关
       使用笔记本内置摄像头时只能设置为 1280*720 以及 640*480，哪怕设置值不同时都会自动校正过来，并且仍然返回 True
返回值：布尔值
参数一：需要设置的视频参数
参数二：设置的参数值
"""
cap.set(3,480)
cap.set(4,320)
 
flag = 1;#设置一个标志，用来输出视频信息
"""
函数名：cv2.isOpened()
功  能：返回一个布尔值（ True / False ），检查是否初始化成功，成功返回 True
返回值：布尔值
"""
while(cap.isOpened()):#循环读取每一帧
    """
    函数名：cap.read()
    功  能：返回两个值
           先返回一个布尔值，如果视频读取正确，则为 True，如果错误，则为 False，也可用来判断是否到视频末尾
           再返回一个值，为每一帧的图像，该值是一个三维矩阵
           通用接收方法为：
           ret,frame = cap.read();
           这样 ret 存储布尔值，frame 存储图像
           若使用一个变量来接收两个值，如
           frame = cap.read()
           则 frame 为一个元组，原来使用 frame 处需更改为 frame[1]
    返回值：R1：布尔值
           R2：图像的三维矩阵
    """
    ret_flag , Vshow = cap.read()
    #gray = cv2.cvtColor(Vshow,cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Gray",gray)
 
    cv2.imshow("Capture_Test",Vshow)  #窗口显示，显示名为 Capture_Test
 
    k = cv2.waitKey(1) & 0xFF #每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
    if  k == ord('s'):  #若检测到按键 ‘s’，打印字符串
        """
        函数名：cap.get( propId )
        功  能：查询视频的参数
        返回值：无
        参数一：查询的视频参数，其中部分值可以使用 cap.set() 进行修改
        """
        print(cap.get(3));
        print(cap.get(4));
 
    elif k == ord('q'): #若检测到按键 ‘q’，退出
        break
 
cap.release() #释放摄像头
cv2.destroyAllWindows()#删除建立的全部窗口