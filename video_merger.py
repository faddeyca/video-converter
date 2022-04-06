import os
import cv2
import moviepy.editor as mpe
import wave
from PIL import Image


def merge_video(speed, fileP, firstTime):
    cv2video = cv2.VideoCapture(fileP)
    frames_per_sec = cv2video.get(cv2.CAP_PROP_FPS)

    height, width, framecount = get_new_video_info()

    currdir = os.getcwd()

    new_video = cv2.VideoWriter(
        'pre_output.mp4', cv2.VideoWriter_fourcc(*'mp4v'),
        frames_per_sec * speed, (width, height))

    # Записывает все кадры в новое видео
    for count in range(framecount):
        filename = currdir + r"\temp" + "\\" + str(count) + ".png"
        img = cv2.imread(filename)
        new_video.write(img)

    new_video.release()

    change_audio_speed(speed, firstTime)

    combine_audio(
        "pre_output.mp4", "audio.wav",
        "output.mp4", frames_per_sec * speed)

    os.remove('pre_output.mp4')


# Получает информацию о выходном видео
def get_new_video_info():
    filename = os.getcwd() + r"\temp"
    image = Image.open(filename + "\\0.png")
    height = int(image.height)
    width = int(image.width)
    framecount = len(os.listdir("temp"))
    return height, width, framecount


# Изменяет скорость аудиодорожки
def change_audio_speed(speed, firstTime):
    spf = wave.open('audio.wav', 'rb')
    rate = spf.getframerate()
    signal = spf.readframes(-1)
    spf.close()
    os.remove('audio.wav')
    
    wf = wave.open('audio.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(rate * firstTime * speed)
    wf.writeframes(signal)
    wf.close()


# Слияние аудио и видео
def combine_audio(vidname, audname, outname, fps):
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)
