import cv2

capture = cv2.VideoCapture(2)
capture_usb = cv2.VideoCapture(1)
# 打开自带的摄像头
if capture.isOpened():
   if capture_usb.isOpened():
	   # 以下设置显示屏的宽高
	   capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	   capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
	   capture_usb.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
	   capture_usb.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
	 
	   # 持续读取摄像头数据
	   while True:
	      read_code, frame = capture.read()
	      read_code2, frame2 = capture_usb.read()
	      if not read_code or not read_code2:
	         break
	      cv2.imshow("screen_title", frame)
	      cv2.imshow("screen_title_usb", frame2)
	      # 输入 q 键，保存当前画面为图片
	      if cv2.waitKey(1) == ord('q'):
	         # 设置图片分辨率
	         frame = cv2.resize(frame, (1920, 1080))
	         cv2.imwrite('pic.jpg', frame)
	         capture_usb.release()
	         break
   # 释放资源      
   capture.release()
   cv2.destroyWindow("screen_title")    