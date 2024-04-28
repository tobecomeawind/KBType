from LanguageWidget import LanguageChanger
from KeyboardGameWindow import KeyboardGameWindow
from MainWidget import GeneralWindow
from LevelChangerWidget import LevelChangerWindow

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

class LevelGameWindow(GeneralWindow):

    def __init__(self, parent_class=None):

        super().__init__()

        self.parent_class = parent_class

        self.stack_widgets = QStackedWidget()

        self.typeline        = KeyboardGameWindow(self)
        self.languageChanger = LanguageChanger(self)
        self.levelChanger    = LevelChangerWindow(self) 

        self.stack_widgets.addWidget(self.typeline)
        self.stack_widgets.addWidget(self.languageChanger)
        self.stack_widgets.addWidget(self.levelChanger)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.stack_widgets)

        self.setLayout(self.layout)

        self.change_to_languageChanger()

    def change_to_typeline(self):

        self.stack_widgets.setCurrentIndex(0)

    def change_to_languageChanger(self):

        self.stack_widgets.setCurrentIndex(1)
        self.languageChanger.setFocusPolicy(True)

    def change_to_levelChanger(self):

        self.stack_widgets.setCurrentIndex(2)
        self.levelChanger.setFocusPolicy(True)

    def put_level(self, file):

        self.typeline.load_file(f'levels/{self.lang}/{file}.txt', max_counter=4 if '9' not in file else 1) 
        self.change_to_typeline()

    def put_language(self, lang):

        self.lang = lang
        self.levelChanger.connect_buttons(self.lang)
        self.change_to_levelChanger()

    def change_to_main(self):

        self.change_to_levelChanger()

    def change_to_parent_class(self):
 
        self.parent_class.change_to_main()
