import os
import shutil
import cv2

from PyQt5.QtWidgets import QFileDialog

from kernel import process_video
import functions as f
from moviepy.editor import VideoFileClip, concatenate_videoclips

import history_machine as hm
import actionSaver as acs


def change_speed(self, speed=None, flag=True, leftB=None, rightB=None):
    '''
    Изменяет скорость видео
    '''
    if flag:
        if leftB is None:
            if self.iswindowed:
                leftB = int(self.speedLeftBorder.text())
        if leftB < 0:
            self.error("Speed photo left border must be >= 0")
            if self.iswindowed:
                self.speedLeftBorder.setText("0")
                self.speedRightBorder.setText(str(self.framesAmount))
            return

        if rightB is None:
            if self.iswindowed:
                rightB = int(self.speedRightBorder.text())
        if rightB > self.framesAmount:
            t1 = "Speed right border must be <= than "
            t2 = f"frames amount ({self.framesAmount})"
            self.error(t1 + t2)
            if self.iswindowed:
                self.speedLeftBorder.setText("0")
                self.speedRightBorder.setText(str(self.framesAmount))
            return

        if speed is None:
            if self.iswindowed:
                speed = float(self.speedEdit.text())
            self.speedEdit.setText("1")
            if speed == 1.0:
                return
            if speed <= 0:
                self.error("Speed value must be > 0")
                return

    if not flag or (leftB == 0 and rightB == self.framesAmount):
        self.show_wait()
        self.framesAmount = process_video(speed=speed)
        acs.write_log(self, "speed", speed)
    else:
        self.saved_flag = True
        self.duration_saved = self.duration
        self.framesAmount_saved = self.framesAmount
        self.show_wait()
        framesAmount = self.framesAmount

        shutil.copy("current.mp4", "temp" + self.slash + "0.mp4")

        cut(self, leftB=leftB, rightB=rightB)
        change_speed(self, speed=speed, flag=False)
        shutil.copy("current.mp4", "temp" + self.slash + "1.mp4")

        if leftB != 0:
            shutil.copy("temp" + self.slash + "0.mp4", "current.mp4")
            cut(self, leftB=0, rightB=leftB-1)
            c1 = VideoFileClip("current.mp4")
            c2 = VideoFileClip("temp" + self.slash + "1.mp4")
            final_clip = concatenate_videoclips([c1, c2])
            final_clip.write_videofile("current1.mp4")
            c1.close()
            c2.close()
            os.remove("current.mp4")
            shutil.copy("current1.mp4", "current.mp4")
            os.remove("current1.mp4")

        if rightB != framesAmount:
            shutil.copy("current.mp4", "temp" + self.slash + "1.mp4")
            shutil.copy("temp" + self.slash + "0.mp4", "current.mp4")
            cut(self, leftB=rightB, rightB=framesAmount)
            c1 = VideoFileClip("current.mp4")
            c2 = VideoFileClip("temp" + self.slash + "1.mp4")
            final_clip = concatenate_videoclips([c2, c1], method="compose")
            final_clip.write_videofile("current1.mp4")
            c1.close()
            c2.close()
            os.remove("current.mp4")
            shutil.copy("current1.mp4", "current.mp4")
            os.remove("current1.mp4")

        self.saved_flag = False

    hm.add_to_history(self)
    self.play()


def rotate(self, degrees=None, reshape=None):
    '''
    Поворачивает видео на заданный угол
    '''
    if degrees is None:
        if self.iswindowed:
            degrees = float(self.rotateEdit.text()) % 360
    if self.iswindowed:
        self.rotateEdit.setText("0")
    if degrees == 0:
        return
    if reshape is None:
        if self.iswindowed:
            reshape = self.rotateCheckBox.isChecked()
    if reshape:
        vidcap = cv2.VideoCapture("current.mp4")
        ok, frame = vidcap.read()
        image = f.rotate_image(frame, degrees, True)
        hw = image.shape[0], image.shape[1]
        process_video(funcFrame=lambda x, y:
                      f.rotate_image(y,
                                     degrees,
                                     True),
                      hw=hw)
        acs.write_log(self, "rotate", (degrees, True))
        self.hw_changed()
    else:
        process_video(funcFrame=lambda x, y:
                      f.rotate_image(y,
                                     degrees,
                                     False))
        acs.write_log(self, "rotate", (degrees, False))


