import cv2
import threading




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
            video_left()
        if self.flag_ju == 2:
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            video_right()

capture1 = cv2.VideoCapture(1)
capture2 = cv2.VideoCapture(2)

def video_left():
    global capture1
    while(True): 
        ret1,frame1 = capture1.read() # read方法返回一个表示视频是否正确读取的布尔值和一帧图像
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY) # 这里用cvtColor（cvt就是convert的缩写）方法进行色彩空间的转换，这里是从BGR空间转换到灰度空间
        cv2.imshow('frame1', gray1) # 通过imshow显示一帧图像
        if cv2.waitKey(1) & 0xFF == ord('q'): # 一帧显示一毫秒，通过上面的while循环不断地显示下一帧，从而形成动态的视频；按q键退出循环，关闭视频。
            break

    capture1.release()
    cv2.destroyAllWindows()

def video_right():
    global capture2
    while(True): # isOpened方法判断视频是否成功打开
        ret2, frame2 = capture2.read()
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame2', gray2)
        
        if cv2.waitKey(1) & 0xFF == ord('q'): # 一帧显示一毫秒，通过上面的while循环不断地显示下一帧，从而形成动态的视频；按q键退出循环，关闭视频。
            break

    capture2.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # from_video_right()
    # thread1 = myThread(1)
    # thread2 = myThread(2)
    # thread3 = myThread(3)
    # thread1.start()
    # thread2.start()

    # while True:
    thread1 = myThread(1)
    thread2 = myThread(2)
    # thread3 = myThread(3)
    thread1.start()
    thread2.start()


