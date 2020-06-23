# import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext        # 导入滚动文本框的模块
from PIL import Image, ImageTk
import cv2

import sys
sys.path.append('./')
# from library.camera import Camera
import threading
import time

# car = Camera()

root= tk.Tk()
root.title('汽车盲点活体监测警报系统')
root.geometry('1150x430')


tempimagepath = r"./photo/test1_1.jpg"

# capture = cv2.VideoCapture(1)

ref, frame = capture.read()
cv2.imwrite('./photo/init_imaage.jpg', frame)#保存图片
height,width = cv2.imread('./photo/init_imaage.jpg').shape[:2]#输出图片的尺寸
#设置控制输出视频的大小
he_height = int(height*0.7)
wid_width = int(width*0.7)
print(he_height,wid_width)

def closecamera():
    capture.release()

def button1():
    ref, frame = capture.read()
    cv2.imwrite(tempimagepath, frame)

def clickMe1(self):
    ref, frame = capture.read()
    cv2.imwrite(tempimagepath, frame)

def clickMe2(self):
    return 0

def clickMe3(self):
    return 0

def clickMe4(self):
    return 0

#追踪测试函数
def spot_test1(frame_test):
    firstframe=None  
    while True:  
        gray=cv2.cvtColor(frame_test,cv2.COLOR_BGR2GRAY)#转灰度图
        gray=cv2.GaussianBlur(gray,(21,21),0)#高斯滤波
        if firstframe is None:  
            firstframe=gray  
            continue  
        
        frameDelta = cv2.absdiff(firstframe,gray)  
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]  
        thresh = cv2.dilate(thresh, None, iterations=2)  
        # cnts= cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  
        
        x,y,w,h=cv2.boundingRect(thresh)  
        frame=cv2.rectangle(frame_test,(x,y),(x+w,y+h),(0,0,255),2)  
    
    return frame

#获取视频函数，返回数据用于画布    
def tkImage():
#进行跟踪识别
    camera=cv2.VideoCapture(1)  
    firstframe=None  
    while (True):
        ret,frame = camera.read()  
        if not ret:  
            break  
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)  
        gray=cv2.GaussianBlur(gray,(21,21),0)  
        if firstframe is None:  
            firstframe=gray  
            continue  
        
        frameDelta = cv2.absdiff(firstframe,gray)  
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]  
        thresh = cv2.dilate(thresh, None, iterations=2)  
        # cnts= cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  
        
        x,y,w,h=cv2.boundingRect(thresh)  
        frame=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)


        #转化为能在tkinter上显示的格式
        cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        pilImage = Image.fromarray(cvimage)
        # print(cvimage.mode)
        # print(pilImage.mode)
        pilImage = pilImage.resize((wid_width, he_height), Image.ANTIALIAS)#对图片进行缩放
        # print(pilImage)
        tkImage = ImageTk.PhotoImage(image=pilImage)
    return tkImage#返回的是图片实例化


# 创建一个主菜单容器,
monty = ttk.LabelFrame(root, text=" 主菜单 ")     # 创建一个容器，其父容器为win
monty.grid(column=0, row=0, padx=10, pady=10)       # padx  pady   该容器外围需要留出的空余空间

ttk.Label(monty, text="警告信息：").grid(column=0, row=0)    # 添加一个标签，并将其列设置为1，行设置为0
# ttk.Label(monty, text="Enter a name:").grid(column=0, row=1, sticky='W')      # 设置其在界面中出现的位置  column代表列   row 代表行

name = tk.StringVar()     # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
nameEntered = ttk.Entry(monty, width=24, textvariable=name)   # 创建一个文本框，定义长度为24个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
nameEntered.grid(column=0, row=1, sticky=tk.W)       # 设置其在界面中出现的位置  column代表列   row 代表行
name.set('有活体进入盲点区域！')
# nameEntered.config(textvariable='gdsgdfgdf')
# nameEntered.focus()     # 当程序运行时,光标默认会出现在该文本框中

action1 = ttk.Button(monty, text="前盲点", command=clickMe1)     # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
action1.grid(column=0, row=2, pady=13)    # 设置其在界面中出现的位置  column代表列   row 代表行

action2 = ttk.Button(monty, text="后盲点", command=clickMe2)
action2.grid(column=0, row=3, pady=13)

action3 = ttk.Button(monty, text="左盲点", command=clickMe3)
action3.grid(column=0, row=4, pady=13)

action4 = ttk.Button(monty, text="右盲点", command=clickMe4)
action4.grid(column=0, row=5, pady=13)

action5 = ttk.Button(monty, text="热成像区", command=clickMe4)
action5.grid(column=0, row=6, pady=13)


#创建视频区容器
monty_vedio = ttk.LabelFrame(root, text=" 视频监测区 ")
monty_vedio.grid(column=3, row=0, padx=10, pady=10)

canvas = tk.Canvas(monty_vedio, bg='white', width=wid_width, height=he_height)
canvas.grid(column=2, row=2) 

# # 绘制画布控件位置设置
b = tk.Button(monty, text='捕获保存', width=13, height=1, command=button1)
b.grid(column=0, row=7, pady=13)

#创建照片区容器
monty_photo = ttk.LabelFrame(root, text=" 照片显示区 ")
monty_photo.grid(column=4, row=0, padx=10, pady=10)

canvas1 = tk.Canvas(monty_photo, bg='white', width=wid_width, height=he_height)
canvas1.grid(column=2, row=2) 

# canvas.place(x=imagepos_x, y=imagepos_y)
# action1.place(x=butpos_x, y=butpos_y)

# ttk.Label(monty, text="实时监测区").grid(column=1, row=0, padx=20)

# # 创建两个容器,其父容器为monty
# labelsFrame1 = ttk.LabelFrame(monty, text='视频区')
# labelsFrame1.grid(column=1, row=1)
# ttk.Label(labelsFrame1, text="检测信息：").grid(column=2, row=0)

# labelsFrame2 = ttk.LabelFrame(monty, text='照片区')
# labelsFrame2.grid(column=1, row=2)
# ttk.Label(labelsFrame2, text="检测信息：").grid(column=2, row=0)



if __name__ == "__main__":
    picture = tkImage()
    


        canvas.create_image(0, 0, anchor='nw', image=picture)
        # ret, img = capture.read()
        # discern(img)
        root.update()
        root.after(150)
    capture.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 释放窗口资源
    closecamera()

root.mainloop()