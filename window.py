import math

from ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Application()
        self.ui.setupUi(self)
        self.x1 = np.linspace(0, 100, 2000)
        self.y1 = [math.sin(x) for x in self.x1]
        self.plot = self.ui.plot1.plot(self.x1, self.y1)
        self.ui.silder1.valueChanged.connect(self.plotGraph1)

    def plotGraph1(self, val):
        self.x1 = np.linspace(0, 100, 2000)
        self.y1 = [math.sin(val*x) for x in self.x1]
        self.plot.setData(self.x1, self.y1)
