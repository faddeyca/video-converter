from pydub import AudioSegment
from pathlib import Path
from PIL import Image
import cv2
from scipy import ndimage


def cutAudio(leftB, rightB, duration, framesAmount):
    '''
    It cuts the current audio from temp.

    Parameters:
        leftB: Left boundary in frames.
        rightB: Right boundary in frames.
        duration: Audio duration.
        framesAmount: Number of frames.
    '''
    leftTime = int(duration * leftB / framesAmount)
    rightTime = int(duration * rightB / framesAmount)
    audio = AudioSegment.from_mp3((str)(Path("temp/audio.wav")))
    new_audio = audio[leftTime:rightTime]
    out = new_audio.export((str)(Path("temp/audio.wav")), format="wav")
    out.close()


def resize_photo(frame):
    '''
    It reformats the inserted photo from temp.

    Parameters:
        frame: Frame from the video.
    '''
    img = Image.open((str)(Path("temp/photo.png")))
    height, width = frame.shape[0], frame.shape[1]
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save((str)(Path("temp/photo.png")))


def add_photo(leftB, rightB, index, frame):
    '''
    It replaces the frame with a static image.

    Parameters:
        leftB: Left boundary in frames.
        rightB: Right boundary in frames.
        index: Frame index.
        frame: Frame.
    '''
    if index >= leftB and index <= rightB:
        return cv2.imread((str)(Path("temp/photo.png")))
    return frame


def crop(frame, cropFirstX, cropFirstY, cropSecondX, cropSecondY):
    '''
    Returns the cropped frame.

    Parameters:
        frame: Frame.
        cropFirstX: Left boundary.
        cropFirstY: Upper boundary.
        cropSecondX: Right boundary.
        cropSecondY: Lower boundary.
    '''
    return frame[cropFirstY:cropSecondY, cropFirstX:cropSecondX]


def rotate_image(frame, degrees, reshape):
    '''
    Rotates the frame counterclockwise by degrees degrees.

    Parameters:
        frame: Frame
        degrees: Degrees
        reshape: Reshape flag
    '''
    return ndimage.rotate(frame, degrees, reshape=reshape)
