from ast import Tuple
import shutil
from PyQt5.QtWidgets import QFileDialog


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
    pass

def write_log(self, fname, args):
    if not self.saving:
        return
    
    self.saver.append((fname, args))