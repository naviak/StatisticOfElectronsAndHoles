from PyQt5 import QtCore, QtGui, QtWidgets
from informationui import Ui_Information


class InfoDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__()

        self.setWindowTitle("HELLO!")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.ui = Ui_Information()
        self.ui.setupUi(self)
        self.ui.OkButton.clicked.connect(self.close)
