from pydub import AudioSegment
from pathlib import Path
from PIL import Image
import cv2
from scipy import ndimage


def crop(index, frame, cropFirstX, cropFirstY, cropSecondX, cropSecondY):
    return frame[cropFirstY:cropSecondY, cropFirstX:cropSecondX]

def add(leftB, rightB, index):
    return index >= leftB and index <= rightB

def cutAudio(leftB, rightB, duration, framesAmount):
    leftTime = int(duration * leftB / framesAmount)
    rightTime = int(duration * rightB / framesAmount)
    audio = AudioSegment.from_mp3((str)(Path("temp/audio.wav")))
    new_audio = audio[leftTime:rightTime]
    new_audio.export((str)(Path("temp/audio.wav")), format = "wav")

def resize_photo(frame):
    img = Image.open((str)(Path("temp/photo.png")))
    height, width = frame.shape[0], frame.shape[1]
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save((str)(Path("temp/photo.png")))


def add_photo(leftB, rightB, index, frame):
    if index >= leftB and index <= rightB:
        return cv2.imread((str)(Path("temp/photo.png")))
    return frame

#  Поворачивает все кадры из frames против часовой стрелки на degrees градусов
def rotate_images(index, frame, degrees, isd):
    return ndimage.rotate(frame, degrees, reshape=isd)