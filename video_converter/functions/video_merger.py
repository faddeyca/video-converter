import os
import cv2
import wave
import moviepy.editor as mpe
from PIL import Image
from pathlib import Path


#  Соединяет кадры в видео с учётом заданной скорости для нового видео
def merge_video(speed, firstTime):
    cv2video = cv2.VideoCapture("current.mp4")
    frames_per_sec = cv2video.get(cv2.CAP_PROP_FPS)

    height, width, framecount = get_new_video_info()

    new_video = cv2.VideoWriter(
        (str)(Path("temp/temp.mp4")), cv2.VideoWriter_fourcc(*"mp4v"),
        frames_per_sec * speed, (width, height))

    currdir = os.getcwd()
    for count in range(framecount):
        filename = currdir + (str)(Path("/frames")) + (str)(Path("/")) + str(count) + ".png"
        img = cv2.imread(filename)
        new_video.write(img)

    new_video.release()

    change_audio_speed(speed, firstTime)

    combine_audio(
        (str)(Path("temp/temp.mp4")), (str)(Path("temp/audio.wav")),
        "current.mp4", frames_per_sec * speed)

    os.remove((str)(Path("temp/temp.mp4")))


#  Получает информацию о выходном видео
def get_new_video_info():
    filename = os.getcwd() + (str)(Path("/frames"))
    image = Image.open(filename + (str)(Path("/0.png")))
    height = int(image.height)
    width = int(image.width)
    framecount = len(os.listdir("frames"))
    return height, width, framecount


#  Изменяет скорость аудиодорожки
def change_audio_speed(speed, isFirstTime):
    audio = wave.open((str)(Path("temp/audio.wav")), "rb")
    rate = audio.getframerate()
    signal = audio.readframes(-1)
    audio.close()
    os.remove((str)(Path("temp/audio.wav")))

    new_audio = wave.open((str)(Path("temp/audio.wav")), "wb")
    new_audio.setnchannels(1)
    new_audio.setsampwidth(2)
    new_audio.setframerate(rate * isFirstTime * speed)
    new_audio.writeframes(signal)
    new_audio.close()


#  Слияние аудио и видео
def combine_audio(input_video, input_audio, output_video, fps):
    my_clip = mpe.VideoFileClip(input_video)
    audio_background = mpe.AudioFileClip(input_audio)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(output_video, fps=fps)
