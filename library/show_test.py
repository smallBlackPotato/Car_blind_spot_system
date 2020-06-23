from datetime import datetime 
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext        # 导入滚动文本框的模块
from PIL import Image, ImageTk
import cv2
import pprint

import serial
import numpy as np
from matplotlib import pyplot as plt

import sys
import os
import threading
import time

import serial.tools.list_ports
 
plist = list(serial.tools.list_ports.comports())
 
if len(plist) <= 0:
    print ("The Serial port can't find!")
else:
    plist_0 =list(plist[0])
    serialName = plist_0[0]
    serialFd = serial.Serial(serialName,9600,timeout = 60)
    if serialFd.isOpen():
        serialFd.close()


root= tk.Tk()
root.title('汽车盲点活体监测警报系统')
root.geometry('1150x405')

#读取串口
ser = serial.Serial(serialFd.name)
#图标
root.iconbitmap("./photo/biaotou.ico")

#定义全局变量

#保存的全局变量

thread_con = 0#线程控制

total = 1
judge_l = 0
judge_r = 0
#第一帧的全局变量 
firstframe_left = None
firstframe_right = None
firstframe_judge = 0

#左右盲点控制
r_l_con = 0
#背景图片
back_picture = None

firstAvgT = 0 #平均
readCount = 8 #初始化次数
catchJudge = 0 #捕获判定
#警告信息
waring_mes_r = ' '
waring_mes_l = ' '

#确定对比帧
count_l = 0
count_r = 0

#进入测试控制
test_con = 0


capture = cv2.VideoCapture(1)
# capture = cv2.VideoCapture('output3.mp4')

ref, frame = capture.read()
cv2.imwrite('./photo/init_imaage.jpg', frame)#保存图片
height,width = cv2.imread('./photo/init_imaage.jpg').shape[:2]#输出图片的尺寸
#设置控制输出视频的大小
he_height = int(height*0.7)
wid_width = int(width*0.7)

class myThread (threading.Thread):
    def __init__(self, flag_ju):
        threading.Thread.__init__(self)
        self.flag_ju = flag_ju
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()       # 设置为True
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True
    def run(self):
        if self.flag_ju == 1:
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            readSerial()
        if self.flag_ju == 2:
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            from_video_left()
        if self.flag_ju == 3:
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            from_video_right()
    
    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()        # 设置为False 


def closecamera():
    capture.release()

def button1():
    global judge_l
    global judge_r
    global catchJudge
    judge_l = 1
    judge_r = 1
    catchJudge = 1

def clickMe1():
    global firstframe_judge
    global readCount
    readCount = 8
    firstframe_judge = 1

def clickMe2():
    global r_l_con
    r_l_con = 0

def clickMe3():
    global r_l_con
    r_l_con = 1

def clickMe4():
    os.system(r"start explorer F:\imageai_test\log")

def clickMe5():
    global test_con
    test_con = test_con + 1

