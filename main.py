import numpy as np
import numpy.fft as fft
import pyqtgraph as pg
from scipy import signal
app = pg.mkQApp()
sampling = 0.1


class MultiLine(pg.QtGui.QGraphicsPathItem):
    def __init__(self, x, y):
        self.path = pg.arrayToQPath(x, y)
        pg.QtGui.QGraphicsPathItem.__init__(self, self.path)
        self.setPen(pg.mkPen('w', width=2))

    def shape(self):
        return pg.QtGui.QGraphicsItem.shape(self)

    def boundingRect(self):
        return self.path.boundingRect()


def FFT(data):
    return fft.fft(data, len(data))


def iFFT(data):
    return fft.ifft(data)


def getFreqAxis(x):
    samplingFreq = 1 / sampling
    return np.arange(-samplingFreq / 2, samplingFreq / 2, samplingFreq / len(x))


def drawPlot(x, ft, view, name):
    fftData = ft
    tmp = np.split(fftData, 2)
    fs = np.concatenate([tmp[1], tmp[0]])
    freqAxis = getFreqAxis(x)
    lines = MultiLine(freqAxis, np.abs(fs))
    w1 = view.addPlot()
    w1.setTitle(name)
    w1.addItem(lines)
    view.show()


def drawSimplePlot(x, y, view, name):
    lines = MultiLine(x, y)
    w1 = view.addPlot()
    w1.setTitle(name)
    w1.addItem(lines)
    view.show()


N = 100


def Hann(n):
    return np.sin(np.pi*n/N)**2


def Hanning(n):
    return 0.53836 - 0.46164*np.cos(2*np.pi*n/(N-1))

def slide(x):
    return 1 - x


def evenSlide(x):
    return slide(x) if x > 0 else slide(-x)


def oddSlide(x):
    return slide(x) if x > 0 else -slide(-x)


view1 = pg.GraphicsLayoutWidget(title="func1")
x = np.arange(-5, 5, sampling)
data = np.sin(np.sin(x))
drawSimplePlot(x,data,view1,'sin')
drawPlot(x, FFT(data), view1,'fft')
drawPlot(x, FFT(data*np.vectorize(Hanning)(x)), view1,'fft hanning')
drawPlot(x, FFT(data*np.vectorize(Hann)(x)), view1,'fft hann')

view2 = pg.GraphicsLayoutWidget(title="func2")
data = [1 if abs(val) <= 0.5 else 0 for val in x]
drawSimplePlot(x,data,view2,'rect')
drawPlot(x, FFT(data), view2, 'fft')
drawPlot(x, FFT(data*np.vectorize(Hanning)(x)), view2, 'fft hanning rect')
drawPlot(x, FFT(data*np.vectorize(Hann)(x)), view2, 'fft hann rect')


view3 = pg.GraphicsLayoutWidget(title="func3")
data = np.vectorize(oddSlide)(x)
drawPlot(x, FFT(data),view3,'Odd slide fft')
drawPlot(x, FFT(data*np.vectorize(Hanning)(x)), view3, 'Windowed fft hanning')
drawPlot(x, FFT(data*np.vectorize(Hann)(x)), view3, 'Windowed fft hann')

view4 = pg.GraphicsLayoutWidget(title="func4")
drawSimplePlot(x, data,view4, 'odd slide')
windowedData = FFT(data*np.vectorize(Hanning)(x))
windowedDataHann = FFT(data*np.vectorize(Hann)(x))
drawSimplePlot(x, np.real(iFFT(windowedData)/np.vectorize(Hanning)(x)),view4,'Func to Normal w Hanning')
drawSimplePlot(x, np.real(iFFT(windowedDataHann)/np.vectorize(Hann)(x)),view4,'Func to Normal w Hann')

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        app.exec_()
