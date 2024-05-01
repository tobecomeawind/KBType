from PyQt5.QtWidgets import QWidget

class GeneralWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle('KBType')

        self.setStyleSheet('background : black')