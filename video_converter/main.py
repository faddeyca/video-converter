import sys
import os
import shutil
from pathlib import Path
from moviepy.editor import VideoFileClip, concatenate_videoclips

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import uic

from functions.frames_extractor import extract_frames, create_temp_dir
from functions.video_merger import merge_video
from functions.rotator import rotate_images
from functions.cutter import cut
from functions.photo_adder import add_photo


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi((str)(Path("video_converter/mainwindow.ui")), self)
        self.setup()
        self.make_connections()

    #  Инициализирует видеоплеер
    def setup(self):
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()
        self.slider.setRange(0, 0)
        self.duration = 0
        self.framesAmount = 0

    #  Инициализирует видеоплеер
    def makeMediaPlayer(self):
        mediaPlayer = QMediaPlayer(self)
        mediaPlayer.setVideoOutput(self.videoOutput)
        return mediaPlayer

    #  Инициализирует видеоплеер
    def makeVideoWidget(self):
        videoOutput = QVideoWidget(self)
        vbox = QVBoxLayout()
        vbox.addWidget(videoOutput)
        self.videoWidget.setLayout(vbox)
        return videoOutput

    #  Привязывает функции к кнопкам в UI
    def make_connections(self):
        self.actionNew_video.triggered.connect(self.load_new_video)
        self.actionSave.triggered.connect(self.save)
        self.playButton.clicked.connect(self.mediaPlayer.play)
        self.pauseButton.clicked.connect(self.mediaPlayer.pause)
        self.stopButton.clicked.connect(self.mediaPlayer.stop)
        self.speedApplyButton.clicked.connect(self.change_speed)
        self.rotateButton.clicked.connect(self.rotate)
        self.cutButton.clicked.connect(self.cut)
        self.photoChooseButton.clicked.connect(self.load_photo)
        self.addPhotoButton.clicked.connect(self.add_photo)
        self.fragmentChooseButton.clicked.connect(self.load_fragment)
        self.putFragmentOnLeftButton.clicked.connect(lambda: self.put_fragment(0))
        self.putFragmentOnRightButton.clicked.connect(lambda: self.put_fragment(1))

        self.slider.sliderMoved.connect(self.setPosition)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
    #переделать
    def put_fragment(self, pos):
        clip1 = VideoFileClip("current.mp4")
        clip2 = VideoFileClip(os.getcwd() + (str)(Path("/temp/fragment.mp4")))
        final_clip = concatenate_videoclips([clip1, clip2])
        final_clip.write_videofile("current.mp4")
        self.play()

    def load_fragment(self):
        path = QFileDialog.getOpenFileName(self, "Choose fragment video", "*.mp4")
        filepath = path[0]
        if filepath == "":
            return
        shutil.copy(filepath, os.getcwd() + (str)(Path("/temp/fragment.mp4")))
        self.fragmentLabel.setText(filepath)
        self.putFragmentOnLeftButton.setEnabled(True)
        self.putFragmentOnRightButton.setEnabled(True)

    def add_photo(self):
        leftB = int(self.photoLeftBorder.text())
        rightB = int(self.photoRightBorder.text())
        add_photo(leftB, rightB)
        merge_video(1, self.firstTime)
        self.play()

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

    #  Выбрать видео для редактора
    def load_new_video(self):
        path = QFileDialog.getOpenFileName(self, "Choose video", "*.mp4")
        self.firstTime = 2
        filepath = path[0]
        if filepath == "":
            return
        shutil.copy(filepath, os.getcwd() + (str)(Path("/current.mp4")))
        self.show_wait()
        extract_frames(filepath)
        self.mediaPlayer.setMedia(QMediaContent(QUrl(filepath)))
        self.mediaPlayer.play()
        self.enable_buttons()

    #  Изменить скорость в заданное количество раз
    def change_speed(self):
        speed = float(self.speedEdit.text())
        self.speedEdit.setText("1")
        if speed == 1.0:
            return
        self.show_wait()
        merge_video(speed, self.firstTime)
        self.play()

    #  Повернуть видео на заданный угол
    def rotate(self):
        degrees = float(self.rotateEdit.text())
        self.rotateEdit.setText("0")
        if degrees == 0:
            return
        self.show_wait()
        rotate_images(degrees)
        merge_video(1, self.firstTime)
        self.play()

    #  Обрезать видео
    def cut(self):
        leftB = int(self.cutLeftBorder.text())
        rightB = int(self.cutRightBorder.text())
        duration = self.duration
        self.cutLeftBorder.setText("0")
        self.show_wait()
        cut(leftB, rightB, duration)
        merge_video(1, self.firstTime)
        self.play()

    #  Сохранить текущее видео
    def save(self):
        path = QFileDialog.getSaveFileName(self, "Save Video")
        filepath = path[0]
        if filepath == "":
            return
        shutil.copy(os.getcwd() + (str)(Path("/current.mp4")), filepath + ".mp4")

    #  Воспроизвести текущее видео
    def play(self):
        self.firstTime = 1
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl.fromLocalFile("current.mp4")))
        self.mediaPlayer.play()

    #  Действия, когда изменена позиция видео
    def positionChanged(self, position):
        if self.duration == 0:
            return
        curr = int(self.framesAmount*position/self.duration)
        self.currentFrameLabel.setText(str(curr))
        self.slider.setValue(position)

    #  Действия, когда продолжительность текущего видео изменилась
    def durationChanged(self, duration):
        self.duration = duration
        self.framesAmount = len(os.listdir("frames"))
        self.cutRightBorder.setText(str(self.framesAmount))
        self.slider.setRange(0, duration)

    #  Установить позицию в видео
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    #  Показать ожидание
    def show_wait(self):
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl.fromLocalFile((str)(Path("video_converter/pictures/wait.png")))))
        self.mediaPlayer.play()

    #  Включить кнопки
    def enable_buttons(self):
        self.actionSave.setEnabled(True)
        self.playButton.setEnabled(True)
        self.pauseButton.setEnabled(True)
        self.stopButton.setEnabled(True)
        self.speedEdit.setEnabled(True)
        self.speedApplyButton.setEnabled(True)
        self.rotateEdit.setEnabled(True)
        self.rotateButton.setEnabled(True)
        self.cutButton.setEnabled(True)
        self.cutLeftBorder.setEnabled(True)
        self.cutRightBorder.setEnabled(True)
        self.photoChooseButton.setEnabled(True)
        self.fragmentChooseButton.setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = MainWindow()
    create_temp_dir()
    w.show()
    sys.exit(app.exec_())
