import cv2
import os


a = os.listdir()
if "temp" in a:
    os.rmdir("temp")
os.makedirs("temp")
vidcap = cv2.VideoCapture('input.mp4')
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(os.path.join(r"C:\Users\Fadg\source\repos\video_converter\temp", "%d.png" % count), image)
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1