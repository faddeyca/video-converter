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
    Extracts frames from the current video, performs certain actions on them, and records a new video.

    Parameters:

        speed: Speed of the new video. Default is 1 - speed remains unchanged.

        funcIndex: Function. Executed on each iteration.
        Takes the index of the current frame as input.
        Returns a boolean value indicating whether to include the current frame in the new video.
        If empty, all frames are transferred to the new video.

        funcFrame: Function. Executed on each iteration.
        Takes the index of the current frame and the current frame itself as input.
        Returns the modified frame. If empty, frames remain unchanged.

        funcBegin: Function. Executed once, before the extraction of frames begins.
        Takes the first frame as input. Performs some actions (preparation for the main iterations).
        If empty, nothing happens at the beginning.

        hw: Extension of the new video. If empty, the new video has the same extension as the current one.
    
        Returns:
            The number of frames in the new video. Sometimes used, especially in complex manipulations, to count the frames in the new video.
    '''

    AudioFileClip("current.mp4").write_audiofile(str(Path("temp/audio.wav")))

    current_video = cv2.VideoCapture("current.mp4")

    ok, frame = current_video.read()

    height, width = frame.shape[0], frame.shape[1]
    frames_per_sec = current_video.get(cv2.CAP_PROP_FPS)

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
        if funcIndex is None or funcIndex(index):
            if funcFrame is not None:
                newFrame = funcFrame(index, frame)
                new_video.write(newFrame)
            else:
                new_video.write(frame)
            count += 1
        index += 1
        ok, frame = current_video.read()

    new_video.release()

    if not speed == 1:
        new_audio = change_audio_speed(speed)
        new_audio.export(str(Path("temp/audio.wav")), format="wav")

    combine_audio(frames_per_sec)

    os.remove(str(Path("temp/temp.mp4")))
    os.remove(str(Path("temp/audio.wav")))

    return count


def change_audio_speed(speed):
    sound = AudioSegment.from_mp3(str(Path("temp/audio.wav")))
    audio = sound._spawn(sound.raw_data,
                         overrides={"frame_rate": int(sound.frame_rate*speed)})
    return audio.set_frame_rate(sound.frame_rate)


def combine_audio(fps):
    my_clip = mpe.VideoFileClip(str(Path("temp/temp.mp4")))
    audio_background = mpe.AudioFileClip(str(Path("temp/audio.wav")))
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile("current.mp4", fps=fps)
    my_clip.close()
