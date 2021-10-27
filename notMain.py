import scipy.constants as constant
import scipy.integrate as integrate
import numpy as np
import matplotlib.pyplot as plt
class ConstParameters:
    kJ = constant.k
    keV = 8.617*1e-5
    hJ = constant.Planck
    heV = 4.135*1e-15
    m0kg = constant.electron_mass
    m0eV = 0.511*1e+6



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

    def f(self, x, nu):
        expArg = (x - nu)/(self.k * self.T)
        exp = np.exp(expArg)
        return 1/(1 + exp)

    def g(self, x):
        return 4 * np.pi * np.sqrt((2 * self.m)**3)* np.sqrt(x - self.E_c) / (self.h ** 3)

    def n(self, nu):
        return integrate.quad(lambda x: self.f(x, nu) * self.g(x) , self.E_c, 2 * self.E_c)[0]

    def N0Plus(self, nu):
        expArg = (self.E_g - self.E_d - nu)/(self.T * self.k)
        exp = np.exp(expArg)
        return self.N_d0/(1 + exp)

def J2eV(x):
    return x/(1.6e-19)

def eV2J(x):
    return x*1.6e-19

def perSm2M(x):
    return x*1e+6

# 1.12 eV
E_g = eV2J(1.12)
# 1.12 eV
E_d = eV2J(0.5)
# 10 : 400 K
T = 10
# 1.12 eV 
E_c = eV2J(1.12)
# 0.36*m0
m = 0.36 * ConstParameters.m0kg
# 1e+15 : 1e+22 per sm
N_d0 = perSm2M(1e+20)
k = ConstParameters.kJ
h = ConstParameters.hJ

silic = Silicon(E_g ,E_d, T, E_c, m, N_d0, k, h)
eq = silic.equation()

xu = np.linspace(0, eV2J(10), 100)
x = np.linspace(0, 1e-18, 1000)

yf= [silic.f(i, eV2J(1)) for i in x]
yg = [silic.g(i) for i in x]

yno = [silic.N0Plus(i) for i in xu]
yn = [silic.n(i) for i in xu]

yeq = [eq(i) for i in xu]

#plt.plot(x,yf)
#plt.plot(x,yg)
#plt.plot(xu,yno)
#plt.plot(xu,yn)
plt.plot(xu,yeq)

plt.show()