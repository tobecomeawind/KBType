import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from PyQt5 import QtGui
from PyQt5 import QtCore

from MainWidget import GeneralWindow
from FreeGameWidget import FreeGameWindow

class Buttons(GeneralWindow):

    def __init__(self, parent_class):
        
        super().__init__()

        self.parent_class = parent_class

        self.layout = QVBoxLayout()

        self.add_buttons()

        self.setLayout(self.layout)
        self.setWindowTitle("Main Window")

    def add_buttons(self):

        self.levelsB   = QPushButton("Levels")
        self.levelsB.setStyleSheet('color:white;font-size: 60px;border-radius: 8px;')
        self.levelsB.setIcon(QtGui.QIcon('images/level.png'))
        self.levelsB.setIconSize(QtCore.QSize(200,200))

        self.freeGameB = QPushButton("Free")
        self.freeGameB.setStyleSheet('color:white;font-size: 60px;border-radius: 8px;')
        self.freeGameB.setIcon(QtGui.QIcon('images/free.png'))
        self.freeGameB.setIconSize(QtCore.QSize(200,200))
        
        self.timeGameB = QPushButton("Time")
        self.timeGameB.setStyleSheet('color:white;font-size: 60px;border-radius: 8px;')
        self.timeGameB.setIcon(QtGui.QIcon('images/time.png'))
        self.timeGameB.setIconSize(QtCore.QSize(200,200))

        self.layout.addWidget(self.levelsB)
        self.layout.addWidget(self.freeGameB)
        self.layout.addWidget(self.timeGameB)


class ModeChangerWindow(GeneralWindow):

    def __init__(self, parent_class):
        
        super().__init__()

        self.layout = QVBoxLayout()

        self.parent_class = parent_class

        self.stack_widget = QStackedWidget()

        self.buttons = Buttons(self)
        self.free    = FreeGameWindow(self)

        self.buttons.freeGameB.clicked.connect(self.change_to_free)

        self.stack_widget.addWidget(self.buttons)
        self.stack_widget.addWidget(self.free)

        self.layout.addWidget(self.stack_widget)

        self.setLayout(self.layout)

        self.change_to_buttons()


    def change_to_levels(self):

        pass

    def change_to_free(self):

        self.stack_widget.setCurrentIndex(1)
        self.buttons.setFocusPolicy(True)

    def change_to_time(self):
        
        pass

    def change_to_buttons(self):

        self.stack_widget.setCurrentIndex(0)
        self.buttons.setFocusPolicy(True)

    def change_to_main(self):

        self.parent_class.change_to_main()