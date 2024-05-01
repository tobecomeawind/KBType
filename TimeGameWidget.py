from LanguageWidget import LanguageChanger
from KeyboardGameWindow import KeyboardGameWindow
from MainWidget import GeneralWindow
from TimeChangerWidget import TimeChanger

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

class TimeGameWindow(GeneralWindow):

    def __init__(self, parent_class=None):

        super().__init__()

        self.parent_class = parent_class

        self.stack_widgets = QStackedWidget()

        self.typeline        = KeyboardGameWindow(self)
        self.typeline.typeLine.check_game_with_time(1)

        self.languageChanger = LanguageChanger(self)
        self.timeChanger     = TimeChanger(self) 

        self.stack_widgets.addWidget(self.typeline)
        self.stack_widgets.addWidget(self.languageChanger)
        self.stack_widgets.addWidget(self.timeChanger)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.stack_widgets)

        self.setLayout(self.layout)

        self.change_to_languageChanger()

    def change_to_typeline(self):

        self.stack_widgets.setCurrentIndex(0)

    def change_to_languageChanger(self):

        self.stack_widgets.setCurrentIndex(1)
        self.languageChanger.setFocusPolicy(True)

    def change_to_timeChanger(self):

        self.stack_widgets.setCurrentIndex(2)
        self.timeChanger.setFocusPolicy(True)

    def put_language(self, lang):

        self.lang = lang
        self.change_to_timeChanger()
    
    def put_time(self, numb):

        self.typeline.typeLine.total_time = numb 

        if self.lang == 'eng': self.typeline.load_file(file='levels/eng/ELarge.txt', random=True)
        else:self.typeline.load_file(file='levels/ru/RLarge.txt', random=True)

        self.change_to_typeline()

    def change_to_main(self):

        self.change_to_timeChanger()

    def change_to_parent_class(self):
 
        self.parent_class.change_to_main()
