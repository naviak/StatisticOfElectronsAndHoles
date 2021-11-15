from fdint import *
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

    k_new = 1.381 * 1e-16
    h_new = 6.626 * 1e-27
    h_bar_new = 1.055 * 1e-27
    ev_new = 1.602 * 1e-12
    m_new = 9.109 * 1e-28


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
        expArg = (np.longdouble(self.E_g - self.E_d - nu)) / np.longdouble((self.T * self.k))

        exp = np.exp(expArg)
        res = self.N_d0 / (1 + exp)
        return res

    def n_new(self, nu):
        effective_state_of_density = 2 * ((2 * np.pi * self.m * self.k * self.T) / self.h ** 2) ** (3 / 2)
        fd = fdk(k=0.5, phi=(nu - self.E_c) / (self.k * self.T))
        return fd * effective_state_of_density

    def new_equation(self):
        return lambda nu: self.N0Plus(nu) - self.n_new(nu)

    def N0Plus_T(self, nu, T):
        expArg = (np.longdouble(self.E_g - self.E_d - nu)) / np.longdouble((T * self.k))

        exp = np.exp(expArg)
        res = self.N_d0 / (1 + exp)
        return res
    """короче все новые хуйности с T это адаптеры для хуйни с помощбю которой они корни находили """
    """я протестил все работает"""
    def n_new_T(self, nu, T):
        effective_state_of_density = 2 * ((2 * np.pi * self.m * self.k * T) / (2 * self.h * np.pi) ** 2) ** (3 / 2)
        fd = fdk(k=0.5, phi=(nu - self.E_c) / (self.k * T))
        return fd * effective_state_of_density

    def new_equation_T(self, nu, T):
        return self.N0Plus_T(nu, T) - self.n_new_T(nu, T)

    def fndRs(self, T0, T1, NT: int):
        v_n = list()
        v_F = list()
        v_T = list()
        dT = (T1 - T0) / NT
        T = T0
        while T < T1:
            itr = 0
            a = -4.0 * self.E_g
            b = 4.0 * self.E_g
            tol = 1e-8 * self.E_g
            F = 0
            while self.new_equation_T(F, T) != 0.0 and b - a > tol and itr < 1000:
                F = (a + b) / 2.0
                if self.new_equation_T(F, T) == 0:
                    a = F
                    b = F
                else:
                    if self.new_equation_T(F, T) > 0:
                        a = F
                    else:
                        b = F
                itr += 1
            v_F.append(F)
            v_n.append((self.n_new_T(F, T)))
            v_T.append(T)

            T += dT
        return np.array(v_F), np.array(v_n), np.array(v_T)


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
        if (arr[i] > 0):
            right = rg[i + 1]
            left = rg[i]
            break
    return (right + left) / 2
