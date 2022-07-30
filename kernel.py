import os
import cv2
from pydub import AudioSegment
import moviepy.editor as mpe
from pathlib import Path
from moviepy.editor import *


def process_video(speed=1,
                  funcIndex=None, funcFrame=None, funcBegin=None,
                  hw=None):
    '''
    Извлекает кадры из текущего видео, делает с ними какие-то действия и записывает новое видео.

            Параметры:
                    speed: Скорость нового видео. По умолчанию 1 - скорость не изменяется.

                    funcIndex: Функция. Выполняется на каждой итерации.
                               Принимает на вход индекс текущего кадра. 
                               Возвращает булевое значение, означающее нужно ли вписывать текущий кадр в новое видео.
                               Если пустая, то в новое видео переносятся все кадры.

                    funcFrame: Функция. Выполняется на каждой итерации.
                               Принимает на вход индекс текущего кадра и текущий кадр. 
                               Возвращает изменённый кадр.
                               Если пустая, то сами кадры никак не изменяются.

                    funcBegin: Функция. Выполняется один раз, до начала извлечения кадров.
                               Принимает на вход первый кадр.
                               Делает какие-то действия (подготовка к основным итерациям).
                               Если пустая, но в начале ничего не происходит.

                    hw: Расширение нового видео.
                        Если пустая, то новое видео имеет такое же расширение как и текущее.

            Возвращает:
                    Количество кадров в новом видео. 
                    Иногда используется, так как при сложных манипуляциях трудно посчитать количество кадров в новом видео.
    '''

    #  Извлечение аудио из текущего видео
    AudioFileClip("current.mp4").write_audiofile(str(Path("temp/audio.wav")))

    #  Текущее видео
    current_video = cv2.VideoCapture("current.mp4")

    #  Успешное ли извлечение и первый кадр
    ok, frame = current_video.read()
    
    #  Значения расширения текущего видео
    height, width = frame.shape[0], frame.shape[1]
    #  Количество кадров в секунду
    frames_per_sec = current_video.get(cv2.CAP_PROP_FPS)

    #  Перезапись значений расширения нового видео
    if hw is not None:
        height, width = hw

    new_video = cv2.VideoWriter(
        str(Path("temp/temp.mp4")), cv2.VideoWriter_fourcc(*"mp4v"),
        frames_per_sec * speed, (width, height))

    if funcBegin is not None:
        funcBegin(frame)

    index = 0
    count = 0
    while ok:
        if funcIndex is None or (funcIndex is not None and funcIndex(index)):
            if funcFrame is not None:
                newFrame = funcFrame(index, frame)
                new_video.write(newFrame)
            else:
                new_video.write(frame)
            count += 1
        index += 1
        ok, frame = current_video.read()

    new_video.release()

    new_audio = change_audio_speed(speed)
    new_audio.export(str(Path("temp/audio.wav")), format="wav")

    combine_audio(frames_per_sec)

    os.remove(str(Path("temp/temp.mp4")))

    return count


def change_audio_speed(speed):
    '''
    Изменяет скорость аудио

            Параметры:
                    speed: Новая скорость

            Возвращает:
                    Изменённое аудио
    '''
    sound = AudioSegment.from_mp3(str(Path("temp/audio.wav")))
    audio = sound._spawn(sound.raw_data,
                         overrides={"frame_rate": int(sound.frame_rate*speed)})
    return audio.set_frame_rate(sound.frame_rate)


def combine_audio(fps):
    '''
    Объединяет аудио и видео

            Параметры:
                    fps: Количество кадров в секунду в видео
    '''
    my_clip = mpe.VideoFileClip(str(Path("temp/temp.mp4")))
    audio_background = mpe.AudioFileClip(str(Path("temp/audio.wav")))
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile("current.mp4", fps=fps)
    my_clip.close()
