import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QWidget, QDesktopWidget, QVBoxLayout
from PyQt5 import Qt 
import time


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle('KBType')

        self.setStyleSheet('background : grey')

        self.__x = 1000
        self.__y = 500

        self.resize(self.__x, self.__y)

class Text:

    def _convert_to_lst(self, file):

        result = list()

        with open(file, 'r') as file:

            lines = file.readlines()

            intermediate_res = list()
            
            for i, line in enumerate(lines):

                result.append(line.replace('\n', ''))
                result.append(" ")

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

        self.lst_sentence = lst_sentence

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


class Type_Line(MainWindow):

    def __init__(self):

        super().__init__()

        self.sentences = LinkedSentence('level1.txt')

        self.current_sentence = self.sentences.head
        self.current_word     = self.current_sentence.head
        self.current_letter   = self.current_word.head

        self.layout = QHBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setSpacing(0)

        self.setLayout(self.layout)
        
        self.paint_letters()

    def keyPressEvent(self, event):

        key = event.text()

        if event.key() == QtCore.Qt.Key_Backspace:

            key = 'backspace' 

        self.check_key(key)

    def check_key(self, key):

        print(key, self.current_letter.data)
        
        match key:

            case self.current_letter.data:

                if not self.current_letter.next:

                    if not self.current_word.next: self.__change_sentence(True)

                    else: self.__change_word(True, True)

                else: self.__change_letter(True, True)

            case 'backspace':

                if not self.current_letter.prev: self.__change_word(False, False)

                else: self.__change_letter(False, False)

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
            self.destroy()

    def __change_word(self, forward, correctness):

        if forward:

            self.current_word   = self.current_word.next
            self.current_letter.color = 'green' if correctness else 'black'
            self.current_letter = self.current_word.head

            return

        if self.current_word.prev:

            self.current_word = self.current_word.prev
            self.current_letter = self.current_word.tail
            self.current_letter.color = 'pink'

    def __change_letter(self, forward, correctness):

        if forward:

            self.current_letter.color = 'green' if correctness else 'black'
            self.current_letter = self.current_letter.next

            return

        if self.current_letter.prev:

            self.current_letter = self.current_letter.prev
            self.current_letter.color = 'pink'

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




app = QApplication([])
window = Type_Line()


window.show()

sys.exit(app.exec_())




