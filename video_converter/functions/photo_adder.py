import os
from PIL import Image
from pathlib import Path
import shutil


def add_photo(leftB, rightB):
    path = os.getcwd() + (str)(Path("/temp/photo.png"))
    img = Image.open(path)
    height, width = get_info()
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(path)
    for i in range(leftB, rightB):
        os.remove("frames" + (str)(Path("/")) + str(i) + ".png")
    for i in range(leftB, rightB):
        shutil.copy(path, os.getcwd() + (str)(Path("/frames")) + (str)(Path("/")) + str(i)+ ".png")


def get_info():
    image = Image.open(os.getcwd() + (str)(Path("/frames")) + (str)(Path("/0.png")))
    height = int(image.height)
    width = int(image.width)
    return height, width