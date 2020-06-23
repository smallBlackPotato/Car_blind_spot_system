# Car_blind_spot_system——基于动态追踪的汽车盲点活体监测系统

注：

- 本代码python版本为3.6.8
- 本代码包含基本的动态追踪、模型训练、图像处理、以及红外热成像传感器AMG8833的成像处理
- 如有个别变量报错，请查看是否是python版本或第三方库版本问题
- 本项目自带有录制好的测试视频，以及模型源文件和训练视频及结果
## 动态追踪部分

为了方便进行测试，我在show_test.py文件针对摄像头部分做了两种选择，一种是直接用摄像头进行测试，另一种是直接读取本地录制好的视频文件进行测试，代码如下：

~~~Python
#左盲点
camera=cv2.VideoCapture(1)#摄像头
camera = cv2.VideoCapture('output7.mp4')#直接读取本地文件

#右盲点
camera=cv2.VideoCapture(2)
camera = cv2.VideoCapture('output9.mp4')
~~~
本系统共有两个摄像头，分别模拟汽车左右两个摄像头，当使用摄像头时，只需要将读取本地文件的代码注释掉就可以，反之将将摄像头部分注释。

如果只使用视频捕捉部分，只需要将热成像部分代码注释掉即可，该部分代码在show_test.py文件中的`readSerial()`函数中，将该函数有关部分注释即可运行。

## 模型训练部分

在FirstVideo_test1.py文件中，是模型训练代码
```Python
input_file_path=os.path.join(execution_path, "output12.mp4"), 
output_file_path=os.path.join(execution_path, "output12_2_custom_detected"), 
```
这两行代码分别为读取文件和输出文件，具体使用方法可以参考imageAI官方使用文档
## 其他
AMG8833红外热成像传感器数据处理代码在pixels_test文件夹下，详细使用请查看官方文档；项目中其他文件中包含基本的图像处理测试，测试图片、视频均在该项目中，请自行查看测试。