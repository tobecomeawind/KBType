import sys


from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QWidget, QDesktopWidget, QVBoxLayout, QStackedWidget
from PyQt5 import Qt
from PyQt5.QtCore import QTimer 


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


import time

class Text:

    def _convert_to_lst(self, file):

        result = list()

        with open(file, 'r') as file:

            lines = file.readlines()

            intermediate_res = list()
            
            for i, line in enumerate(lines):

                line = line.replace('\n', '').split()

                [line.insert(i+1, " ") for i in range(0, len(line)+1, 2)]

                result.append(line)

        file.close()

        return result


class PropertyCSS:

    def __set_name__(self, owner, name):

        self.name = name

    def __set__(self, instance, value):

        instance.__dict__[self.name] = value

        instance.propertiesCSS[self.name.replace("_", "-") if "_" in self.name else self.name] = value

        instance.letter_label.setStyleSheet(self.transform_dict_to_css(instance))

    def __get__(self, instance, owner):

        return instance.__dict__[self.name]

    def transform_dict_to_css(self, instance):

        return ' '.join([f'{key}: {value};' for key, value in instance.propertiesCSS.items()]) 

class Letter:

    color     = PropertyCSS()
    font      = PropertyCSS()
    font_size = PropertyCSS()

    def __init__(self, data: str):

        self.data = data

        self.next = None
        self.prev = None

        self.letter_label = QLabel(self.data)
        self.propertiesCSS = dict()


        self.color     = 'pink'
        self.font      = 'Ubuntu'
        self.font_size = '50px'


class Word:

    def __init__(self, word: str):

        self.next = None
        self.prev = None

        self.head = None
        self.tail = None

        self.data = word

        self.count_errors = 0

        self.init_word()

    def init_word(self): [self.__link(Letter(str_letter)) for str_letter in self.data]

    def __link(self, obj: 'class Letter'):

        if not self.head:

            self.head = obj
            self.tail = obj

            return

        current_obj = self.head

        while current_obj:

            last_obj = current_obj
            current_obj = current_obj.next

        last_obj.next = obj
        obj.prev      = last_obj

        self.tail = obj

        return

class Sentence:

    def __init__(self, lst_sentence: list):

        self.next = None

        self.head = None
        self.tail = None

        self.lst_sentence = list(lst_sentence)

        self.init_sentence()

    def init_sentence(self): [self.__link(Word(str_word)) for str_word in self.lst_sentence]

    def __link(self, obj: 'class Word'):

        if not self.head:

            self.head = obj
            self.tail = obj

            return

        current_obj = self.head

        while current_obj:

            last_obj = current_obj
            current_obj = current_obj.next

        last_obj.next = obj
        obj.prev      = last_obj

        self.tail = obj

        return

    @property
    def sentence(self): return "".join(self.lst_sentence)
    

class LinkedSentence(Text):

    def __init__(self, file):

        self.head = None

        self.text = super()._convert_to_lst(file)

        self.init_sentences()

    def init_sentences(self): [self.__link(Sentence(lst_sentence)) for lst_sentence in self.text]

    def __link(self, obj: 'class Sentence'):

        if not self.head:

            self.head = obj

            return

        current_obj = self.head

        while current_obj:

            last_obj = current_obj
            current_obj = current_obj.next

        last_obj.next = obj


class GeneralWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle('KBType')

        self.setStyleSheet('background : grey')

        self.__x = 1000
        self.__y = 600

        self.resize(self.__x, self.__y)

        self.stack_widgets = QStackedWidget()

        self.typeLine = KeyboardGameWindow() #index 0

        self.stack_widgets.addWidget(self.typeLine)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.stack_widgets)

        self.setLayout(self.layout)

        self.change_to_type_line()

    def change_to_type_line(self):

        self.stack_widgets.setCurrentIndex(0)


class KeyboardGameWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.stack_widgets = QStackedWidget()

        self.typeLine = TypeLineWindow() #index 0
        self.plot     = PlotWindow([1,2,3], [1,2,3])

        self.stack_widgets.addWidget(self.typeLine)
        self.stack_widgets.addWidget(self.plot)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.stack_widgets)

        self.setLayout(self.layout)

        self.change_to_type_line()

    def change_to_type_line(self):

        self.stack_widgets.setCurrentIndex(0)
        self.typeLine.setFocusPolicy(True)

    def change_to_plot(self):

        self.stack_widgets.setCurrentIndex(1)
        self.plot.setFocusPolicy(True)
        print('changed to plot')


class PlotWindow(QWidget):

    def __init__(self, x, y, parent=None):

        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.x = x
        self.y = y

        self.figure = Figure()
        self.ax     = self.figure.add_subplot()
        self.ax.plot(self.x, self.y) 

        self.canvas = FigureCanvasQTAgg(self.figure)

        self.layout.addWidget(self.canvas)


class TypeLineWindow(KeyboardGameWindow):

    def __init__(self, parent=None):

        super(KeyboardGameWindow, self).__init__(parent)

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

        print(key, self.current_letter.data)

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
            self.change_to_plot()
            print(self.time_x)
            print(self.wpm_y)

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
                    clearLayout(child.layout())    

    def start_timer(self):

        self.timer.start(1000)

    def get_time(self):

        self.current_time += 1
        self.current_time  = round(self.current_time, 1)
        self.time_x.append(self.current_time)

        self.wpm = round(self.correctly_words * 60 / self.current_time, 1) 
        self.wpm_y.append(self.wpm)

app = QApplication([])
window = GeneralWindow()


window.show()

app.exec_()




