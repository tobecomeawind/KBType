import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QStackedWidget
from PyQt5 import QtGui
from PyQt5 import QtCore

from MainWidget import GeneralWindow

class TimeChanger(GeneralWindow):

    def __init__(self, parent_class=None):
        
        super().__init__()

        self.parent_class = parent_class

        self.stack_widget = QStackedWidget()

        self.layout = QHBoxLayout()

        self.add_buttons()

        self.stack_widget = QStackedWidget()

        self.setLayout(self.layout)

    def add_buttons(self):

        self.fifteen = QPushButton()
        self.fifteen.setStyleSheet('color:white;font-size: 60px;border-radius: 8px;')
        self.fifteen.setIcon(QtGui.QIcon('images/numbers/15.png'))
        self.fifteen.setIconSize(QtCore.QSize(200,200))
        self.fifteen.clicked.connect(lambda: self.press(15))

        self.twenty_five = QPushButton()
        self.twenty_five.setStyleSheet('color:white;font-size: 60px;border-radius: 8px;')
        self.twenty_five.setIcon(QtGui.QIcon('images/numbers/25.png'))
        self.twenty_five.setIconSize(QtCore.QSize(200,200))
        self.twenty_five.clicked.connect(lambda: self.press(25))

        self.fifty = QPushButton()
        self.fifty.setStyleSheet('color:white;font-size: 60px;border-radius: 8px;')
        self.fifty.setIcon(QtGui.QIcon('images/numbers/50.png'))
        self.fifty.setIconSize(QtCore.QSize(200,200))
        self.fifty.clicked.connect(lambda: self.press(50))

        self.hundred = QPushButton()
        self.hundred.setStyleSheet('color:white;font-size: 60px;border-radius: 8px;')
        self.hundred.setIcon(QtGui.QIcon('images/numbers/100.png'))
        self.hundred.setIconSize(QtCore.QSize(200,200))
        self.hundred.clicked.connect(lambda: self.press(100))

        self.layout.addWidget(self.fifteen)
        self.layout.addWidget(self.twenty_five)
        self.layout.addWidget(self.fifty)
        self.layout.addWidget(self.hundred)

    def press(self, numb):

        self.parent_class.put_time(numb)

    def keyPressEvent(self, event):

        match event.text():

            case '1':

                self.press(15)
            
            case '2':

                self.press(25)

            case '3':

                self.press(50)

            case '4':

                self.press(100)

            case _:

                if event.key() == QtCore.Qt.Key_Escape:

                    self.parent_class.change_to_languageChanger()
