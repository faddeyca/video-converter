import os
import cv2
import moviepy.editor as mpe


def merge_video():
    cv2video = cv2.VideoCapture("input.mp4")

    height, width, frames_per_sec, framecount = get_video_info(cv2video)

    currdir = os.getcwd()

    new_video = cv2.VideoWriter(
        'output.mp4', cv2.VideoWriter_fourcc(*'mp4v'),
        frames_per_sec, (width, height))

    # Записывает все кадры в новое видео
    for count in range(framecount):
        filename = currdir + r"\temp" + "\\" + str(count) + ".png"
        img = cv2.imread(filename)
        new_video.write(img)

    new_video.release()

    combine_audio("input.mp4", "audio.mp3", "o.mp4", frames_per_sec)


# Извлекает информацию о входном видео
def get_video_info(cv2video):
    height = int(cv2video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cv2video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frames_per_sec = cv2video.get(cv2.CAP_PROP_FPS)
    framecount = int(cv2video.get(cv2.CAP_PROP_FRAME_COUNT))
    return height, width, frames_per_sec, framecount


def combine_audio(vidname, audname, outname, fps):
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)
