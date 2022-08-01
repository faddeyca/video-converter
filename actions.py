import os
import shutil
import cv2

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
    if cropFirstX < 0:
        self.error("Left border value must be >= 0")
        reset_after_crop(self)
        return

    cropFirstY = int(self.cropFirstY.text())
    if cropFirstY < 0:
        self.error("Up border value must be >= 0")
        reset_after_crop(self)
        return

    cropSecondX = int(self.cropSecondX.text())
    if cropSecondX > self.width:
        self.error(f"Right border value must be <= video width ({self.width})")
        reset_after_crop(self)
        return

    cropSecondY = int(self.cropSecondY.text())
    if cropSecondY > self.height:
        t = f"Down border value must be <= video height ({self.height})"
        self.error(t)
        reset_after_crop(self)
        return

    c1 = cropFirstX == 0 and cropFirstY == 0
    c2 = cropSecondX == self.width and cropSecondY == self.height
    if c1 and c2:
        return

    process_video(funcFrame=lambda x, y:
                  f.crop(y,
                         cropFirstX, cropFirstY, cropSecondX, cropSecondY),
                  hw=(cropSecondY - cropFirstY, cropSecondX - cropFirstX))
    self.hw_changed()
    reset_after_crop(self)


def reset_after_crop(self):
    '''
    Восстанавливает значения в окошках по умолчанию после кропа
    '''
    self.cropFirstX.setText("0")
    self.cropFirstY.setText("0")
    self.cropSecondX.setText(str(self.width))
    self.cropSecondY.setText(str(self.height))


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
    clip2 = VideoFileClip("temp" + self.slash + "fragment.mp4")
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
    shutil.copy(filepath, "temp" + self.slash + "fragment.mp4")
    self.fragmentLabel.setText(filepath)
    self.putOnLeftButton.setEnabled(True)
    self.putOnRightButton.setEnabled(True)


def add_photo(self):
    '''
    Вставляет статическое изображение
    '''
    leftB = int(self.photoLeftBorder.text())
    if leftB < 0:
        self.error("Add photo left border must be >= 0")
        self.photoLeftBorder.setText("0")
        self.photoRightBorder.setText("0")
        return

    rightB = int(self.photoRightBorder.text())
    if rightB > self.framesAmount:
        t1 = "Add photo right border must be <= than "
        t2 = f"frames amount ({self.framesAmount})"
        self.error(t1 + t2)
        self.photoLeftBorder.setText("0")
        self.photoRightBorder.setText("0")
        return

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
    shutil.copy(filepath, "temp" + self.slash + "photo.png")
    self.photoLabel.setText(filepath)
    self.photoLeftBorder.setEnabled(True)
    self.photoRightBorder.setEnabled(True)
    self.addPhotoButton.setEnabled(True)


def change_speed(self):
    '''
    Изменяет скорость видео
    '''
    leftB = int(self.speedLeftBorder.text())
    if leftB < 0:
        self.error("Speed photo left border must be >= 0")
        self.speedLeftBorder.setText("0")
        self.speedRightBorder.setText(str(self.framesAmount))
        return

    rightB = int(self.speedRightBorder.text())
    if rightB > self.framesAmount:
        t1 = "Speed right border must be <= than "
        t2 = f"frames amount ({self.framesAmount})"
        self.error(t1 + t2)
        self.speedLeftBorder.setText("0")
        self.speedRightBorder.setText(str(self.framesAmount))
        return

    speed = float(self.speedEdit.text())
    self.speedEdit.setText("1")
    if speed == 1.0:
        return
    if speed <= 0:
        self.error("Speed value must be > 0")
        return
    
    if leftB == 0 and rightB == self.framesAmount:
        self.framesAmount = process_video(speed=speed)
    else:
        shutil.copy("current.mp4", )


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
        self.cutRightBorder.setText(str(self.framesAmount))
        return
    rightB = int(self.cutRightBorder.text())
    if rightB > self.framesAmount:
        t1 = "Cut right border must be <= than "
        t2 = f"frames amount ({self.framesAmount})"
        self.error(t1 + t2)
        self.cutLeftBorder.setText("0")
        self.cutRightBorder.setText(str(self.framesAmount))
        return
    if leftB == 0 and rightB == self.framesAmount:
        return
    duration = self.duration
    framesAmount = self.framesAmount
    self.show_wait()
    self.cutLeftBorder.setText("0")
    process_video(funcIndex=lambda x:
                  x >= leftB and x <= rightB,
                  funcBegin=lambda x:
                  f.cutAudio(leftB, rightB, duration, framesAmount))
    hm.add_to_history(self)
    self.play()
