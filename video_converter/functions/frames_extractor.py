import cv2
import os
import shutil
from moviepy.editor import *


#  Извлекает все кадры и аудио дорожку из видео из path
def extract_frames(path):
    create_temp_dir()
    audioclip = AudioFileClip(path)
    audioclip.write_audiofile("temp\\audio.wav")

    vidcap = cv2.VideoCapture(path)
    ok, frame = vidcap.read()
    count = 0
    currdir = os.getcwd()
    while ok:
        cv2.imwrite(os.path.join(currdir + "\\frames", "%d.png" % count), frame)
        ok, frame = vidcap.read()
        count += 1

#  Создает временные папки
def create_temp_dir():
    files = os.listdir()
    if "frames" in files:
        shutil.rmtree(os.getcwd() + "\\frames")
    os.makedirs("frames")
    if "temp" in files:
        shutil.rmtree(os.getcwd() + "\\temp")
    os.makedirs("temp")

