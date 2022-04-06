import os
import cv2
import wave
import moviepy.editor as mpe
from PIL import Image


#  Соединяет кадры в видео с учётом заданной скорости для нового видео
def merge_video(speed, firstTime):
    cv2video = cv2.VideoCapture("current.mp4")
    frames_per_sec = cv2video.get(cv2.CAP_PROP_FPS)

    height, width, framecount = get_new_video_info()

    new_video = cv2.VideoWriter(
        'temp\\temp.mp4', cv2.VideoWriter_fourcc(*'mp4v'),
        frames_per_sec * speed, (width, height))

    currdir = os.getcwd()
    for count in range(framecount):
        filename = currdir + "\\frames\\" + str(count) + ".png"
        img = cv2.imread(filename)
        new_video.write(img)

    new_video.release()

    change_audio_speed(speed, firstTime)

    combine_audio(
        "temp\\temp.mp4", "temp\\audio.wav",
        "current.mp4", frames_per_sec * speed)

    os.remove('temp\\temp.mp4')


#  Получает информацию о выходном видео
def get_new_video_info():
    filename = os.getcwd() + "\\frames"
    image = Image.open(filename + "\\0.png")
    height = int(image.height)
    width = int(image.width)
    framecount = len(os.listdir("frames"))
    return height, width, framecount


#  Изменяет скорость аудиодорожки
def change_audio_speed(speed, isFirstTime):
    spf = wave.open('temp\\audio.wav', 'rb')
    rate = spf.getframerate()
    signal = spf.readframes(-1)
    spf.close()
    os.remove('temp\\audio.wav')
    
    wf = wave.open('temp\\audio.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(rate * isFirstTime * speed)
    wf.writeframes(signal)
    wf.close()


#  Слияние аудио и видео
def combine_audio(input_video, input_audio, output_video, fps):
    my_clip = mpe.VideoFileClip(input_video)
    audio_background = mpe.AudioFileClip(input_audio)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(output_video, fps=fps)
