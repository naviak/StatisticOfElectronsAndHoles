import scipy.constants as constant
import scipy.integrate as integrate
import numpy as np
import matplotlib.pyplot as plt
class ConstParameters:
    k = constant.k
    h = constant.Planck


class Silicon:
    def __init__(self, E_g, E_d, T, E_c, m, N_d0):
        self.setParams(E_g, E_d, T, E_c, m, N_d0)

    def setParams(self, E_g, E_d, T, E_c, m, N_d0):
        self.E_g = E_g
        self.E_d = E_d
        self.T = T
        self.E_c = E_c
        self.m = m
        self.N_d0 = N_d0
        
    def equation(self):
        return lambda nu: self.N0Plus(nu) - self.n(nu)

    def f(self, x, nu):
        exp = np.exp((x - nu)/(ConstParameters.k * self.T))
        return 1/(1 + exp)

    def g(self, x):
        return 4 * np.pi * np.sqrt((2 * self.m)**3)* np.sqrt(x - self.E_c) / (ConstParameters.h ** 3)

    def n(self, nu):
        return integrate.quad(lambda x: self.f(x, nu) * self.g(x) , self.E_c, 2 * self.E_c)[0]

    def N0Plus(self, nu):
        exp = (self.E_g - self.E_d - nu)/(self.T * ConstParameters.k)
        return self.N_d0/(1 + np.exp(exp))


silic = Silicon(8.0*1.6e-19, 0.0*1.6e-19, 1000 , 1.0*1.6e-19, 5.0e-31, 1e+14)
eq = silic.equation()

x = np.linspace(0,100.0*1.6e-19, 100)
y= [eq(i) for i in x]


plt.plot(x,y)

plt.show()