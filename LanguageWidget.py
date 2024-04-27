import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from PyQt5 import QtGui
from PyQt5 import QtCore

from MainWidget import GeneralWindow

class LanguageChanger(GeneralWindow):

    def __init__(self, parent_class=None):
        
        super().__init__()

        self.parent_class = parent_class

        self.stack_widget = QStackedWidget()

        self.layout = QVBoxLayout()

        self.add_buttons()

        self.stack_widget = QStackedWidget()

        self.setLayout(self.layout)

    def add_buttons(self):

        self.eng = QPushButton("English")
        self.eng.setStyleSheet('color:white;font-size: 60px;border-radius: 8px;')
        self.eng.setIcon(QtGui.QIcon('images/eng.png'))
        self.eng.setIconSize(QtCore.QSize(200,200))
        self.eng.clicked.connect(self.press_english)

        self.ru = QPushButton("Russian")
        self.ru.setStyleSheet('color:white;font-size: 60px;border-radius: 8px;')
        self.ru.setIcon(QtGui.QIcon('images/rus.png'))
        self.ru.setIconSize(QtCore.QSize(200,200))
        self.ru.clicked.connect(self.press_russian)
        
        self.layout.addWidget(self.eng)
        self.layout.addWidget(self.ru)

    def press_english(self):

        self.parent_class.put_language('eng')

    def press_russian(self):

        self.parent_class.put_language('ru')

    def keyPressEvent(self, event):

        if event.text() == '1':

            self.press_english()

        if event.text() == '2':

            self.press_russian()

        if event.key() == QtCore.Qt.Key_Escape:

            self.parent_class.change_to_parent_class()

