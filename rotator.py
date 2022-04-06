from PIL import Image
import os
 
def rotate_images(degrees):
    ln = len(os.listdir("temp"))
    currdir = os.getcwd()
    for count in range(ln):
        filename = currdir + r"\temp" + "\\" + str(count) + ".png"
        im = Image.open(filename)
        im_rotate = im.rotate(degrees, expand = True)
        im_rotate.save(filename)
        im.close()
