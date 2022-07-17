import os
import cv2
from pydub import AudioSegment
import moviepy.editor as mpe
from pathlib import Path
from moviepy.editor import *


#  Соединяет кадры в видео с учётом заданной скорости для нового видео
def process_video(speed, funcIndex=None, funcFrame=None, funcBegin=None, hw=None):
    AudioFileClip("current.mp4").write_audiofile((str)(Path("temp/audio.wav")))

    vidcap = cv2.VideoCapture("current.mp4")

    frames_per_sec = vidcap.get(cv2.CAP_PROP_FPS)
    ok, frame = vidcap.read()
    height, width = frame.shape[0], frame.shape[1]

    if hw != None:
        height, width = hw    

    new_video = cv2.VideoWriter(
        (str)(Path("temp/temp.mp4")), cv2.VideoWriter_fourcc(*"mp4v"),
        frames_per_sec * speed, (width, height))

    if funcBegin != None:
        funcBegin(frame)

    index = 0
    count = 0
    while ok:
        if funcIndex == None or (funcIndex != None and funcIndex(index)):
            if funcFrame != None:
                newFrame = funcFrame(index, frame)
                new_video.write(newFrame)
            else:
                new_video.write(frame)
            count += 1
        index += 1
        ok, frame = vidcap.read()

    new_video.release()

    audio = AudioSegment.from_mp3((str)(Path("temp/audio.wav")))
    new_audio = change_audio_speed(audio, speed)
    new_audio.export((str)(Path("temp/audio.wav")), format = "wav")

    combine_audio(
        (str)(Path("temp/temp.mp4")), (str)(Path("temp/audio.wav")),
        "current.mp4", frames_per_sec)

    os.remove((str)(Path("temp/temp.mp4")))

    return count


#  Изменяет скорость аудиодорожки
def change_audio_speed(sound, speed):
    audio = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)})
    return audio.set_frame_rate(sound.frame_rate)


#  Слияние аудио и видео
def combine_audio(input_video, input_audio, output_video, fps):
    my_clip = mpe.VideoFileClip(input_video)
    audio_background = mpe.AudioFileClip(input_audio)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(output_video, fps=fps)
    my_clip.close()
