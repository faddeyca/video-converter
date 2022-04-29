import cv2
from pydub import AudioSegment
from pathlib import Path


def add(leftB, rightB, index):
    return index >= leftB and index <= rightB

def cutAudio(leftB, rightB, duration, framesAmount):
    leftTime = int(duration * leftB / framesAmount)
    rightTime = int(duration * rightB / framesAmount)
    audio = AudioSegment.from_mp3((str)(Path("temp/audio.wav")))
    new_audio = audio[leftTime:rightTime]
    new_audio.export((str)(Path("temp/audio.wav")), format = "wav")
