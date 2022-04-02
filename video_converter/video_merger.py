import os
import cv2
import moviepy.editor as mpe
import wave


def merge_video(speed):
    cv2video = cv2.VideoCapture("input.mp4")

    height, width, frames_per_sec, framecount = get_video_info(cv2video)

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

    change_audio_speed(speed)

    combine_audio(
        "pre_output.mp4", "new_audio.wav",
        "output.mp4", frames_per_sec * speed)


# Извлекает информацию о входном видео
def get_video_info(cv2video):
    height = int(cv2video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cv2video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frames_per_sec = cv2video.get(cv2.CAP_PROP_FPS)
    framecount = int(cv2video.get(cv2.CAP_PROP_FRAME_COUNT))
    return height, width, frames_per_sec, framecount


# Изменяет скорость аудиодорожки
def change_audio_speed(speed):
    CHANNELS = 1
    swidth = 2
    Change_RATE = speed

    spf = wave.open('audio.wav', 'rb')
    RATE = spf.getframerate()
    signal = spf.readframes(-1)

    wf = wave.open('new_audio.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE*Change_RATE*2)
    wf.writeframes(signal)
    wf.close()


# Слияние аудио и видео
def combine_audio(vidname, audname, outname, fps):
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)
