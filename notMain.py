import scipy.constants as constant
import scipy.integrate as integrate
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate.quadpack import _RangeFunc


class ConstParameters:
    kJ = constant.k
    keV = 8.617 * 1e-5
    hJ = constant.Planck
    heV = 4.135 * 1e-15
    m0kg = constant.electron_mass
    m0eV = 0.511 * 1e+6


class Silicon:
    def __init__(self, E_g, E_d, T, E_c, m, N_d0, k, h):
        self.setParams(E_g, E_d, T, E_c, m, N_d0, k, h)

    def setParams(self, E_g, E_d, T, E_c, m, N_d0, k, h):
        self.E_g = E_g
        self.E_d = E_d
        self.T = T
        self.E_c = E_c
        self.m = m
        self.N_d0 = N_d0
        self.k = k
        self.h = h

    def equation(self):
        return lambda nu: self.N0Plus(nu) - self.n(nu)

    def n(self, nu):
        factor = 1 / (2 * np.pi ** 2) * (2 * self.m / self.h ** 2) ** (3 / 2)
        return factor * integrate.quad(lambda x: (x - self.E_c) ** (1 / 2) / (np.exp((x - nu) / (self.k * self.T)) + 1),
                                       self.E_c, np.inf)[0]

    def N0Plus(self, nu):
        expArg = (self.E_g - self.E_d - nu) / (self.T * self.k)
        exp = np.exp(expArg)
        return self.N_d0 / (1 + exp)




def J2eV(x):
    return x / (1.6e-19)


def eV2J(x):
    return x * 1.6e-19


def perSm2M(x):
    return x * 1e+6


def findRightSolution(arr, rg):
    right = 0
    left = 0
    for i in range(len(arr) - 1, 0, -1):
        if arr[i] > 0:
            right = rg[i + 1]
            left = rg[i]
            break
    return (right + left) / 2




