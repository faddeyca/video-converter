import os
from pydub import AudioSegment
from pathlib import Path


def cut(leftB, rightB, duration):
    framesAmount = len(os.listdir("frames"))
    for i in range(leftB):
        os.remove("frames" + (str)(Path("/")) + str(i) + ".png")
    for i in range(rightB, framesAmount):
        os.remove("frames" + (str)(Path("/")) + str(i) + ".png")
    for i in range(leftB, rightB):
        os.rename("frames" + (str)(Path("/")) + str(i) + ".png", "frames" + (str)(Path("/")) + str(i - leftB) + ".png")

    leftTime = int(duration * leftB / framesAmount)
    rightTime = int(duration * rightB / framesAmount)
    audio = AudioSegment.from_mp3((str)(Path("temp/audio.wav")))
    new_audio = audio[leftTime:rightTime]
    new_audio.export((str)(Path("temp/audio.wav")), format = "wav")
