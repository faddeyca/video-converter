from pathlib import Path
import cv2

import main as mn
import actions as act
import shutil


slash = str(Path("/"))


def compare_videos(path1, path2):
    curv1 = cv2.VideoCapture(path1)
    width1 = curv1.get(3)
    height1 = curv1.get(4)
    fps1 = curv1.get(5)
    fc1 = curv1.get(7)

    curv2 = cv2.VideoCapture(path2)
    width2 = curv2.get(3)
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


def test_speed_2x():
    self = mn.MainWindow(False)
    path = "test" + slash + "speed0.mp4"
    shutil.copy(path, "current.mp4")

    act.change_speed(self, 2, flag=False)

    path1 = "test" + slash + "speed1n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res


def test_speed_10x():
    self = mn.MainWindow(False)
    path = "test" + slash + "speed0.mp4"
    shutil.copy(path, "current.mp4")

    act.change_speed(self, 10, flag=False)

    path1 = "test" + slash + "speed2n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res


def test_speed_01x():
    self = mn.MainWindow(False)
    path = "test" + slash + "speed0.mp4"
    shutil.copy(path, "current.mp4")

    act.change_speed(self, 0.1, flag=False)

    path1 = "test" + slash + "speed3n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res


def test_speed_2xb():
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


def test_speed_01xb():
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


def test_rotate_45degF():
    self = mn.MainWindow(False)
    path = "test" + slash + "rotate0.mp4"
    shutil.copy(path, "current.mp4")

    act.rotate(self, 45, False)

    path1 = "test" + slash + "rotate1n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res


def test_rotate_10000degF():
    self = mn.MainWindow(False)
    path = "test" + slash + "rotate0.mp4"
    shutil.copy(path, "current.mp4")

    act.rotate(self, 10000, False)

    path1 = "test" + slash + "rotate2n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res


def test_rotate_67degT():
    self = mn.MainWindow(False)
    path = "test" + slash + "rotate0.mp4"
    shutil.copy(path, "current.mp4")

    act.rotate(self, 67, True)

    path1 = "test" + slash + "rotate3n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res

#  TestCut


def test_cut_LR():
    self = mn.MainWindow(False)
    path = "test" + slash + "cut0.mp4"
    shutil.copy(path, "current.mp4")

    self.duration = 2134
    self.framesAmount = 32
    act.cut(self, 10, 20)

    path1 = "test" + slash + "cut1n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res


def test_cut_R():
    self = mn.MainWindow(False)
    path = "test" + slash + "cut0.mp4"
    shutil.copy(path, "current.mp4")

    self.duration = 2134
    self.framesAmount = 32
    act.cut(self, 10, 32)

    path1 = "test" + slash + "cut2n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res


def test_cut_L():
    self = mn.MainWindow(False)
    path = "test" + slash + "cut0.mp4"
    shutil.copy(path, "current.mp4")

    self.duration = 2134
    self.framesAmount = 32
    act.cut(self, 0, 10)

    path1 = "test" + slash + "cut3n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res

#  TestPhotoAdder


def test_photo():
    self = mn.MainWindow(False)
    path = "test" + slash + "photo0.mp4"
    shutil.copy(path, "current.mp4")

    self.duration = 2134
    self.framesAmount = 32
    shutil.copy("test" + slash + "photo.jpg", "temp" + slash + "photo.png")
    act.add_photo(self, 10, 20)

    path1 = "test" + slash + "photo1n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res

#  TestFragmentAdder


def test_fragment_notResize():
    self = mn.MainWindow(False)
    path = "test" + slash + "fragment0.mp4"
    shutil.copy(path, "current.mp4")

    path1 = "test" + slash + "fragment1.mp4"
    shutil.copy(path1, "temp" + slash + "fragment.mp4")
    act.put_fragment(self)

    path1 = "test" + slash + "fragment1n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res


def test_fragment_Resize():
    self = mn.MainWindow(False)
    path = "test" + slash + "fragment0.mp4"
    shutil.copy(path, "current.mp4")

    path1 = "test" + slash + "fragment2.mp4"
    shutil.copy(path1, "temp" + slash + "fragment.mp4")
    act.put_fragment(self)

    path1 = "test" + slash + "fragment2n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res

#  TestCrop


def test_crop():
    self = mn.MainWindow(False)
    path = "test" + slash + "crop0.mp4"
    shutil.copy(path, "current.mp4")

    self.height = 240
    self.width = 320
    act.crop(self, 0, 0, 99, 100)

    path1 = "test" + slash + "crop1n.mp4"
    path2 = str("current.mp4")
    res = compare_videos(path1, path2)
    print(res)
    return res


if __name__ == "__main__":
    sum = 0

    sum += test_speed_2x()
    sum += test_speed_10x()
    sum += test_speed_01x()
    sum += test_speed_2xb()
    sum += test_speed_01xb()

    sum += test_rotate_45degF()
    sum += test_rotate_10000degF()
    sum += test_rotate_67degT()

    sum += test_cut_LR()
    sum += test_cut_R()
    sum += test_cut_L()

    sum += test_photo()

    sum += test_fragment_notResize()
    sum += test_fragment_Resize()

    sum += test_crop()

    print(f"{sum} of 15")
