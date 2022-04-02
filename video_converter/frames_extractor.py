import cv2
import os
import shutil
from moviepy.editor import *


def extract_frames():
    audioclip = AudioFileClip("input.mp4")
    audioclip.write_audiofile("audio.mp3")

    currdir = os.getcwd()  # Текущая директория

    create_temp_dir(currdir)

    vidcap = cv2.VideoCapture('input.mp4')
    ok, frame = vidcap.read()  # Удачное ли извлечение кадра и сам кадр
    count = 0
    #  Извлекает и нумерует кадры, пока они не закончатся
    while ok:
        cv2.imwrite(os.path.join(currdir + r"\temp", "%d.png" % count), frame)
        ok, frame = vidcap.read()
        count += 1


# Создает временную папку для кадров, удаляет старую, если она есть
def create_temp_dir(currdir):
    files = os.listdir()
    if "temp" in files:
        shutil.rmtree(currdir + r"\temp")
    os.makedirs("temp")
