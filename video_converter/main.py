from multiprocessing.connection import wait
import sys
import os
import shutil
from pathlib import Path

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from functions.frames_extractor import extract_frames, create_temp_dir
from functions.video_merger import merge_video
from functions.rotator import rotate_images
from functions.cutter import cut
from functions.photo_adder import add_photo
from functions.fragment_adder import add_fragment_on_right


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi((str)(Path("video_converter/mainwindow.ui")), self)
        self.setup()
        self.make_connections()

    #  Настройка
    def setup(self):
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()
        self.slider.setRange(0, 0)
        self.duration = 0
        self.framesAmount = 0
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
        self.actionUndo.triggered.connect(self.undo_history)
        self.actionRedo.triggered.connect(self.redo_history)

        self.playButton.clicked.connect(self.mediaPlayer.play)
        self.pauseButton.clicked.connect(self.mediaPlayer.pause)
        self.stopButton.clicked.connect(self.mediaPlayer.stop)
        self.speedApplyButton.clicked.connect(self.change_speed)
        self.rotateButton.clicked.connect(self.rotate)
        self.cutButton.clicked.connect(self.cut)
        self.photoChooseButton.clicked.connect(self.load_photo)
        self.addPhotoButton.clicked.connect(self.add_photo)
        self.fragmentChooseButton.clicked.connect(self.load_fragment)

        self.slider.sliderMoved.connect(self.setPosition)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)


    #  Вставить фрагмент
    def put_fragment(self, pos):
        add_fragment_on_right()
        self.add_to_history()
        self.play()

    #  Загрузить фрагмент
    def load_fragment(self):
        path = QFileDialog.getOpenFileName(self, "Choose fragment video", "*.mp4")
        filepath = path[0]
        if filepath == "":
            return
        shutil.copy(filepath, os.getcwd() + (str)(Path("/temp/fragment.mp4")))
        self.fragmentLabel.setText(filepath)
        self.putFragmentOnLeftButton.setEnabled(True)
        self.putFragmentOnRightButton.setEnabled(True)

    #  Вставить фото
    def add_photo(self):
        leftB = int(self.photoLeftBorder.text())
        rightB = int(self.photoRightBorder.text())
        self.show_wait()
        add_photo(leftB, rightB)
        merge_video(1)
        self.add_to_history()
        self.play()

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

    #  Выбрать видео для редактора
    def load_new_video(self):
        path = QFileDialog.getOpenFileName(self, "Choose video", "*.mp4")
        filepath = path[0]
        if filepath == "":
            return
        shutil.copy(filepath, os.getcwd() + (str)(Path("/current.mp4")))
        self.add_to_history()
        self.show_wait()
        extract_frames()
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
        merge_video(speed)
        self.add_to_history()
        extract_frames()
        self.play()

    #  Повернуть видео на заданный угол
    def rotate(self):
        degrees = float(self.rotateEdit.text())
        self.rotateEdit.setText("0")
        if degrees == 0:
            return
        self.show_wait()
        rotate_images(degrees)
        merge_video(1)
        self.add_to_history()
        self.play()

    #  Обрезать видео
    def cut(self):
        leftB = int(self.cutLeftBorder.text())
        rightB = int(self.cutRightBorder.text())
        duration = self.duration
        self.cutLeftBorder.setText("0")
        self.show_wait()
        cut(leftB, rightB, duration)
        merge_video(1)
        self.add_to_history()
        self.play()

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

    #  Добавить в историю
    def add_to_history(self):
        self.actionRedo.setEnabled(False)
        for i in range(self.history_index + 1, self.history_max - 1):
            os.remove("history" + (str)(Path("/")) + (str)(i) + ".mp4")
        if self.history_index >= 1:
            self.actionUndo.setEnabled(True)
        shutil.copy("current.mp4", "history" + (str)(Path("/")) + (str)(self.history_index) + ".mp4")
        self.history_index += 1
        self.history_max = self.history_index + 1
    
    #  Откатить изменения
    def undo_history(self):
        self.show_wait()
        self.actionRedo.setEnabled(True)
        self.history_index -= 1
        if self.history_index == 1:
            self.actionUndo.setEnabled(False)
        shutil.copy("history" + (str)(Path("/")) + (str)(self.history_index - 1) + ".mp4", "current.mp4")
        extract_frames()
        self.play()

    #  Вернуть изменения обрано
    def redo_history(self):
        self.show_wait()
        self.history_index += 1
        if self.history_index == self.history_max - 1:
            self.actionRedo.setEnabled(False)
        shutil.copy("history" + (str)(Path("/")) + (str)(self.history_index - 1) + ".mp4", "current.mp4")
        extract_frames()
        self.play()

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
    files = os.listdir()
    if "history" in files:
        s = os.getcwd() + (str)(Path("/history"))
        shutil.rmtree(os.getcwd() + (str)(Path("/history")))
    os.makedirs("history")
    w.show()
    sys.exit(app.exec_())
