import sys

from sentenceGenerator import LinkedSentence

from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QWidget, QDesktopWidget, QVBoxLayout, QStackedWidget, QLayout, QSizePolicy
from PyQt5 import Qt
from PyQt5.QtCore import QTimer 

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import numpy as np
from scipy import interpolate

import time

from MainWidget import GeneralWindow


class GeneralWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle('KBType')

        self.setStyleSheet('background : black')


class KeyboardGameWindow(GeneralWindow):

    def __init__(self, parent_class=None, time=None, file=None, random=False):

        super().__init__()

        self.parent_class = parent_class

        self.stack_widgets = QStackedWidget()

        self.typeLine = TypeLineWindow(self, time, file, random)

        self.time = time

        self.plot = PlotWindow(self) 

        self.stack_widgets.addWidget(self.typeLine)
        self.stack_widgets.addWidget(self.plot)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.stack_widgets)

        self.setLayout(self.layout)

        self.change_to_type_line()

    def change_to_type_line(self):

        self.typeLine.check_game_with_time(self.time)
        self.stack_widgets.setCurrentIndex(0)
        self.typeLine.setFocusPolicy(True)
        print('changed to typeLine')

    def change_to_plot(self, typeline):

        self.plot.ax.clear()
        self.plot.change_data(typeline)
        self.stack_widgets.setCurrentIndex(1)
        self.plot.setFocusPolicy(True)
        print('changed to plot')

    def change_to_main(self):

        self.parent_class.change_to_main()

    def load_file(self, file, random=False):

        file, count_letters = self.typeLine.sentences.load(file, random)
        self.typeLine.file        = file
        self.typeLine.random      = random
        self.typeLine.len_letters = count_letters

    def showEvent(self, event):
        
        super().showEvent(event)

        self.change_to_type_line()


class PlotWindow(GeneralWindow):

    def __init__(self, parent_class):

        super().__init__()

        self.parent_class = parent_class

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.x = [0]
        self.y = [0]

        self.figure = Figure()
        self.ax     = self.figure.add_subplot()
        self.ax.plot(self.x, self.y)

        self.figure.subplots_adjust(left=0.3)
        
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.layout.addWidget(self.canvas)

    def change_data(self, typeline):

        self.figure.clf()

        self.ax = self.figure.add_subplot()

        self.x    = np.array(typeline.time_x)
        self.y    = np.array(typeline.wpm_y)
        self.acc  = typeline.accuracy
        self.cor  = typeline.letter_good if typeline.letter_good > 0 else typeline.len_letters - typeline.letter_bad
        self.inc  = typeline.letter_bad
        self.time = typeline.current_time
        self.wpm  = typeline.wpm
        self.raw  = typeline.raw

        x_smooth = np.linspace(self.x.min(), self.x.max(), 1000)
        bspline  = interpolate.make_interp_spline(self.x, self.y)
        y_smooth = bspline(x_smooth)

        self.ax.clear()
        self.ax.plot(x_smooth, y_smooth, color='w')

        """Style"""

        self.figure.text(0.07, 0.85, f'\Results/', fontsize=25, color='white', ha='left', va='center')
        self.figure.text(0.06, 0.8, f'WPM: {self.wpm}', fontsize=25, color='white', ha='left', va='center')
        self.figure.text(0.075, 0.77, f'max: {self.y.max()} | min: {(np.trim_zeros(self.y)).min()}', fontsize=10, color='white', ha='left', va='center')
        self.figure.text(0.023, 0.73, f'ACCURACY: {round(self.acc, 1)}%', fontsize=25, color='white', ha='left', va='center')
        self.figure.text(0.075, 0.7, f'{self.cor} correct | {self.inc} incorrect', fontsize=10, color='white', ha='left', va='center')
        self.figure.text(0.06, 0.65, f'TIME: {self.time}s', fontsize=25, color='white', ha='left', va='center')
        self.figure.text(0.06, 0.6, f'RAW: {self.raw}', fontsize=25, color='white', ha='left', va='center')
        self.figure.text(0.085, 0.57, f'(if all correct)', fontsize=10, color='white', ha='left', va='center')
        self.figure.text(0.01, 0.2, f'Press |Space| to restart...', fontsize=20, color='white', ha='left', va='center')
        self.figure.text(0.01, 0.02, f'<-- |Esc| <--', fontsize=10, color='white', ha='left', va='center')

        self.ax.grid(True, which='both', linestyle='dashed', color='gray', zorder=0.5)
        
        self.figure.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        
        self.ax.set_xlabel('Time \n', fontsize=20)
        self.ax.xaxis.label.set_color('white')
        
        self.ax.set_ylabel('WPM ', fontsize=20)
        self.ax.yaxis.label.set_color('white')

        self.ax.set_title('Plot \n', fontsize=20)
        self.ax.title.set_color('white')

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        self.ax.spines['left'].set_color('white')        
        self.ax.spines['bottom'].set_color('white')

        """Style"""

        self.canvas.draw()

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Space:

            self.parent_class.change_to_type_line()

        elif event.key() ==  QtCore.Qt.Key_Escape:

            self.parent_class.change_to_main()
        
        elif event.key() == QtCore.Qt.Key_Backspace:

            self.parent_class.change_to_main()

            return

