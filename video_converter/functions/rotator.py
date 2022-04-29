import os
from PIL import Image
from pathlib import Path


#  Поворачивает все кадры из frames против часовой стрелки на degrees градусов
def rotate_images(degrees):
    ln = len(os.listdir("frames"))
    currdir = os.getcwd()
    for i in range(ln):
        filename = currdir + (str)(Path("/frames")) + (str)(Path("/")) + str(i) + ".png"
        im = Image.open(filename)
        im_rotate = im.rotate(degrees)
        im_rotate.save(filename)
        im.close()
