import cv2 as cv
 
n=input("Please input c or o:")
cap = cv.VideoCapture(1)#用VideoCapture()创建一个对象，其参数是摄像机的编号或者是一个视频的文件名
fourcc=cv.VideoWriter_fourcc(*'XVID')#指定视频视频编解码器格式
out=cv.VideoWriter('output.avi',fourcc,20.0,(640,480))#用VideoWriter创建一个对象，其参数有：输出视频的格式、编码格式、帧数（图片数/s,帧数少，视频不流畅，反之流畅，一般在25帧左右）、画面的大小
open=cv.VideoCapture('kongfan.mp4')
 
if n=='c':
    while (True):
        ret,frame=cap.read()#返回一个布尔值和一个图像矩阵
        gray = cv.cvtColor(frame, 0)
        flip=cv.flip(gray,1)#一个标志，指定如何翻转数组; 0表示绕x轴翻转，正值（例如1）表示绕y轴翻转。负值（例如，-1）表示在两个轴周围翻转
        out.write(frame)
        cv.imshow("frame", flip)
        k = cv.waitKey(1)
        if k == ord('q'):
            break
 
 
elif n=='o':
    while(open.isOpened()):
        ret,frame=open.read()
        gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        cv.imshow("Playing Video",frame)
        if cv.waitKey(25)==ord("q"):
            break
else:
    print("Please input right order")
 
#完成后，要释放摄像机（或文件）
cap.release()
open.release()
cv.destroyAllWindows()
