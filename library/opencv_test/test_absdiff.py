import numpy as np
import cv2
 
img1 = cv2.imread('./test1.jpg')
img2 = cv2.imread('./test2.jpg')
 
img = cv2.absdiff(img1,img2)
 
 
cv2.imshow("img1",img1)
cv2.imshow("img2",img2)
cv2.imshow("img原图",img)
 
cv2.waitKey(0)
cv2.destroyAllWindows()