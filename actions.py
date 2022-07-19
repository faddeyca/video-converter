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
    cropFirstX = int(self.cropFirstX.text())
    cropFirstY = int(self.cropFirstY.text())
    cropSecondX = int(self.cropSecondX.text())
    cropSecondY = int(self.cropSecondY.text())
    process_video(1,
                  funcFrame=lambda x, y:
                  f.crop(x, y,
                         cropFirstX, cropFirstY, cropSecondX, cropSecondY),
                  hw=(cropSecondY - cropFirstY, cropSecondX - cropFirstY))
    self.hw_changed()


def put_fragment_left(self):
    put_fragment(self, True)


#  Вставить фрагмент
def put_fragment(self, pos=False):
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


#  Загрузить фрагмент
def load_fragment(self):
    path = QFileDialog.getOpenFileName(self, "Choose fragment video", "*.mp4")
    filepath = path[0]
    if filepath == "":
        return
    shutil.copy(filepath, os.getcwd() + (str)(Path("/temp/fragment.mp4")))
    self.fragmentLabel.setText(filepath)
    self.putOnLeftButton.setEnabled(True)
    self.putOnRightButton.setEnabled(True)


#  Вставить фото
def add_photo(self):
    leftB = int(self.photoLeftBorder.text())
    rightB = int(self.photoRightBorder.text())
    process_video(1,
                  funcFrame=lambda x, y:
                  add_photo(leftB, rightB, x, y),
                  funcBegin=lambda x: f.resize_photo(x))


#  Выбрать фото для вставки
def load_photo(self):
    path = QFileDialog.getOpenFileName(self, "Choose photo", "*.png")
    filepath = path[0]
    if filepath == "":
        return
    shutil.copy(filepath, os.getcwd() + (str)(Path("/temp/photo.png")))
    self.photoLabel.setText(filepath)
    self.photoLeftBorder.setEnabled(True)
    self.photoRightBorder.setEnabled(True)
    self.addPhotoButton.setEnabled(True)


#  Изменить скорость в заданное количество раз
def change_speed(self):
    speed = float(self.speedEdit.text())
    self.speedEdit.setText("1")
    if speed == 1.0:
        return
    if speed <= 0:
        self.error("Speed value must be greater than 0")
        return
    self.framesAmount = process_video(speed)


#  Повернуть видео на заданный угол
def rotate(self):
    degrees = float(self.rotateEdit.text()) % 360
    self.rotateEdit.setText("0")
    if degrees == 0:
        return
    if self.rotateCheckBox.isChecked():
        vidcap = cv2.VideoCapture("current.mp4")
        ok, frame = vidcap.read()
        image = f.rotate_image(0, frame, degrees, True)
        hw = image.shape[0], image.shape[1]
        process_video(1,
                    funcFrame=lambda x, y:
                    f.rotate_image(x, y,
                                    degrees,
                                    True),
                    hw=hw)
    else:
        process_video(1,
                    funcFrame=lambda x, y:
                    f.rotate_image(x, y,
                                    degrees,
                                    False))


#  Обрезать видео
def cut(self):
    leftB = int(self.cutLeftBorder.text())
    rightB = int(self.cutRightBorder.text())
    duration = self.duration
    framesAmount = self.framesAmount
    self.show_wait()
    self.cutLeftBorder.setText("0")
    process_video(1,
                  funcIndex=lambda x:
                  f.add(leftB, rightB, x),
                  funcBegin=lambda x:
                  f.cutAudio(leftB, rightB, duration, framesAmount))
    hm.add_to_history(self)
    self.play()
