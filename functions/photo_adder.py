from PIL import Image
from pathlib import Path
import cv2

def resize_photo(frame):
    img = Image.open((str)(Path("temp/photo.png")))
    height, width = frame.shape[0], frame.shape[1]
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save((str)(Path("temp/photo.png")))


def add_photo(leftB, rightB, index, frame):
    if index >= leftB and index <= rightB:
        return cv2.imread((str)(Path("temp/photo.png")))
    return frame