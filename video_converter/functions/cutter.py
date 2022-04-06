import os
from pydub import AudioSegment


def cut(leftB, rightB, duration):
    framesAmount = len(os.listdir("frames"))
    for i in range(leftB):
        os.remove("frames\\" + str(i) + ".png")
    for i in range(rightB, framesAmount):
        os.remove("frames\\" + str(i) + ".png")
    for i in range(leftB, rightB):
        os.rename("frames\\" + str(i) + ".png", "frames\\" + str(i - leftB) + ".png")

    leftTime = int(duration * leftB / framesAmount)
    rightTime = int(duration * rightB / framesAmount)
    audio = AudioSegment.from_mp3("temp\\audio.wav")
    new_audio = audio[leftTime:rightTime]
    new_audio.export("temp\\audio.wav", format = "wav")
