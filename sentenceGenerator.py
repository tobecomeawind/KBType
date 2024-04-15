from PyQt5.QtWidgets import QLabel 

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