import os
import shutil


#  Добавить в историю
def add_to_history(self):
    '''
    Добавляет текущее видео в историю
    '''
    if self.saved_flag:
        return
    if self.iswindowed:
        self.actionRedo.setEnabled(False)
    for i in range(self.history_index + 1, self.history_max - 1):
        os.remove("history"+self.slash+(str)(i) + ".mp4")
    if self.history_index >= 1:
        if self.iswindowed:
            self.actionUndo.setEnabled(True)
    shutil.copy("current.mp4",
                "history"+self.slash+(str)(self.history_index)+".mp4")
    self.history_index += 1
    self.history_max = self.history_index + 1


#  Откатить изменения
def undo_history(self):
    '''
    Заменяет текущее видео на предыдущую версию
    '''
    self.show_wait()
    if self.iswindowed:
        self.actionRedo.setEnabled(True)
    self.history_index -= 1
    if self.history_index == 1:
        if self.iswindowed:
            self.actionUndo.setEnabled(False)
    shutil.copy("history" +
                self.slash + (str)(self.history_index - 1) + ".mp4",
                "current.mp4")
    self.hw_changed()
    self.play()


#  Вернуть изменения обрано
def redo_history(self):
    '''
    Возвращает видео после undo
    '''
    self.show_wait()
    if self.iswindowed:
        self.actionUndo.setEnabled(True)
    self.history_index += 1
    if self.history_index == self.history_max - 1:
        if self.iswindowed:
            self.actionRedo.setEnabled(False)
    shutil.copy("history" +
                self.slash + (str)(self.history_index - 1) + ".mp4",
                "current.mp4")
    self.hw_changed()
    self.play()
