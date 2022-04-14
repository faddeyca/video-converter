import cv2
import os
import shutil
from moviepy.editor import *
from pathlib import Path


#  Извлекает все кадры и аудио дорожку из видео из path
def extract_frames(path):
    create_temp_dir()
    audioclip = AudioFileClip(path)
    audioclip.write_audiofile((str)(Path("temp/audio.wav")))

    vidcap = cv2.VideoCapture(path)
    ok, frame = vidcap.read()
    count = 0
    currdir = os.getcwd() + (str)(Path("/frames"))
    while ok:
        cv2.imwrite(
            os.path.join(currdir, "%d.png" % count), frame)
        ok, frame = vidcap.read()
        count += 1


#  Создает временные папки
def create_temp_dir():
    files = os.listdir()
    if "frames" in files:
        s = os.getcwd() + (str)(Path("/frames"))
        shutil.rmtree(os.getcwd() + (str)(Path("/frames")))
    os.makedirs("frames")
    if "temp" in files:
        shutil.rmtree(os.getcwd() + (str)(Path("/temp")))
    os.makedirs("temp")
