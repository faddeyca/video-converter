# This Python file uses the following encoding: utf-8
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5 import uic
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from frames_extractor import extract_frames
from video_merger import merge_video
from rotator import rotate_images


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("mainwindow.ui", self)
        self.setup()
        self.isRotated = False
        self.makeConnections()

    def setup(self):
        self.videoOutput = self.makeVideoWidget()
        self.mediaPlayer = self.makeMediaPlayer()

    def makeMediaPlayer(self):
        mediaPlayer = QMediaPlayer(self)
        mediaPlayer.setVideoOutput(self.videoOutput)
        return mediaPlayer

    def makeVideoWidget(self):
        videoOutput = QVideoWidget(self)
        vbox = QVBoxLayout()
        vbox.addWidget(videoOutput)
        self.videoWidget.setLayout(vbox)
        return videoOutput

    def makeConnections(self):
        self.actionNew_video.triggered.connect(self.newVideoAction)
        self.actionClose.triggered.connect(self.close)
        self.playButton.clicked.connect(self.mediaPlayer.play)
        self.pauseButton.clicked.connect(self.mediaPlayer.pause)
        self.stopButton.clicked.connect(self.mediaPlayer.stop)
        self.x2Button.clicked.connect(lambda: self.amerge_video(2))
        self.x05Button.clicked.connect(lambda: self.amerge_video(0.5))
        self.x01Button.clicked.connect(lambda: self.amerge_video(0.1))
        self.x15Button.clicked.connect(lambda: self.amerge_video(15))
        self.rotateButton.clicked.connect(self.rotate)

    def rotate(self):
        self.mediaPlayer.setMedia(QMediaContent(QUrl("wait.png")))
        self.mediaPlayer.play()
        if self.isRotated:
            self.isRotated = False
        else:
            self.isRotated = True
        rotate_images()
        merge_video(1, self.isRotated, self.fileP)
        self.mediaPlayer.setMedia(QMediaContent(QUrl("output.mp4")))
        self.mediaPlayer.play()
        

    def amerge_video(self, speed):
        self.mediaPlayer.setMedia(QMediaContent(QUrl("wait.png")))
        self.mediaPlayer.play()
        merge_video(speed, self.isRotated, self.fileP)
        self.mediaPlayer.setMedia(QMediaContent(QUrl("output.mp4")))
        self.mediaPlayer.play()


    def newVideoAction(self):
        path = QFileDialog.getOpenFileName(self, "Abrir", "/")
        filepath = path[0]
        if filepath == "":
            return
        self.fileP = filepath
        self.mediaPlayer.setMedia(QMediaContent(QUrl("wait.png")))
        self.mediaPlayer.play()
        extract_frames(filepath)
        self.mediaPlayer.setMedia(QMediaContent(QUrl(filepath)))
        self.mediaPlayer.play()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
