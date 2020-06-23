import sys
# sys.path.append('./')
# from library.camera import Camera

import threading
import time



exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter,flag):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.flag = flag
    def run(self):
        print ("开始线程：" + self.name)
        if self.flag == 1:
            f_d(self.name, self.counter, 1)
        if self.flag == 2:
            i_c(self.name, self.counter, 5)
        print ("退出线程：" + self.name)

# car = Camera()

def f_d(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        # car.face_detection('getTrainData',0,'./photo/')
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


def i_c(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        # car.image_comparison('./photo/0.jpg','./photo/1.jpg')
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


# 创建新线程
thread1 = myThread(1, "Thread-1", 1,1)
thread2 = myThread(2, "Thread-2", 25,2)

# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print ("退出主线程")