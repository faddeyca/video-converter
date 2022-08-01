import sys
import os
import cv2
import shutil
from pathlib import Path

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QMainWindow, QMessageBox
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

import history_machine as hm
import actions as a


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, slash):
        QMainWindow.__init__(self)
        uic.loadUi("mainwindow.ui", self)
        self.setup(slash)
        self.make_connections()

    def setup(self, slash):
        '''
        Настраивает редактор
        '''
        self.slash = slash
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()
        self.slider.setRange(0, 0)
        self.duration = 0
        self.framesAmount = 0
        self.height = 0
        self.width = 0
        self.history_index = 0
        self.history_max = 0

    def makeMediaPlayer(self):
        '''
        Инициализирует медиаплеер
        '''
        mediaPlayer = QMediaPlayer(self)
        mediaPlayer.setVideoOutput(self.videoOutput)
        return mediaPlayer

    def makeVideoWidget(self):
        '''
        Инициализирует видеоплеер
        '''
        videoOutput = QVideoWidget(self)
        vbox = QVBoxLayout()
        vbox.addWidget(videoOutput)
        self.videoWidget.setLayout(vbox)
        return videoOutput

    def make_connections(self):
        '''
        Привязывает функции к кнопкам в UI
        '''
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
        '''
        Выводит сообщение об ошибке
        '''
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def action(self, func):
        '''
        Выполняет действие
        '''
        self.show_wait()
        func(self)
        hm.add_to_history(self)
        self.play()

    def hw_changed(self):
        '''
        Меняет переменые, если расширение текущего видео было изменено
        '''
        vidcap = cv2.VideoCapture("current.mp4")
        self.width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.cropSecondX.setText(str(self.width))
        self.cropSecondY.setText(str(self.height))

    def load_new_video(self):
        '''
        Выбрать видео для редактора
        '''
        path = QFileDialog.getOpenFileName(self, "Choose video", "*.mp4")
        filepath = path[0]
        if filepath == "":
            return
        shutil.copy(filepath, "current.mp4")
        hm.add_to_history(self)
        self.show_wait()
        self.hw_changed()
        self.play()
        self.enable_buttons(True)

    def save(self):
        '''
        Сохранить текущее видео
        '''
        path = QFileDialog.getSaveFileName(self, "Save Video")
        filepath = path[0]
        if filepath == "":
            return
        shutil.copy(("current.mp4"), filepath + ".mp4")

    def play(self):
        '''
        Воспроизвести текущее видео
        '''
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl.fromLocalFile("current.mp4")))
        self.mediaPlayer.play()

    def positionChanged(self, position):
        '''
        Действия, когда изменена позиция видео
        '''
        if self.duration == 0:
            return
        curr = int(self.framesAmount*position/self.duration)
        self.currentFrameLabel.setText(str(curr) + " / " + str(self.framesAmount))
        self.slider.setValue(position)

    def durationChanged(self, duration):
        '''
        Действия, когда продолжительность текущего видео изменилась
        '''
        vidcap = cv2.VideoCapture("current.mp4")
        self.framesAmount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = duration
        self.speedRightBorder.setText(str(self.framesAmount))
        self.cutRightBorder.setText(str(self.framesAmount))
        self.slider.setRange(0, duration)

    def setPosition(self, position):
        '''
        Установить позицию в видео
        '''
        self.mediaPlayer.setPosition(position)

    def show_wait(self):
        '''
        Показать ожидание
        '''
        self.mediaPlayer.setMedia(QMediaContent(
            QUrl.fromLocalFile("wait.png")))
        self.mediaPlayer.play()

    def enable_buttons(self, state):
        '''
        Включить/выключить кнопки
        '''
        self.actionSave.setEnabled(state)
        self.playButton.setEnabled(state)
        self.pauseButton.setEnabled(state)
        self.stopButton.setEnabled(state)
        self.speedLeftBorder.setEnabled(state)
        self.speedRightBorder.setEnabled(state)
        self.speedEdit.setEnabled(state)
        self.speedApplyButton.setEnabled(state)
        self.rotateEdit.setEnabled(state)
        self.rotateButton.setEnabled(state)
        self.cutButton.setEnabled(state)
        self.cutLeftBorder.setEnabled(state)
        self.cutRightBorder.setEnabled(state)
        self.photoChooseButton.setEnabled(state)
        self.fragmentChooseButton.setEnabled(state)
        self.rotateCheckBox.setEnabled(state)
        self.cropButton.setEnabled(state)
        self.cropFirstX.setEnabled(state)
        self.cropFirstY.setEnabled(state)
        self.cropSecondX.setEnabled(state)
        self.cropSecondY.setEnabled(state)
        self.actionDelete.setEnabled(state)


def create_temp_dir():
    '''
    Создать временные директории
    '''
    files = os.listdir()
    if "temp" in files:
        shutil.rmtree("temp")
    os.makedirs("temp")
    if "history" in files:
        shutil.rmtree("history")
    os.makedirs("history")

if __name__ == "__main__":
    slash = str(Path("/"))
    app = QtWidgets.QApplication([])
    w = MainWindow(slash)
    create_temp_dir()
    w.show()
    sys.exit(app.exec_())
