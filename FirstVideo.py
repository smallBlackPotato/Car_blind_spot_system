from imageai.Detection import VideoObjectDetection
import os

os.environ['KERAS_BACKEND']='tensorflow'

execution_path = os.getcwd()
print(execution_path)


detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path,"resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()

custom_objects = detector.CustomObjects(person=True, bicycle=True, motorcycle=True)

video_path = detector.detectCustomObjectsFromVideo(custom_objects=custom_objects, input_file_path=os.path.join(execution_path, "xiaohai.mp4"), output_file_path=os.path.join(execution_path, "xiaohai_custom_detected"), frames_per_second=20, log_progress=True)
print(video_path)
