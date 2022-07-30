import os
import shutil
import cv2
from pathlib import Path

from PyQt5.QtWidgets import QFileDialog

from kernel import process_video
import functions as f
from moviepy.editor import VideoFileClip, concatenate_videoclips

import history_machine as hm


def crop(self):
    '''
    Обрезает видео по пикселям(кроп)
    '''
    cropFirstX = int(self.cropFirstX.text())
    cropFirstY = int(self.cropFirstY.text())
    cropSecondX = int(self.cropSecondX.text())
    cropSecondY = int(self.cropSecondY.text())
    process_video(funcFrame=lambda x, y:
                  f.crop(y,
                         cropFirstX, cropFirstY, cropSecondX, cropSecondY),
                  hw=(cropSecondY - cropFirstY, cropSecondX - cropFirstY))
    self.hw_changed()


def put_fragment_left(self):
    '''
    Вставляет фрагмент налево
    '''
    put_fragment(self, True)


def put_fragment(self, pos=False):
    '''
    Вставляет фрагмент налево или направо. По умолчанию направо
    '''
    clip1 = VideoFileClip("current.mp4")
    clip2 = VideoFileClip((str)(Path("temp/fragment.mp4")))
    if not pos:
        final_clip = concatenate_videoclips([clip1, clip2], method="compose")
    else:
        final_clip = concatenate_videoclips([clip2, clip1], method="compose")
    final_clip.write_videofile("current1.mp4")
    clip1.close()
    clip2.close()
    os.remove("current.mp4")
    shutil.copy("current1.mp4", "current.mp4")
    os.remove("current1.mp4")


def load_fragment(self):
    '''
    Загружает фрагмент для вставки
    '''
    path = QFileDialog.getOpenFileName(self, "Choose fragment video", "*.mp4")
    filepath = path[0]
    if filepath == "":
        return
    shutil.copy(filepath, os.getcwd() + str(Path("/temp/fragment.mp4")))
    self.fragmentLabel.setText(filepath)
    self.putOnLeftButton.setEnabled(True)
    self.putOnRightButton.setEnabled(True)


def add_photo(self):
    '''
    Вставляет статическое изображение
    '''
    leftB = int(self.photoLeftBorder.text())
    rightB = int(self.photoRightBorder.text())
    process_video(funcFrame=lambda x, y:
                  f.add_photo(leftB, rightB, x, y),
                  funcBegin=lambda x: f.resize_photo(x))


def load_photo(self):
    '''
    Загружает статическое изображение для вставки
    '''
    path = QFileDialog.getOpenFileName(self, "Choose photo", "*.png")
    filepath = path[0]
    if filepath == "":
        return
    shutil.copy(filepath, os.getcwd() + (str)(Path("/temp/photo.png")))
    self.photoLabel.setText(filepath)
    self.photoLeftBorder.setEnabled(True)
    self.photoRightBorder.setEnabled(True)
    self.addPhotoButton.setEnabled(True)


def change_speed(self):
    '''
    Изменяет скорость видео
    '''
    speed = float(self.speedEdit.text())
    self.speedEdit.setText("1")
    if speed == 1.0:
        return
    if speed <= 0:
        self.error("Speed value must be > 0")
        return
    self.framesAmount = process_video(speed=speed)


def rotate(self):
    '''
    Поворачивает видео на заданный угол
    '''
    degrees = float(self.rotateEdit.text()) % 360
    self.rotateEdit.setText("0")
    if degrees == 0:
        return
    if self.rotateCheckBox.isChecked():
        vidcap = cv2.VideoCapture("current.mp4")
        ok, frame = vidcap.read()
        image = f.rotate_image(frame, degrees, True)
        hw = image.shape[0], image.shape[1]
        process_video(funcFrame=lambda x, y:
                      f.rotate_image(y,
                                     degrees,
                                     True),
                      hw=hw)
        self.hw_changed()
    else:
        process_video(funcFrame=lambda x, y:
                      f.rotate_image(y,
                                     degrees,
                                     False))


def cut(self):
    '''
    Обрезает видео
    '''
    leftB = int(self.cutLeftBorder.text())
    if leftB < 0:
        self.error("Cut left border must be >= 0")
        self.cutLeftBorder.setText("0")
        return
    rightB = int(self.cutRightBorder.text())
    if rightB > self.framesAmount:
        self.error(f"Cut right border must be <= than frames amount ({self.framesAmount})")
        self.cutRightBorder.setText(str(self.framesAmount))
        return
    if leftB == 0 and rightB == self.framesAmount:
        return
    duration = self.duration
    framesAmount = self.framesAmount
    self.cutLeftBorder.setText("0")
    process_video(funcIndex=lambda x:
                  x >= leftB and x <= rightB,
                  funcBegin=lambda x:
                  f.cutAudio(leftB, rightB, duration, framesAmount))
