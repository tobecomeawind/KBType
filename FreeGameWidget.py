from LanguageWidget import LanguageChanger
from KeyboardGameWindow import KeyboardGameWindow
from MainWidget import GeneralWindow

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

class FreeGameWindow(GeneralWindow):

    def __init__(self, parent_class=None):

        super().__init__()

        self.parent_class = parent_class

        self.stack_widgets = QStackedWidget()

        self.typeline        = KeyboardGameWindow(self, file='level1.txt')
        self.languageChanger = LanguageChanger(self) 

        self.stack_widgets.addWidget(self.typeline)
        self.stack_widgets.addWidget(self.languageChanger)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.stack_widgets)

        self.setLayout(self.layout)

        self.change_to_languageChanger()

    def change_to_typeline(self):

        self.stack_widgets.setCurrentIndex(0)
        self.typeline.setFocusPolicy(True)

    def change_to_languageChanger(self):

        self.stack_widgets.setCurrentIndex(1)
        self.languageChanger.setFocusPolicy(True)

    def put_language(self, lang):

    	#self.typeline = KeyboardGameWindow(file='RLarge.txt' if lang == 'ru' else 'ELarge.txt')
    	self.typeline = KeyboardGameWindow(file='level1.txt')
    	self.stack_widgets.setCurrentIndex(0)

    def change_to_main(self):

        self.change_to_languageChanger()
