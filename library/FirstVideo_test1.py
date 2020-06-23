from imageai.Detection import VideoObjectDetection
import os

# 用fast,参数5训练前15秒时间，训练时间1分55秒

os.environ['KERAS_BACKEND']='tensorflow'

execution_path = os.getcwd()


detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path,"./model_video/resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()#载入模型

custom_objects = detector.CustomObjects(person=True, bicycle=True, motorcycle=True)

detector.loadModel(detection_speed="normal")
video_path = detector.detectCustomObjectsFromVideo(custom_objects=custom_objects, 
    input_file_path=os.path.join(execution_path, "output12.mp4"), 
    output_file_path=os.path.join(execution_path, "output12_2_custom_detected"), 
    frames_per_second=20, log_progress=True)# frame_detection_interval=5,
print(video_path)
