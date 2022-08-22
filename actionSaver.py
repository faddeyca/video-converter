import shutil
from PyQt5.QtWidgets import QFileDialog

import actions as act

import history_machine as hm


def start_writting(self):
    self.actionStart_writting.setEnabled(False)
    self.actionStop_writting.setEnabled(True)
    self.actionSave_2.setEnabled(False)
    self.saving = True
    self.saver = list()


def stop_writting(self):
    self.actionStart_writting.setEnabled(True)
    self.actionStop_writting.setEnabled(False)
    self.actionSave_2.setEnabled(True)
    self.saving = False


def save(self):
    with open('actions.txt', 'w') as f:
        for item in self.saver:
            s = ""
            for i in item:
                if type(i) == tuple:
                    for ii in i:
                        s += str(ii) + " "
                else:
                    s += str(i) + " "
            s += '\n'
            f.write(s)
    path = QFileDialog.getSaveFileName(self, "Save Actions")
    filepath = path[0]
    if filepath == "":
        return
    shutil.copy(("actions.txt"), filepath + ".txt")


def load(self):
    path = QFileDialog.getOpenFileName(self, "Choose video", "*.txt")
    filepath = path[0]
    if filepath == "":
        return
    self.show_wait()
    self.saved_flag = True
    self.loaded_flag = True
    shutil.copy(filepath, "actions.txt")
    with open("actions.txt", "r") as f:
        for line in f.readlines():
            now = line.split()
            if now[0] == "speed":
                act.change_speed(self, float(now[1]), False)
            if now[0] == "rotate":
                a = False
                if now[2] == "True":
                    a = True
                act.rotate(self, float(now[1]), a)
    self.saved_flag = False
    self.loaded_flag = False
    hm.add_to_history(self)
    self.play()


def write_log(self, fname, args):
    if not self.saving:
        return
    self.saver.append((fname, args))
