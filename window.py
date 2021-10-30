import math

from ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from notMain import ConstParameters, Silicon, J2eV, eV2J, perSm2M


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Application()
        self.ui.setupUi(self)



        self.E_g = eV2J(1.12)
        # 1.12 eV
        self.E_d = eV2J(0.5)
        # 10 : 400 K
        self.T = 10
        # 1.12 eV
        self.E_c = eV2J(1.12)
        # 0.36*m0
        self.m = 0.36 * ConstParameters.m0kg
        # 1e+15 : 1e+22 per sm
        self.N_d0 = perSm2M(1e+15)
        self.k = ConstParameters.kJ
        self.h = ConstParameters.hJ

        self.x1 = np.linspace(0, eV2J(10), 100)
        self.silic = Silicon(self.E_g, self.E_d, self.T, self.E_c,
                             self.m, self.N_d0, self.k, self.h)

        self.plot = self.ui.plot1.plot()
        self.E_dChanged(0)
        self.E_dChanged(0)

        self.ui.Ed_silder.valueChanged.connect(self.E_dChanged)
        self.ui.Nd0_slider.valueChanged.connect(self.N_d0Changed)

        self.ui.T_slider.valueChanged.connect(self.T_Changed)

    def E_dChanged(self, val):
        valf = float(val)/100
        self.E_g = eV2J(val)
        self.ui.Ed_lineEdit.clear()
        self.ui.Ed_lineEdit.insert(str(valf))
        self.plotData()

    def N_d0Changed(self, val):
        valf = 1e15 * (10 ** val)
        self.N_d0 = perSm2M(valf)
        self.ui.Nd0_lineEdit.clear()
        self.ui.Nd0_lineEdit.insert(str(f"1e{15 + val}"))
        self.plotData()

    def T_Changed(self, val):
        self.T = val
        self.ui.T1_lineEdit.clear()
        self.ui.T1_lineEdit.insert(str(val))
        self.plotData()

    def plotData(self):
        self.silic = Silicon(self.E_g, self.E_d, self.T, self.E_c,
                             self.m, self.N_d0, self.k, self.h)
        y1 = [self.silic.equation()(i) for i in self.x1]
        self.plot.setData(self.x1, y1)

