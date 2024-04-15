import sys

from sentenceGenerator import LinkedSentence

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QWidget, QDesktopWidget, QVBoxLayout, QStackedWidget
from PyQt5 import Qt
from PyQt5.QtCore import QTimer 


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


import time

class GeneralWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle('KBType')

        self.setStyleSheet('background : grey')

        self.__x = 1000
        self.__y = 600

        self.resize(self.__x, self.__y)


class KeyboardGameWindow(GeneralWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setStyleSheet('background : grey')

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


    def change_to_plot(self, x, y):

        self.plot.change_data(x, y)
        self.stack_widgets.setCurrentIndex(1)
        self.plot.setFocusPolicy(True)
        print('changed to plot')


class PlotWindow(GeneralWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setStyleSheet('background : yellow')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.x = [0]
        self.y = [0]

        self.figure = Figure()
        self.ax     = self.figure.add_subplot()
        self.ax.plot(self.x, self.y) 

        self.canvas = FigureCanvasQTAgg(self.figure)

        self.layout.addWidget(self.canvas)

    def change_data(self, x, y):

        self.ax.clear()
        self.ax.plot(x, y)

        self.canvas.draw()

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Space:

            window.change_to_type_line()


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

        self.start_layout()

    def keyPressEvent(self, event):

        print(self.current_time, f"WPM: {self.wpm}")
        print(self.correctly_words)

        match event.key():

            case QtCore.Qt.Key_Backspace:

                key = 'backspace'

            case QtCore.Qt.Key_Space:

                key = 'space'

                if not self.game_status:

                    self.start_typing()

                    return

            case _:

                key = event.text()

        self.current_event_key = key

        if self.game_status: 

            self.check_key(key)

    def check_key(self, key):

        # print(key, self.current_letter.data)

        print(f"{self.current_word.data} errors: " + str(self.current_word.count_errors))
        
        match key:

            case self.current_letter.data:

                if not self.current_letter.next:

                    if not self.current_word.next: self.__change_sentence(True)

                    else: self.__change_word(True, True)

                else: self.__change_letter(True, True)

            case 'backspace':

                if not self.current_letter.prev: self.__change_word(False, False)

                else: self.__change_letter(False, True)

            case _:

                if not self.current_letter.next:

                    if not self.current_word.next: self.__change_sentence(True)

                    else: self.__change_word(True, False)

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
            window.change_to_plot(self.time_x, self.wpm_y)
            print(self.isVisible())

    def __change_word(self, forward, correctness):

        if forward:

            self.current_word = self.current_word.next

            self.correctly_words += 1 

            self.current_letter.color = 'green' if correctness else 'black'
            self.current_letter = self.current_word.head

            return

        if self.current_word.prev:

            self.current_word   = self.current_word.prev
            self.current_letter = self.current_word.tail
            self.current_letter.color = 'pink'

    def __change_letter(self, forward, correctness):

        if not correctness:

            self.current_word.count_errors += 1

        if forward:

            self.current_letter.color = 'green' if correctness else 'black'
            self.current_letter = self.current_letter.next

            return

        if self.current_letter.prev:

            self.current_letter = self.current_letter.prev
            self.current_letter.color = 'pink'

    def start_typing(self):

        self.game_status = True
        self.paint_letters()
        self.start_timer()

    def start_layout(self): self.layout.addWidget(QLabel('Press "Space", if u ready'))

    def paint_letters(self):

        self.clearLayout()

        point_word = self.current_word

        while point_word:
        
            point_letter = point_word.head
        
            while point_letter:

                if self.isVisible() == False:

                    break

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

        self.timer.start(1000)

    def get_time(self):

        self.current_time += 1
        self.current_time  = round(self.current_time, 1)
        self.time_x.append(self.current_time)

        self.wpm = round(self.correctly_words * 60 / self.current_time, 1) 
        self.wpm_y.append(self.wpm)

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

        self.game_status = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.get_time)
        self.current_time = 0

        self.wpm_y.clear()
        self.time_x.clear()

        self.start_layout()


app = QApplication([])

window = KeyboardGameWindow()


window.show()

app.exec_()




