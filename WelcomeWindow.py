import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

from MainWidget import GeneralWindow
from ModeChangerWidget import ModeChangerWindow 

class MainMenu(GeneralWindow):

    def __init__(self, parent_class=None):

        super().__init__()

        self.parent_class = parent_class

        self.stack_widgets = QStackedWidget()

        self.welcome     = WelcomeWindow(self)
        self.modeChanger = ModeChangerWindow(self) 

        self.stack_widgets.addWidget(self.welcome)
        self.stack_widgets.addWidget(self.modeChanger)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.stack_widgets)

        self.setLayout(self.layout)

        self.change_to_welcome()

    def change_to_welcome(self):

        self.stack_widgets.setCurrentIndex(0)
        self.welcome.setFocusPolicy(True)

    def change_to_modeChanger(self):

        self.stack_widgets.setCurrentIndex(1)
        self.modeChanger.setFocusPolicy(True)

    def change_to_main(self):

        self.change_to_modeChanger()

class WelcomeWindow(GeneralWindow):

    def __init__(self, parent_class=None):

        super().__init__()

        self.parent_class = parent_class
    
        self.layout = QVBoxLayout()

        self.logo_image = QPixmap("images/logo.jpg")
        self.logo_label = QLabel()
        self.logo_label.setPixmap(self.logo_image)
        self.logo_label.setAlignment(Qt.AlignCenter)
    
        self.label = QLabel("...Press 'Space' to continue...")
        self.label.setStyleSheet('color: white; font-size: 40px; font-family: Courier New, monospace')
        self.label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.logo_label)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

    def keyPressEvent(self, event):

        if event.key() ==  QtCore.Qt.Key_Escape:

            self.destroy()

        elif event.key() == QtCore.Qt.Key_Space:

            self.parent_class.change_to_modeChanger()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())