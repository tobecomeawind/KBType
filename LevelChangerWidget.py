import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5 import QtGui
from PyQt5 import QtCore

from MainWidget import GeneralWindow

class LevelChangerWindow(GeneralWindow):
    
    def __init__(self, parent_class=None):

        super().__init__()

        self.parent_class = parent_class

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.buttons = list()

        self.add_buttons()

    def add_buttons(self):

        positions = [(i, j) for i in range(3) for j in range(3)]
       
        for index, position in enumerate(positions, start=1):

            button = QPushButton()

            button.setIcon(QtGui.QIcon(f'images/numbers/level_numbers/{index}.png'))
            button.setStyleSheet('color:white;font-size: 100px;border-radius: 2px;')
            button.setIconSize(QtCore.QSize(200,200))
            
            self.grid.addWidget(button, *position)
            self.buttons.append(button)

    def connect_buttons(self, lang):

        for index, button in enumerate(self.buttons, start=1):

            button.disconnect()
            button.clicked.connect(lambda: self.press(f"level{index}"))

    def press(self, file):

        self.parent_class.put_level(file)

    def keyPressEvent(self, event):

        if event.key() == QtCore.Qt.Key_Escape:

            self.parent_class.change_to_languageChanger()

        if event.text().isdigit() and 0 < int(event.text()) < 10:

            self.press("level"+event.text()) 







