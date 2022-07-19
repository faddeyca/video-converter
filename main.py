import sys
import os
import cv2
import shutil

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QMainWindow, QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

import history_machine as hm
import actions as a


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("mainwindow.ui", self)
        self.setup()
        self.make_connections()

    #  Настройка
    def setup(self):
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()
        self.slider.setRange(0, 0)
        self.duration = 0
        self.framesAmount = 0
        self.height = 0
        self.width = 0
        self.history_index = 0
        self.history_max = 0

    #  Инициализирует медиаплеер
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
        self.actionUndo.triggered.connect(lambda: hm.undo_history(self))
        self.actionRedo.triggered.connect(lambda: hm.redo_history(self))

        self.playButton.clicked.connect(self.mediaPlayer.play)
        self.pauseButton.clicked.connect(self.mediaPlayer.pause)
        self.stopButton.clicked.connect(self.mediaPlayer.stop)
        self.speedApplyButton.clicked.connect(
            lambda: self.action(a.change_speed))
        self.rotateButton.clicked.connect(
            lambda: self.action(a.rotate))
        self.cutButton.clicked.connect(
            lambda: a.cut(self))
        self.photoChooseButton.clicked.connect(
            lambda: a.load_photo(self))
        self.addPhotoButton.clicked.connect(
            lambda: self.action(a.add_photo))
        self.fragmentChooseButton.clicked.connect(
            lambda: a.load_fragment(self))
        self.putOnLeftButton.clicked.connect(
            lambda: self.action(a.put_fragment_left))
        self.putOnRightButton.clicked.connect(
            lambda: self.action(a.put_fragment))
        self.cropButton.clicked.connect(
            lambda: self.action(a.crop))

        self.slider.sliderMoved.connect(self.setPosition)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

    def error(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def action(self, func):
        self.show_wait()
        func(self)
        hm.add_to_history(self)
        self.play()

    def hw_changed(self):
        vidcap = cv2.VideoCapture("current.mp4")
        self.width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.cropSecondX.setText(str(self.width))
        self.cropSecondY.setText(str(self.height))

    #  Выбрать видео для редактора
    def load_new_video(self):
        self.mediaPlayer.stop()
        path = QFileDialog.getOpenFileName(self, "Choose video", "*.mp4")
        filepath = path[0]
        if filepath == "":
            return
        shutil.copy(filepath, "current.mp4")
        hm.add_to_history(self)
        self.hw_changed()
        self.play()
        self.enable_buttons()

    #  Сохранить текущее видео
    def save(self):
        path = QFileDialog.getSaveFileName(self, "Save Video")
        filepath = path[0]
        if filepath == "":
            return
        shutil.copy(("current.mp4"), filepath + ".mp4")

    #  Воспроизвести текущее видео
    def play(self):
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
        vidcap = cv2.VideoCapture("current.mp4")
        self.framesAmount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = duration
        self.cutRightBorder.setText(str(self.framesAmount))
        self.slider.setRange(0, duration)

    #  Установить позицию в видео
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    #  Показать ожидание
    def show_wait(self):
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl.fromLocalFile("wait.png")))
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
        self.rotateCheckBox.setEnabled(True)
        self.cropButton.setEnabled(True)


def create_temp_dir():
    files = os.listdir()
    if "temp" in files:
        shutil.rmtree("temp")
    os.makedirs("temp")
    if "history" in files:
        shutil.rmtree("history")
    os.makedirs("history")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = MainWindow()
    create_temp_dir()
    w.show()
    sys.exit(app.exec_())
