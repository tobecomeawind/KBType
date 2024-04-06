
words_dict = [["apple", " ", "banana", " ", "chocolate", " "], ["tortoise", " ", "umbrella", " "]]

class Text:

    def _convert_to_lst(self, file): #подразумеывктся файл но пока тут список

        return file

class Letter:

    def __init__(self, data: str):

        self.data = data

        self.next = None
        self.prev = None


class Word:

    def __init__(self, word: str):

        self.next = None

        self.head = None
        self.tail = None

        self.word = word

        self.init_word()

    def init_word(self): [self.__link(Letter(str_letter)) for str_letter in self.word]

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

        return







