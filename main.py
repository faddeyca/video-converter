import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import uic

from frames_extractor import extract_frames
from video_merger import merge_video
from rotator import rotate_images


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("mainwindow.ui", self)
        self.setup()
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
        self.speedApplyButton.clicked.connect(self.amerge_video)
        self.rotateButton.clicked.connect(self.rotate)

    def rotate(self):
        degrees = float(self.rotateEdit.text())
        if degrees == 0:
            return
        self.mediaPlayer.setMedia(QMediaContent(QUrl("wait.png")))
        self.mediaPlayer.play()
        rotate_images(degrees)
        merge_video(1, self.fileP, self.firstTime)
        self.firstTime = 1
        self.fileP = "output.mp4"
        self.mediaPlayer.setMedia(QMediaContent(QUrl("output.mp4")))
        self.mediaPlayer.play()
        

    def amerge_video(self):
        speed = float(self.speedEdit.text())
        if speed == 1.0:
            return
        self.mediaPlayer.setMedia(QMediaContent(QUrl("wait.png")))
        self.mediaPlayer.play()
        merge_video(speed, self.fileP, self.firstTime)
        self.firstTime = 1
        self.fileP = "output.mp4"
        self.mediaPlayer.setMedia(QMediaContent(QUrl("output.mp4")))
        self.mediaPlayer.play()


    def newVideoAction(self):
        path = QFileDialog.getOpenFileName(self, "Choose video", "*.mp4")
        self.firstTime = 2
        filepath = path[0]
        if filepath == "":
            return
        self.fileP = filepath
        self.mediaPlayer.setMedia(QMediaContent(QUrl("wait.png")))
        self.mediaPlayer.play()
        extract_frames(filepath)
        self.mediaPlayer.setMedia(QMediaContent(QUrl(filepath)))
        self.mediaPlayer.play()
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
    w.show()
    sys.exit(app.exec_())