class TypeLineWindow(GeneralWindow):

    def __init__(self, parent_class, time=None, file=None, random=False):

        super().__init__()

        print(time)

        self.parent_class = parent_class

        self.sentences = LinkedSentence()
        self.file, self.len_letters = self.sentences.load(file, random)
        self.random = random
        
        if file:

            self.current_sentence  = self.sentences.head
            self.current_word      = self.current_sentence.head
            self.current_letter    = self.current_word.head
            self.current_event_key = None


        self.correctly_words = 0
        self.total_words     = 0
        
        self.wpm = 0
        self.accuracy = 0

        self.letter_good = 0
        self.letter_bad  = 0
        
        self.game_status = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.get_time)
        self.current_time = 0
        self.total_time   = 0

        self.layout = QHBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setSpacing(0)

        self.wpm_y  = list()
        self.time_x = list()

        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(QtCore.Qt.AlignLeft)

        self.center_layout = QVBoxLayout()
        self.center_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        self.game_with_time = False 
        self.game_with_time = self.check_game_with_time(time)

        self.center_layout.addLayout(self.layout)

        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(QtCore.Qt.AlignRight)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.center_layout)
        self.main_layout.addLayout(self.right_layout)

        self.setLayout(self.main_layout)

    def check_game_with_time(self, time):

        if not self.game_with_time:

            if time and isinstance(time, (int, float)):

                self.game_with_time = True
                self.total_time     = time

                self.time_label = QLabel(str(self.current_time))
                self.time_label.setStyleSheet('color: white; font-size: 40px')
                self.time_label.setAlignment(QtCore.Qt.AlignCenter)

                self.center_layout.addWidget(self.time_label)

                return True

        return False


    def keyPressEvent(self, event):

        print(f"Time: {self.current_time}", f"WPM: {self.wpm}")
        print(f"Correct words: {self.correctly_words}")
        print(f'Accuracy: {self.accuracy}')
        print(f'Letter bad: {self.letter_bad}')

        match event.key():

            case QtCore.Qt.Key_Backspace:

                key = 'backspace'

                if not self.game_status: self.parent_class.change_to_main()

            case QtCore.Qt.Key_Space:

                key = ' '

                if not self.game_status:

                    self.start_typing()

                    return

            case QtCore.Qt.Key_Escape:

                self.parent_class.change_to_main()

                return

            case _:

                key = event.text()

        self.current_event_key = key

        if self.game_status: 

            self.check_key(key)

    def check_key(self, key):

        print(f"word: {self.current_letter.parent.data} errors: " + str(self.current_word.count_errors))

        try: print(f'Предыдущая клавиша нажата: {self.current_letter.prev.correct} \n')
        except: pass

        try: print(f'Предыдущее слово написано: {self.current_word.prev.get_correctness()}')
        except: pass

        match key:

            case self.current_letter.data:

                if not self.current_letter.next:

                    if not self.current_word.next: self.__change_sentence(True)

                    else:
                        self.__change_letter(True, True)
                        self.__change_word(True)

                else: self.__change_letter(True, True)

            case 'backspace':

                if not self.current_letter.prev: self.__change_word(False)

                else: self.__change_letter(False, True)

            case _:

                if not self.current_letter.next:

                    if not self.current_word.next: self.__change_sentence(True)

                    else:
                        self.__change_letter(True, False)
                        self.__change_word(True)

                else: self.__change_letter(True, False)

    def __change_sentence(self, forward):

        if forward:

            if self.current_sentence.next:

                self.current_sentence = self.current_sentence.next
                self.current_word     = self.current_sentence.head
                self.current_letter   = self.current_word.head

                self.paint_letters()

                return

            self.stop_game()

    def __change_word(self, forward):

        if forward: 
            
            if self.current_word.get_correctness(): self.correctly_words += 1 
            
            self.current_word = self.current_word.next
            self.current_letter = self.current_word.head

            self.total_words += 1

            return

        if self.current_word.prev:

            self.current_word   = self.current_word.prev
            self.current_letter = self.current_word.tail
            self.current_letter.color = 'white'
            self.current_letter.text_decoration = 'none'

    def __change_letter(self, forward, correctness):

        if forward:

            if correctness:
                self.current_letter.correct = True
                self.letter_good += 1
            else: self.letter_bad += 1
            
            if correctness:self.current_letter.color = 'grey'
            else: self.current_letter.text_decoration = 'line-through'

            self.current_letter = self.current_letter.next

            return

        if self.current_letter.prev:

            self.current_letter.correct = False
            self.current_letter = self.current_letter.prev
            self.current_letter.color = 'white'
            self.current_letter.text_decoration = 'none'

    def start_typing(self):

        self.game_status = True
        self.paint_letters()
        self.start_timer()

    def start_layout(self):

        start_label = QLabel('Press "Space", if u ready')
        start_label.setStyleSheet('color: white; font-size: 40px')

        self.layout.addWidget(start_label)

    def paint_letters(self):

        self.clearLayout()

        point_word = self.current_word

        while point_word:
        
            point_letter = point_word.head
        
            while point_letter:

                self.layout.addWidget(point_letter.letter_label)

                point_letter = point_letter.next

            point_word = point_word.next

    def clearLayout(self):

        if self.layout is not None:
            while self.layout.count():
                child = self.layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()  

    def start_timer(self):

        self.timer.start(100)

    def get_time(self):

        self.current_time += 0.1
        self.current_time  = round(self.current_time, 1)
        self.time_x.append(self.current_time)

        self.wpm = round(self.correctly_words * 60 / self.current_time, 1)
        self.raw = round(self.total_words * 60 / self.current_time, 1) 
        
        if self.wpm >= 0: self.wpm_y.append(self.wpm)


        if self.game_with_time:

            self.time_label.setText(str(self.current_time))

            try:
            
                self.accuracy = 100 - round(((self.letter_bad*100 / self.letter_good)), 1)

            except: 

                pass
            
            self.accuracy = self.accuracy if self.accuracy > 0 else 0 

            if self.current_time == self.total_time: 

                self.time_label.setText(str(self.current_time))

                self.stop_game()

        self.accuracy = 100 - round(((self.letter_bad*100 / self.len_letters)), 1)
    
    def stop_game(self):

        print("Игра окончена")
        self.game_status = False 
        self.timer.stop()
        self.parent_class.change_to_plot(self)

    def showEvent(self, event):

        super().showEvent(event)

        print("---Show Event---")

        self.clearLayout()

        print(self.random)

        self.sentences = LinkedSentence()
        self.file, self.len_letters = self.sentences.load(self.file, self.random)

        self.current_sentence  = self.sentences.head
        self.current_word      = self.current_sentence.head
        self.current_letter    = self.current_word.head
        self.current_event_key = None

        self.correctly_words = 0
        self.total_words = 0
        self.wpm = 0
        self.accuracy = 0
        self.raw = 0

        self.letter_bad  = 0
        self.letter_good = 0

        self.game_status = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.get_time)
        self.current_time = 0

        if self.game_with_time: self.time_label.setText(str(self.current_time))

        self.wpm_y.clear()
        self.time_x.clear()

        self.start_layout()


# app = QApplication([])

# screen_rect = app.desktop().screenGeometry()
# print(screen_rect.width(), screen_rect.height())

# window = KeyboardGameWindow(time=4, file='level1.txt')


# window.show()

# app.exec_()









