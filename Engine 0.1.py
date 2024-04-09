import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QWidget, QDesktopWidget, QVBoxLayout
from PyQt5 import Qt 
import time




words_dict = [["bus", " ", "hello", " ", "terrible", " "], ["tortoise", " ", "umbrella", " "]]

class Text:

    def _convert_to_lst(self, file): #подразумеывктся файл но пока тут список

        return file

class Letter:

    def __init__(self, data: str):

        self.data = data

        self.next = None
        self.prev = None

        self.color     = 'pink'
        self.font      = None
        self.font_size = None

        self.letter_label = QLabel(self.data)
        self.letter_label.setStyleSheet('font-size: 50px')


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


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle('KBType')

        self.setStyleSheet('background : grey')

        self.__x = 1000
        self.__y = 800

        self.resize(self.__x, self.__y)


class Type_Line(MainWindow):

    def __init__(self):

        super().__init__()

        self.sentences = LinkedSentence(words_dict)

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

                    else: self.__change_word(True)

                else: self.__change_letter(True)


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
            self.current_letter = self.current_word.head

            return

        if self.current_word.prev:

            self.current_word = self.current_word.prev
            self.current_letter = self.current_word.tail

    def __change_letter(self, forward, correctness):

        if forward:

            self.current_letter = self.current_letter.next

            return

        if self.current_letter.prev: self.current_letter = self.current_letter.prev

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