def cut(self, leftB=None, rightB=None):
    '''
    Обрезает видео
    '''
    if not self.saved_flag:
        if leftB is None:
            if self.iswindowed:
                leftB = int(self.cutLeftBorder.text())
        if leftB < 0:
            self.error("Cut left border must be >= 0")
            if self.iswindowed:
                self.cutLeftBorder.setText("0")
                self.cutRightBorder.setText(str(self.framesAmount))
            return
        if rightB is None:
            if self.iswindowed:
                rightB = int(self.cutRightBorder.text())
        if rightB > self.framesAmount:
            t1 = "Cut right border must be <= than "
            t2 = f"frames amount ({self.framesAmount})"
            self.error(t1 + t2)
            if self.iswindowed:
                self.cutLeftBorder.setText("0")
                self.cutRightBorder.setText(str(self.framesAmount))
            return
        if leftB == 0 and rightB == self.framesAmount:
            return
    duration = self.duration
    if self.saved_flag:
        duration = self.duration_saved
    framesAmount = self.framesAmount
    if self.saved_flag:
        framesAmount = self.framesAmount_saved
    self.show_wait()
    if self.iswindowed:
        self.cutLeftBorder.setText("0")
    process_video(funcIndex=lambda x:
                  x >= leftB and x <= rightB,
                  funcBegin=lambda x:
                  f.cutAudio(leftB, rightB, duration, framesAmount))
    hm.add_to_history(self)
    self.play()


def load_photo(self):
    '''
    Загружает статическое изображение для вставки
    '''
    if not self.iswindowed:
        return
    path = QFileDialog.getOpenFileName(self, "Choose photo", "*.png")
    filepath = path[0]
    if filepath == "":
        return
    shutil.copy(filepath, "temp" + self.slash + "photo.png")
    self.photoLabel.setText(filepath)
    self.photoLeftBorder.setEnabled(True)
    self.photoRightBorder.setEnabled(True)
    self.addPhotoButton.setEnabled(True)


def add_photo(self, leftB=None, rightB=None):
    '''
    Вставляет статическое изображение
    '''
    if leftB is None:
        if self.iswindowed:
            leftB = int(self.photoLeftBorder.text())
    if leftB < 0:
        self.error("Add photo left border must be >= 0")
        if self.iswindowed:
            self.photoLeftBorder.setText("0")
            self.photoRightBorder.setText("0")
        return

    if rightB is None:
        if self.iswindowed:
            rightB = int(self.photoRightBorder.text())
    if rightB > self.framesAmount:
        t1 = "Add photo right border must be <= than "
        t2 = f"frames amount ({self.framesAmount})"
        self.error(t1 + t2)
        if self.iswindowed:
            self.photoLeftBorder.setText("0")
            self.photoRightBorder.setText("0")
        return

    process_video(funcFrame=lambda x, y:
                  f.add_photo(leftB, rightB, x, y),
                  funcBegin=lambda x: f.resize_photo(x))


def load_fragment(self, filepath=None):
    '''
    Загружает фрагмент для вставки
    '''
    if not self.iswindowed:
        return
    if filepath is None:
        text = "Choose fragment video"
        path = QFileDialog.getOpenFileName(self, text, "*.mp4")
        filepath = path[0]
        if filepath == "":
            return
    shutil.copy(filepath, "temp" + self.slash + "fragment.mp4")
    self.fragmentLabel.setText(filepath)
    self.putOnLeftButton.setEnabled(True)
    self.putOnRightButton.setEnabled(True)


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
    final_clip.write_videofile("current.mp4")
    clip1.close()
    clip2.close()


def crop(self, cropFirstX=None, cropFirstY=None,
         cropSecondX=None, cropSecondY=None):
    '''
    Обрезает видео по пикселям(кроп)
    '''
    if cropFirstX is None:
        if self.iswindowed:
            cropFirstX = int(self.cropFirstX.text())
    if cropFirstX < 0:
        self.error("Left border value must be >= 0")
        reset_after_crop(self)
        return

    if cropFirstY is None:
        if self.iswindowed:
            cropFirstY = int(self.cropFirstY.text())
    if cropFirstY < 0:
        self.error("Up border value must be >= 0")
        reset_after_crop(self)
        return

    if cropSecondX is None:
        if self.iswindowed:
            cropSecondX = int(self.cropSecondX.text())
    if cropSecondX > self.width:
        self.error(f"Right border value must be <= video width ({self.width})")
        reset_after_crop(self)
        return

    if cropSecondY is None:
        if self.iswindowed:
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
    if not self.iswindowed:
        return
    self.cropFirstX.setText("0")
    self.cropFirstY.setText("0")
    self.cropSecondX.setText(str(self.width))
    self.cropSecondY.setText(str(self.height))
