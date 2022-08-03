from pathlib import Path
import cv2

import main as mn
import actions as act
import shutil


slash = str(Path("/"))

def compare_videos(path1, path2):
    curv1 = cv2.VideoCapture(path1)
    width1  = curv1.get(3)
    height1 = curv1.get(4)
    fps1 = curv1.get(5)
    fc1 = curv1.get(7)

    curv2 = cv2.VideoCapture(path2)
    width2  = curv2.get(3)
    height2 = curv2.get(4)
    fps2 = curv2.get(5)
    fc2 = curv2.get(7)

    if width1 != width2:
        return False

    if height1 != height2:
        return False

    if fps1 != fps2:
        return False

    if fc1 != fc2:
        return False

    ok1, frame1 = curv1.read()
    ok2, frame2 = curv2.read()

    while ok1 and ok2:
        ok1, frame1 = curv1.read()
        ok2, frame2 = curv2.read()
        if cv2.norm(frame1, frame2):
            return False
    
    return True

#  TestSpeedChange

def test_2x():
    self = mn.MainWindow(False)
    path = "test" + slash + "speed0.mp4"
    shutil.copy(path, "current.mp4")
    act.change_speed(self, 2, flag=False)
    path1 = "test" + slash + "speed1n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res

def test_10x():
    self = mn.MainWindow(False)
    path = "test" + slash + "speed0.mp4"
    shutil.copy(path, "current.mp4")
    act.change_speed(self, 10, flag=False)
    path1 = "test" + slash + "speed2n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res

def test_01x():
    self = mn.MainWindow(False)
    path = "test" + slash + "speed0.mp4"
    shutil.copy(path, "current.mp4")
    act.change_speed(self, 0.1, flag=False)
    path1 = "test" + slash + "speed3n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res

def test_2xb():
    self = mn.MainWindow(False)
    path = "test" + slash + "speed0.mp4"
    shutil.copy(path, "current.mp4")
    self.duration = 2134
    self.framesAmount = 32
    act.change_speed(self, 2, leftB=10, rightB=20)
    path1 = "test" + slash + "speed4n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res

def test_01xb():
    self = mn.MainWindow(False)
    path = "test" + slash + "speed0.mp4"
    shutil.copy(path, "current.mp4")
    self.duration = 2134
    self.framesAmount = 32
    act.change_speed(self, 0.1, leftB=10, rightB=20)
    path1 = "test" + slash + "speed5n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res

#  TestRotate
#  TestCut
#  TestPhotoAdder
#  TestFragmentAdder
#  TestCrop
#  TestActionSaver
#  TestHistoryMachine

if __name__ == "__main__":
    sum = 0
    sum += test_2x()
    sum += test_10x()
    sum += test_01x()
    sum += test_2xb()
    sum += test_01xb()
    print(sum)