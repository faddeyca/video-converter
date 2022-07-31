from pydub import AudioSegment
from pathlib import Path
from PIL import Image
import cv2
from scipy import ndimage


def cutAudio(leftB, rightB, duration, framesAmount):
    '''
    Обрезает текущее аудио из temp

        Параметры:
            leftB: Левая граница в кадрах
            rightB: Правая граница в кадрах
            duration: Продолжительность аудио
            framesAmount: Количество кадров
    '''
    leftTime = int(duration * leftB / framesAmount)
    rightTime = int(duration * rightB / framesAmount)
    audio = AudioSegment.from_mp3((str)(Path("temp/audio.wav")))
    new_audio = audio[leftTime:rightTime]
    new_audio.export((str)(Path("temp/audio.wav")), format="wav")


def resize_photo(frame):
    '''
    Переформатирует вставляемое фото из temp

        Параметры:
            frame: кадр из видео
    '''
    img = Image.open((str)(Path("temp/photo.png")))
    height, width = frame.shape[0], frame.shape[1]
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save((str)(Path("temp/photo.png")))


def add_photo(leftB, rightB, index, frame):
    '''
    Заменяет кадр на статиечское изображение

        Параметры:
            leftB: Левая граница в кадрах
            rightB: Правая граница в кадрах
            index: Индекс кадра
            frame: Кадр
    '''
    if index >= leftB and index <= rightB:
        return cv2.imread((str)(Path("temp/photo.png")))
    return frame


def crop(frame, cropFirstX, cropFirstY, cropSecondX, cropSecondY):
    '''
    Возвращает обрезанный кадр

        Параметры:
            frame: Кадр
            cropFirstX: Левая граница
            cropFirstY: Верхняя граница
            cropSecondX: Правая граница
            cropSecondY: Нижняя граница
    '''
    return frame[cropFirstY:cropSecondY, cropFirstX:cropSecondX]


def rotate_image(frame, degrees, reshape):
    '''
    Поворачивает кадр на degrees градусов против часовой

        Параметры:
            frame: Кадр
            degrees: Градусы
            reshape: Флаг переформатирования
    '''
    return ndimage.rotate(frame, degrees, reshape=reshape)
