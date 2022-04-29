import os
import cv2
from pydub import AudioSegment
import moviepy.editor as mpe
from PIL import Image
from pathlib import Path


#  Соединяет кадры в видео с учётом заданной скорости для нового видео
def merge_video(speed):
    cv2video = cv2.VideoCapture("current.mp4")
    frames_per_sec = cv2video.get(cv2.CAP_PROP_FPS)

    height, width = get_new_video_info()

    new_video = cv2.VideoWriter(
        (str)(Path("temp/temp.mp4")), cv2.VideoWriter_fourcc(*"mp4v"),
        frames_per_sec * speed, (width, height))

    framesAmount = len(os.listdir("frames"))
    currdir = os.getcwd()
    for count in range(framesAmount):
        filename = currdir + (str)(Path("/frames")) + (str)(Path("/")) + str(count) + ".png"
        img = cv2.imread(filename)
        new_video.write(img)

    new_video.release()

    audio = AudioSegment.from_mp3((str)(Path("temp/audio.wav")))
    new_audio = change_audio_speed(audio, speed)
    new_audio.export((str)(Path("temp/audio.wav")), format = "wav")

    combine_audio(
        (str)(Path("temp/temp.mp4")), (str)(Path("temp/audio.wav")),
        "current.mp4", frames_per_sec)

    os.remove((str)(Path("temp/temp.mp4")))


#  Получает информацию о выходном видео
def get_new_video_info():
    filename = os.getcwd() + (str)(Path("/frames"))
    image = Image.open(filename + (str)(Path("/0.png")))
    height = int(image.height)
    width = int(image.width)
    return height, width


#  Изменяет скорость аудиодорожки
def change_audio_speed(sound, speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


#  Слияние аудио и видео
def combine_audio(input_video, input_audio, output_video, fps):
    my_clip = mpe.VideoFileClip(input_video)
    audio_background = mpe.AudioFileClip(input_audio)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(output_video, fps=fps)
    my_clip.close()
