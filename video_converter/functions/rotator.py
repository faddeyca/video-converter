import os
from PIL import Image


#  Поворачивает все кадры из frames против часовой стрелки на degrees градусов
def rotate_images(degrees):
    ln = len(os.listdir("frames"))
    currdir = os.getcwd()
    for i in range(ln):
        filename = currdir + "\\frames\\" + str(i) + ".png"
        im = Image.open(filename)
        im_rotate = im.rotate(degrees, expand=True)
        im_rotate.save(filename)
        im.close()
