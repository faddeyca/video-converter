from scipy import ndimage


#  Поворачивает все кадры из frames против часовой стрелки на degrees градусов
def rotate_images(index, degrees, frame):
    return ndimage.rotate(frame, degrees, reshape=False)
