import sys
import os
import shutil

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import uic

from functions.frames_extractor import extract_frames, create_temp_dir
from functions.video_merger import merge_video
from functions.rotator import rotate_images


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("video_converter\\mainwindow.ui", self)
        self.setup()
        self.make_connections()

    #  Инициализирует видеоплеер
    def setup(self):
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()

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

    #  Выбрать видео для редактора
    def load_new_video(self):
        path = QFileDialog.getOpenFileName(self, "Choose video", "*.mp4")
        self.firstTime = 2
        filepath = path[0]
        if filepath == "":
            return
        shutil.copy(filepath, os.getcwd() + "\\current.mp4")
        self.show_wait()
        extract_frames(filepath)
        self.mediaPlayer.setMedia(QMediaContent(QUrl(filepath)))
        self.mediaPlayer.play()
        self.enable_buttons()
    
    #  Изменить скорость в заданное количество раз
    def change_speed(self):
        speed = float(self.speedEdit.text())
        if speed == 1.0:
            return
        self.show_wait()
        merge_video(speed, self.firstTime)
        self.play()

    #  Повернуть видео на заданный угол
    def rotate(self):
        degrees = float(self.rotateEdit.text())
        if degrees == 0:
            return
        self.show_wait()
        rotate_images(degrees)
        merge_video(1, self.firstTime)
        self.play()

    #  Сохранить текущее видео
    def save(self):
        name = QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name, 'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()

    #  Воспроизвести текущее видео
    def play(self):
        self.firstTime = 1
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl.fromLocalFile("current.mp4")))
        self.mediaPlayer.play()

    #  Показать ожидание
    def show_wait(self):
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl.fromLocalFile('video_converter\\pictures\\wait.png')))
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

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = MainWindow()
    create_temp_dir()
    w.show()
    sys.exit(app.exec_())