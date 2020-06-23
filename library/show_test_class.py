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

total = 0

class Spot_GUI():
    def __init__(self):
        self.__init_gui()

    def __button1():
    # global total#设置全局变量
    # global x
    # global y
    # global w
    # global h
    ref, frame = capture.read()
    frame=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    cv2.imwrite('./photo/test_temp.jpg', gray)
    cv2.imwrite('./photo/save_me_image/me_image_' + str(total) + '.jpg', gray)
    total = total + 1

    def __clickMe1(self):
        global firstframe
        global judge
        judge = 1
        firstframe = None

    def __clickMe2(self):
        return 0

    def __clickMe3(self):
        return 0

    def __clickMe4(self):
        return 0

    #获取视频函数，返回数据用于画布    
    def __tkImage():
        ref, frame = capture.read()

        cvimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        pilImage = Image.fromarray(cvimage)
        # print(cvimage.mode)
        # print(pilImage.mode)
        pilImage = pilImage.resize((wid_width, he_height), Image.ANTIALIAS)#对图片进行缩放
        # print(pilImage)
        tkImage = ImageTk.PhotoImage(image=pilImage)

        # print(tkImage)
        return tkImage#返回的是图片

    
    def __init_gui(self):
        capture = cv2.VideoCapture(1)

        ref, frame = capture.read()
        cv2.imwrite('./photo/init_imaage.jpg', frame)#保存图片
        height,width = cv2.imread('./photo/init_imaage.jpg').shape[:2]#输出图片的尺寸
        #设置控制输出视频的大小
        he_height = int(height*0.7)
        wid_width = int(width*0.7)
        
        root= tk.Tk()
        root.title('汽车盲点活体监测警报系统')
        root.geometry('1150x430')
        # 创建一个主菜单容器,
        monty = ttk.LabelFrame(root, text=" 主菜单 ")     # 创建一个容器，其父容器为win
        monty.grid(column=0, row=0, padx=10, pady=10)       # padx  pady   该容器外围需要留出的空余空间

        ttk.Label(monty, text="警告信息：").grid(column=0, row=0)    # 添加一个标签，并将其列设置为1，行设置为0
        # ttk.Label(monty, text="Enter a name:").grid(column=0, row=1, sticky='W')      # 设置其在界面中出现的位置  column代表列   row 代表行

        # name = tk.StringVar()     # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
        # nameEntered = ttk.Entry(monty, width=24, textvariable=name)   # 创建一个文本框，定义长度为24个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
        # nameEntered.grid(column=0, row=1, sticky=tk.W)       # 设置其在界面中出现的位置  column代表列   row 代表行
        # name.set(waring_mes)
        # # nameEntered.config(textvariable='gdsgdfgdf')
        # # nameEntered.focus()     # 当程序运行时,光标默认会出现在该文本框中

        action1 = ttk.Button(monty, text="重新定位", command=self.__clickMe1)     # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
        action1.grid(column=0, row=2, pady=13)    # 设置其在界面中出现的位置  column代表列   row 代表行

        action2 = ttk.Button(monty, text="后盲点", command=self.__clickMe2)
        action2.grid(column=0, row=3, pady=13)

        action3 = ttk.Button(monty, text="左盲点", command=self.__clickMe3)
        action3.grid(column=0, row=4, pady=13)

        action4 = ttk.Button(monty, text="右盲点", command=self.__clickMe4)
        action4.grid(column=0, row=5, pady=13)

        action5 = ttk.Button(monty, text="热成像区", command=self.__clickMe4)
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

    def launch(self):
        self.root.mainloop()

if __name__ == '__main__':
    spg = Spot_GUI()
    spg.launch()