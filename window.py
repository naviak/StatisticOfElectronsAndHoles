from ui import *
from PyQt5 import QtWidgets
import numpy as np
from silicon import ConstParameters, Silicon, findRightSolution
import pyqtgraph as pg


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Application()
        self.ui.setupUi(self)

        self.E_g = 1.12 * ConstParameters.ev_new
        # 1.12 eV
        self.E_d = self.E_g - 0.054 * ConstParameters.ev_new
        # 10 : 400 K
        self.T = 10
        # 1.12 eV
        self.E_c = 1.12 * ConstParameters.ev_new
        # 0.36*m0
        self.m = 0.36 * ConstParameters.m_new
        # 1e+15 : 1e+22 per sm
        self.N_d0 = 1e+15
        self.k = ConstParameters.k_new
        self.h = ConstParameters.h_new

        self.x1 = np.linspace(-5, 5, 200)
        self.silic = Silicon(self.E_g, self.E_d, self.T, self.E_c,
                             self.m, self.N_d0, self.k, self.h)
        self.plot = self.ui.plot1.plot(pen=pg.mkPen(color='g', width=2))
        self.plot2 = self.ui.plot2.plot(pen=pg.mkPen(color='g', width=2))
        self.line = self.ui.plot2.plot([0, 400], [1.12, 1.12], pen=pg.mkPen(color='r', width=2))

        self.E_dChanged(1)
        self.N_d0Changed(0)
        self.plotData()
        self.plotData()
        self.plotData2_n()
        self.plotData2_n()
        self.ui.Ed_silder.valueChanged.connect(self.E_dChanged)
        self.ui.Nd0_slider.valueChanged.connect(self.N_d0Changed)

        self.sols = []
        self.T_range = []

    def E_dChanged(self, val):
        valf = float(val) / 100
        self.E_d = valf * ConstParameters.ev_new
        self.ui.Ed_lineEdit.clear()
        self.ui.Ed_lineEdit.insert(str(valf) + ', eV')
        self.plotData2_n()
        self.plotData()

    def N_d0Changed(self, val):
        valf = 1e15 * (10 ** val)
        self.N_d0 = valf
        self.ui.Nd0_lineEdit.clear()
        self.ui.Nd0_lineEdit.insert(str(f"1e{15 + val}"))
        self.plotData2_n()
        self.plotData()

    def plotData(self):
        self.silic = Silicon(self.E_g, self.E_d, self.T, self.E_c,
                             self.m, self.N_d0, self.k, self.h)
        # y1 = [self.silic.new_equation()(i) for i in self.x1]
        # y2 = [ self.silic.n(i) for i in self.x1]
        y1 = [Silicon(self.E_g, self.E_d, self.T_range[i], self.E_c,
                      self.m, self.N_d0, self.k, self.h).N0Plus(self.sols[i]) for i in range(len(self.T_range))]

        self.plot.setData(self.T_range, y1)
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
        self.sols, _, self.T_range = self.silic.fndRs(10, 400, 100)

        self.plot2.setData(self.T_range, self.sols / ConstParameters.ev_new)
