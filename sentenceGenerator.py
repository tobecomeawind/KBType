from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore 
from random import choice

class Text:

    def _convert_to_lst(self, file, random, max_counter=None):

        result = list()

        max_counter = max_counter if isinstance(max_counter, int) else 3

        with open(file, 'r', encoding='UTF-8') as file:

            lines = file.readlines()

            if random:

                print("---Random words created---")

                counter = 1

                intermediate_result = list()
                
                for _ in range(100):

                    intermediate_result.append(choice(lines).replace('\n', ''))
                    intermediate_result.append(" ")

                    if counter == max_counter:

                        result.append(intermediate_result.copy())

                        intermediate_result.clear()

                        counter = 1
                        continue 

                    counter += 1 

            else:

                print("---Word created---")

                counter = 1
                intermediate_result = list()

                for line in lines:

                    for word in line.split(' '):

                        word = word.replace('\n', '')

                        if word != '\n':

                            intermediate_result.append(word)
                            intermediate_result.append(" ")

                            if counter == max_counter:

                                result.append(intermediate_result.copy())
                                intermediate_result.clear()
                                counter = 1
                                continue

                            counter += 1

        file.close()

        count_letters = sum([sum([len(word) for word in line])for line in result])

        return result, count_letters


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

    color                 = PropertyCSS()
    font                  = PropertyCSS()
    font_size             = PropertyCSS()
    font_family           = PropertyCSS()
    text_decoration       = PropertyCSS()

    def __init__(self, data: str, parent):

        self.data = data

        self.next = None
        self.prev = None

        self.parent = parent
        self.correct = False

        self._letter_label = QLabel(self.data)
        
        self.propertiesCSS = dict()

        self.color       = 'white'
        self.font        = 'Ubuntu'
        self.font_size   = '70px'
        self.font_family = 'Andale Mono, monospace'
        self.text_decoration = 'none'

    @property
    def letter_label(self): return self._letter_label

    @letter_label.setter
    def letter_label(self, value): self._letter_label = value

    @letter_label.deleter
    def letter_label(self): pass


class Word:

    def __init__(self, word: str):

        self.next = None
        self.prev = None

        self.head = None
        self.tail = None

        self.data = word

        self.count_errors  = 0
        self.count_letters = len(self.data)

        self.init_word()

    def init_word(self): [self.__link(Letter(str_letter, self)) for str_letter in self.data]

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

    def get_correctness(self):

        cur = self.head
        res = True

        while cur:

            if not cur.correct:

                res = False
                break

            cur = cur.next

        return res

class Sentence:

    def __init__(self, lst_sentence: list):

        self.next = None

        self.head = None
        self.tail = None

        self.lst_sentence = list(lst_sentence)

        self.count_letters = sum([len(elem) for elem in self.lst_sentence])

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

    def __init__(self):

        self.head = None

        self.len_letters = 0

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

    def load(self, file, random, max_counter):

        if file:

            self.text, count_letters = super()._convert_to_lst(file, random, max_counter)

            self.init_sentences()

            return file, count_letters

        return None, None