def readSerial():
    global readCount
    global catchJudge
    first = []
    read = 0
    element = 0
    counter = 0

    w, h = 8, 8
    mat = [[0 for x in range(w)] for y in range(h)]

    x = 0
    y = 0
    
    while True:
        while True:
            char = ser.read()

            if read == 1:
                if char == b',':
                    mat[x][y] = element
                    x = x+1
                    element = 0
                    counter = 0
                    # ser.read()
                elif char == b'\r':
                    y = y+1
                    x = 0
                    element = 0
                    counter = 0
                    ser.read() # b'\n'
                elif char == b']':
                    read = 0
                    # print("DONE")
                    x = 0
                    y = 0
                    break
                elif char != b'-' and char != b'.':
                    element = element + int(char) * pow(10, 1-counter)
                    counter = counter + 1

            if char == b'[':
                read = 1

        conf_arr = np.asarray(mat)
        if (readCount > 0):
            first.append(np.mean(conf_arr))
            readCount = readCount - 1
            name_read.set("红外检测初始化中...")
        elif (readCount == 0):
            firstAvgT = np.mean(np.asarray(first))
            name_read.set("红外检测初始化完毕")
            readCount = readCount - 1
            if (catchJudge == 1):
                catchJudge = 0
        else:
            # human = np.mean(conf_arr) - firstAvgT > firstAvgT / 6.0 or np.var(conf_arr) > 5
            human = np.mean(conf_arr) > 20 or np.var(conf_arr) > 5
            if (human):
                name_read.set("红外检测到物体进入")
            else:
                name_read.set("红外检测中...")
            if (catchJudge == 1):
                catchJudge = 0
                log_file = open('./log/serial_log.txt', 'a')
                log_file.write('time:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + '\n')
                log_file.write('array:' + str(mat) + '\n')
                log_file.write('variance:' + str(np.var(conf_arr)) + '\n')
                log_file.write('average:' + str(np.mean(conf_arr)) + '\n')
                log_file.write('first_average:' + str(firstAvgT) + '\n')
                log_file.write('human:' + str(human) + '\n\n')
                log_file.close()
            log_file = open('./log/auto_serial_log.txt', 'a')
            log_file.write('time:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + '\n')
            log_file.write('array:' + str(mat) + '\n')
            log_file.write('variance:' + str(np.var(conf_arr)) + '\n')
            log_file.write('average:' + str(np.mean(conf_arr)) + '\n')
            log_file.write('first_average:' + str(firstAvgT) + '\n')
            log_file.write('human:' + str(human) + '\n\n')
            log_file.close()            



#获取视频函数，返回数据用于画布
def tkImage():
    ref, frame = capture.read()

    cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    pilImage = Image.fromarray(cvimage)
    pilImage = pilImage.resize((wid_width, he_height), Image.ANTIALIAS)#对图片进行缩放
    tkImage = ImageTk.PhotoImage(image=pilImage)
    return tkImage#返回的是图片

# 创建一个主菜单容器,
monty = tk.LabelFrame(root, text=" 主菜单 ")     # 创建一个容器，其父容器为win
monty.grid(column=0, row=0, padx=10, pady=10)       # padx  pady   该容器外围需要留出的空余空间


tk.Label(monty, text="警告信息：").grid(column=0, row=0)    # 添加一个标签，并将其列设置为1，行设置为0

action1 = tk.Button(monty, text="重新定位", width=13, height=1, command=clickMe1)     # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
action1.grid(column=0, row=4, pady=13)    # 设置其在界面中出现的位置  column代表列   row 代表行

action4 = tk.Button(monty, text="历史记录", height=1, width=13, command=clickMe4)
action4.grid(column=0, row=5, pady=13)

# action5 = tk.Button(monty, text="测试", height=1, width=13, command=clickMe5)
# action5.grid(column=0, row=6, pady=13)


#创建左视频区容器
monty_vedio = tk.LabelFrame(root, text=" 左盲点监测区 ")
monty_vedio.grid(column=3, row=0, padx=10, pady=10)

canvas = tk.Canvas(monty_vedio, bg='white', width=wid_width, height=he_height)
canvas.grid(column=2, row=2) 

# # 绘制画布控件位置设置
b = tk.Button(monty, text='捕获保存', width=13, height=1, command=button1)
b.grid(column=0, row=7, pady=13)

#创建右视频区容器
monty_photo = tk.LabelFrame(root, text=" 右盲点检测区 ")
monty_photo.grid(column=4, row=0, padx=10, pady=10)

canvas1 = tk.Canvas(monty_photo, bg='white', width=wid_width, height=he_height)
canvas1.grid(column=2, row=2)

#右文本框
name_right = tk.StringVar()     # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
nameEntered_right = tk.Entry(monty, width=24, textvariable=name_right)   # 创建一个文本框，定义长度为24个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
nameEntered_right.grid(column=0, row=1, sticky=tk.W, pady=6)       # 设置其在界面中出现的位置  column代表列   row 代表行
name_right.set("右摄像头初始化中...")

#左文本框
name_left = tk.StringVar()     # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
nameEntered_left = tk.Entry(monty, width=24, textvariable=name_left)   # 创建一个文本框，定义长度为24个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
nameEntered_left.grid(column=0, row=2, sticky=tk.W, pady=6)       # 设置其在界面中出现的位置  column代表列   row 代表行
name_left.set("左摄像头初始化中...")


#红外文本框
name_read = tk.StringVar()     # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
nameEntered_read = tk.Entry(monty, width=24, textvariable=name_read)   # 创建一个文本框，定义长度为24个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
nameEntered_read.grid(column=0, row=3, sticky=tk.W, pady=6)       # 设置其在界面中出现的位置  column代表列   row 代表行
name_read.set("红外检测初始化中...")


#左盲点
def from_video_left():
    global firstframe_left
    global judge_l
    global total
    global firstframe_judge
    global waring_mes_l
    global count_l
    global test_con
    #进行跟踪识别
    camera=cv2.VideoCapture(1)
    # camera = cv2.VideoCapture('output7.mp4')

    # if test_con % 2 == 0:
    #     # camera.release()
    #     camera=cv2.VideoCapture(1)
    
    # if test_con % 2 == 1:
    #     camera.release()
    #     camera = cv2.VideoCapture('output7.mp4')
    
    # firstframe=None
    while (True):

        count_l = count_l + 1

        ret,frame = camera.read()

        # print(str(type(frame)))

        # if str(type(frame)) == '':
        #     camera=cv2.VideoCapture(1)
        #     continue

        # 改变尺寸
        cv2.imwrite('./photo/temp_image.jpg', frame)#保存图片
        imag = cv2.imread('./photo/temp_image.jpg')
        im_height, im_width = imag.shape[:2]
        size = (int(im_width*1.15), int(im_height*1.15))
        frame = cv2.resize(imag, size, interpolation=cv2.INTER_CUBIC)

 

        if not ret:  
            break  
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  
        gray=cv2.GaussianBlur(gray,(21,21),0)  
        if firstframe_left is None or count_l % 3 == 0:  
            firstframe_left=gray  
            continue  
        
        if firstframe_judge == 1:
            firstframe_left = None
            firstframe_judge = 0
            continue


        frameDelta = cv2.absdiff(firstframe_left,gray)  #计算差值
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]  #阈值化
        thresh = cv2.dilate(thresh, None, iterations=2)  #膨胀图像,得到图像轮廓
        
        #绘出边框
        x,y,w,h=cv2.boundingRect(thresh) 
        frame=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)


        #切换左右盲点
        if r_l_con == 0:
            #绘制警戒线
            cv2.rectangle(frame, (486,0), (488,600), (0, 0, 255), 2) #左盲点

            #左文本框信息
            if x+w > 0 and x+w < 430:
                waring_mes_l = "左侧有活体接近盲点区域！"
            elif x+w >= 430:
                waring_mes_l = "左侧有活体进入盲点区域！"
            else:
                waring_mes_l = "左侧摄像头检测中..."

        if r_l_con == 1:
            #绘制警戒线
            cv2.rectangle(frame, (246,0), (248,600), (0, 0, 255), 2) #右盲点 

            #右文本框信息
            if x > 320:
                waring_mes_l = "右侧有活体接近盲点区域！"
            elif x <= 320 and x >= 0:
                waring_mes_l = "右侧有活体进入盲点区域！"
            else:
                waring_mes_l = "右侧摄像头检测中..."

        name_left.set(waring_mes_l)



        #转化为能在tkinter上显示的格式
        cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        pilImage = Image.fromarray(cvimage)
        pilImage = pilImage.resize((wid_width, he_height), Image.ANTIALIAS)#对图片进行缩放
        picture = ImageTk.PhotoImage(image=pilImage)

        if judge_l == 1:
            t_imag=cv2.rectangle(imag,(x,y),(x+w,y+h),(0,0,255),2)

            #获取系统当前时间
            now_time = datetime.now()
            strnow_data = datetime.strftime(now_time,'%Y-%m-%d')
            strnow_h = datetime.strftime(now_time,'%H')
            strnow_m = datetime.strftime(now_time,'%M')
            strnow_s = datetime.strftime(now_time,'%S')
            str_time = strnow_data + '_' + strnow_h + '-' + strnow_m + '-' + strnow_s

            cv2.imwrite('./photo/test_temp.jpg', t_imag)
            # cv2.imwrite('./photo/save_me_image/me_image_' + str(total) + '.jpg', t_imag)
            cv2.imwrite('./log/save_me_image/' + 'left_' + str_time + '.jpg', t_imag)
            total = total + 1
            judge_l = 0

        #在画布上面显示图片
        canvas.create_image(0, 0, anchor='nw', image=picture)
        # discern(img)
        root.update()
        root.after(150)
    capture.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 释放窗口资源
    closecamera()


