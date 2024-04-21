import sys

from sentenceGenerator import LinkedSentence

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QWidget, QDesktopWidget, QVBoxLayout, QStackedWidget
from PyQt5 import Qt
from PyQt5.QtCore import QTimer 

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import numpy as np
from scipy import interpolate

import time

class GeneralWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle('KBType')

        self.setStyleSheet('background : black')

        # self.__x = 1000
        # self.__y = 600

        # self.resize(self.__x, self.__y)

        #self.resize(self.sizeHint())

        # self.showFullScreen()


class KeyboardGameWindow(GeneralWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setStyleSheet('background : black')

        self.stack_widgets = QStackedWidget()

        self.typeLine = TypeLineWindow() #index 0
        self.plot     = PlotWindow() 

        self.stack_widgets.addWidget(self.typeLine)
        self.stack_widgets.addWidget(self.plot)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.stack_widgets)

        self.setLayout(self.layout)

        self.change_to_type_line()

    def change_to_type_line(self):

        self.stack_widgets.setCurrentIndex(0)
        self.typeLine.setFocusPolicy(True)
        print('changed to typeLine')


    def change_to_plot(self, x, y, acc):

        self.plot.change_data(x, y, acc)
        self.stack_widgets.setCurrentIndex(1)
        self.plot.setFocusPolicy(True)
        print('changed to plot')


class PlotWindow(GeneralWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

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

    def change_data(self, x, y, acc):
        
        print(sum(x)//len(x))

        self.x = np.array(x)
        self.y = np.array(y)

        print(np.median(self.y))

        x_smooth = np.linspace(self.x.min(), self.x.max(), 1000)
        bspline  = interpolate.make_interp_spline(self.x, self.y)
        y_smooth = bspline(x_smooth)

        self.ax.clear()
        self.ax.plot(x_smooth, y_smooth, color='w')

        """Style"""

        self.figure.text(0.01, 0.8, f'WPM: {np.median(self.y)}', fontsize=40, color='white', ha='left', va='center')
        self.figure.text(0.01, 0.7, f'ACCURACY: {acc}%', fontsize=40, color='white', ha='left', va='center')

        self.ax.grid(True, which='both', linestyle='dashed', color='gray', zorder=0.5)
        
        self.figure.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        
        self.ax.set_xlabel('Time \n', fontsize=20)
        self.ax.xaxis.label.set_color('white')
        
        self.ax.set_ylabel('WPM ', fontsize=20)
        self.ax.yaxis.label.set_color('white')

        self.ax.set_title('Results \n', fontsize=20)
        self.ax.title.set_color('white')

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        self.ax.spines['left'].set_color('white')        
        self.ax.spines['bottom'].set_color('white')

        """Style"""

        self.canvas.draw()

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Space:

            window.change_to_type_line()

        elif event.key() ==  QtCore.Qt.Key_Escape:

            window.destroy()
            
            return

class TypeLineWindow(GeneralWindow):

    def __init__(self):

        super().__init__()

        self.sentences = LinkedSentence('level1.txt')

        self.current_sentence  = self.sentences.head
        self.current_word      = self.current_sentence.head
        self.current_letter    = self.current_word.head
        self.current_event_key = None

        self.correctly_words = 0
        
        self.wpm = 0
        self.accuracy = 0

        self.letter_bad  = 0
        self.len_letters = self.sentences.len_letters 

        self.game_status = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.get_time)
        self.current_time = 0

        self.layout = QHBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setSpacing(0)

        self.wpm_y  = list()
        self.time_x = list()

        self.setLayout(self.layout)

    def keyPressEvent(self, event):

        print(f"Time: {self.current_time}", f"WPM: {self.wpm}")
        print(f"Correct words: {self.correctly_words}")
        print(f'Accuracy: {self.accuracy}')
        print(f'Letter bad: {self.letter_bad}')

        match event.key():

            case QtCore.Qt.Key_Backspace:

                key = 'backspace'

            case QtCore.Qt.Key_Space:

                key = 'space'

                if not self.game_status:

                    self.start_typing()

                    return

            case QtCore.Qt.Key_Escape:

                window.destroy()

                return

            case _:

                key = event.text()

        self.current_event_key = key

        if self.game_status: 

            self.check_key(key)

    def check_key(self, key):

        # print(key, self.current_letter.data)

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

                self.letter_bad += 1

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

            print("Игра окончена")
            self.game_status = False 
            self.timer.stop()
            window.change_to_plot(self.time_x, self.wpm_y, self.accuracy)

    def __change_word(self, forward):

        if forward: 
            
            if self.current_word.get_correctness(): self.correctly_words += 1 
            
            self.current_word = self.current_word.next
            self.current_letter = self.current_word.head

            return

        if self.current_word.prev:

            self.current_word   = self.current_word.prev
            self.current_letter = self.current_word.tail
            self.current_letter.color = 'white'

    def __change_letter(self, forward, correctness):

        if forward:

            if correctness: self.current_letter.correct = True
            
            self.current_letter.color = 'grey' if correctness else 'yellow'
            self.current_letter = self.current_letter.next

            return

        if self.current_letter.prev:

            self.current_letter.correct = False
            self.current_letter = self.current_letter.prev
            self.current_letter.color = 'white'

    def start_typing(self):

        self.game_status = True
        self.paint_letters()
        self.start_timer()

    def start_layout(self):

        start_label = QLabel('Press "Space", if u ready')
        start_label.setStyleSheet('color: white')

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
                elif child.layout() is not None:
                    self.clearLayout(child.layout())    

    def start_timer(self):

        self.timer.start(500)

    def get_time(self):

        self.current_time += 0.5
        self.current_time  = round(self.current_time, 1)
        self.time_x.append(self.current_time)

        self.wpm = round(self.correctly_words * 60 / self.current_time, 1) 
        
        if self.wpm >= 0: self.wpm_y.append(self.wpm)

        self.accuracy = 100 - round(((self.letter_bad*100 / self.len_letters)), 1)

    def showEvent(self, event):

        super().showEvent(event)

        self.clearLayout()

        self.sentences = LinkedSentence('level1.txt')

        self.current_sentence  = self.sentences.head
        self.current_word      = self.current_sentence.head
        self.current_letter    = self.current_word.head
        self.current_event_key = None

        self.correctly_words = 0
        self.wpm = 0
        self.accuracy = 0

        self.letter_bad  = 0

        self.game_status = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.get_time)
        self.current_time = 0

        self.wpm_y.clear()
        self.time_x.clear()



        self.start_layout()


app = QApplication([])

# screen_rect = app.desktop().screenGeometry()
# print(screen_rect.width(), screen_rect.height())

window = KeyboardGameWindow()


window.show()

app.exec_()









