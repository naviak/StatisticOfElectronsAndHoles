import math

from ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from silicon import ConstParameters, Silicon, J2eV, eV2J, perSm2M, findRightSolution


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Application()
        self.ui.setupUi(self)

        self.E_g = 1.12
        # 1.12 eV
        self.E_d = 1
        # 10 : 400 K
        self.T = 10
        # 1.12 eV
        self.E_c = 1.12
        # 0.36*m0
        self.m = 0.36 * ConstParameters.m0eV
        # 1e+15 : 1e+22 per sm
        self.N_d0 = 1e+15
        self.k = ConstParameters.keV
        self.h = ConstParameters.heV

        self.x1 = np.linspace(-30, 30, 200)
        self.silic = Silicon(self.E_g, self.E_d, self.T, self.E_c,
                             self.m, self.N_d0, self.k, self.h)

        self.plot = self.ui.plot1.plot()
        self.line = self.ui.plot2.plot()
        self.plot2 = self.ui.plot2.plot()
        self.E_dChanged(1)
        self.plotData()
        self.plotData()
        self.plotData2()
        self.plotData2()
        self.ui.Ed_silder.valueChanged.connect(self.E_dChanged)
        self.ui.Nd0_slider.valueChanged.connect(self.N_d0Changed)
        self.line = self.ui.plot2.plot([0, 400], [1.12, 1.12])
        self.ui.T_slider.valueChanged.connect(self.T_Changed)

    def E_dChanged(self, val):
        valf = float(val) / 100
        self.E_d = valf
        self.ui.Ed_lineEdit.clear()
        self.ui.Ed_lineEdit.insert(str(valf))
        self.plotData()
        self.plotData2()

    def N_d0Changed(self, val):
        valf = 1e15 * (10 ** val)
        self.N_d0 = valf
        self.ui.Nd0_lineEdit.clear()
        self.ui.Nd0_lineEdit.insert(str(f"1e{15 + val}"))
        self.plotData()
        self.plotData2()

    def T_Changed(self, val):
        self.T = val
        self.ui.T1_lineEdit.clear()
        self.ui.T1_lineEdit.insert(str(val))
        self.plotData()

    def plotData(self):
        self.silic = Silicon(self.E_g, self.E_d, self.T, self.E_c,
                             self.m, self.N_d0, self.k, self.h)
        y1 = [self.silic.new_equation()(i) for i in self.x1]
        # y2 = [ self.silic.n(i) for i in self.x1]
        # y3 = [ self.silic.N0Plus(i) for i in self.x1]
        print('x = ' + str(findRightSolution(y1, self.x1)))

        self.plot.setData(self.x1, y1)
        # self.plot.setData(self.x1, y2)
        # self.plot.setData(self.x1, y3)

    def plotData2(self):
        T1 = np.linspace(0, 400, 300)
        sols = [findRightSolution([Silicon(
            self.E_g, self.E_d, t, self.E_c, self.m, self.N_d0, self.k,
            self.h).new_equation()(i) for i in self.x1], self.x1) for t in T1]
        self.plot2.setData(T1, sols)

    def plotData2_n(self):
        self.silic = Silicon(self.E_g, self.E_d, self.T, self.E_c,
                             self.m, self.N_d0, self.k, self.h)
        sol, _, T = self.silic.fndRs(0.1, 400, 100)
        assert T.shape == sol.shape
        self.plot2.setData(T, sol)
