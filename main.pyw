import sys
from PyQt5.QtWidgets import QApplication
from window import MainWindow
import warnings
if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    app = QApplication(sys.argv)
    wind = MainWindow()
    wind.show()
    sys.exit(app.exec_())