#右盲点
def from_video_right():
    
    global firstframe_right
    global judge_r
    global total
    global firstframe_judge
    global waring_mes_r
    global count_r
    global test_con
    #进行跟踪识别
    camera=cv2.VideoCapture(2)
    # camera = cv2.VideoCapture('output9.mp4')


    # if test_con % 2 == 0:
    #     camera=cv2.VideoCapture(2)
    
    # if test_con % 2 == 1:
    #     camera = cv2.VideoCapture('output9.mp4')

    
    # firstframe=None
    while (True):

        count_r = count_r + 1

        ret,frame = camera.read()

        #跳转到摄像头
        # if str(type(frame)) == '':
        #     camera=cv2.VideoCapture(1)
        #     continue

        # 改变尺寸
        cv2.imwrite('./photo/temp_image.jpg', frame)#保存图片
        imag = cv2.imread('./photo/temp_image.jpg')
        im_height, im_width = imag.shape[:2]
        size = (int(im_width*1.15), int(im_height*1.15))
        frame = cv2.resize(imag, size, interpolation=cv2.INTER_CUBIC)
        #绘制警戒线
        cv2.rectangle(frame, (246,0), (248,600), (0, 0, 255), 2)  
        if not ret:  
            break  
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  
        gray=cv2.GaussianBlur(gray,(21,21),0)  
        if firstframe_right is None or count_r % 3 == 0:  
            firstframe_right=gray  
            continue  
        
        if firstframe_judge == 1:
            firstframe_right = None
            firstframe_judge = 0
            continue


        frameDelta = cv2.absdiff(firstframe_right,gray)  #计算差值
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]  #阈值化
        thresh = cv2.dilate(thresh, None, iterations=2)  #膨胀图像,得到图像轮廓
        
        #绘出边框
        x,y,w,h=cv2.boundingRect(thresh) 
        frame=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

        #文本框信息
        if x > 300:
            waring_mes_r = "右侧有活体接近盲点区域！"
        elif x <= 300 and x != 0:
            waring_mes_r = "右侧有活体进入盲点区域！"
        else:
            waring_mes_r = "右侧摄像头检测中..."

        name_right.set(waring_mes_r)



        #转化为能在tkinter上显示的格式
        cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        pilImage = Image.fromarray(cvimage)
        pilImage = pilImage.resize((wid_width, he_height), Image.ANTIALIAS)#对图片进行缩放
        picture = ImageTk.PhotoImage(image=pilImage)

        if judge_r == 1:
            t_imag=cv2.rectangle(imag,(x,y),(x+w,y+h),(0,0,255),2)

            
            #获取系统当前时间
            now_time = datetime.now()
            strnow_data = datetime.strftime(now_time,'%Y-%m-%d')
            strnow_h = datetime.strftime(now_time,'%H')
            strnow_m = datetime.strftime(now_time,'%M')
            strnow_s = datetime.strftime(now_time,'%S')
            str_time = strnow_data + '_' + strnow_h + '-' + strnow_m + '-' + strnow_s


            cv2.imwrite('./photo/test_temp.jpg', t_imag)
            # cv2.imwrite('./photo/save_me_image/me_image_' + str(total) + '.jpg', t_imag)
            cv2.imwrite('./log/save_me_image/' + 'right_' + str_time + '.jpg', t_imag)
            total = total + 1
            judge_r = 0

        #在画布上面显示图片
        canvas1.create_image(0, 0, anchor='nw', image=picture)
        # discern(img)
        root.update()
        root.after(150)
    capture.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 释放窗口资源
    closecamera()


if __name__ == "__main__":
    thread3 = myThread(3)
    thread1 = myThread(1)
    thread2 = myThread(2)
    thread3.start()
    thread1.start()
    thread2.start()
root.mainloop()