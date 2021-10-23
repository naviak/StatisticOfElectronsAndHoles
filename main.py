import sys
from PyQt5.QtWidgets import QApplication
from window import MainWindow
import qtmodern.styles
import qtmodern.windows
if __name__ == '__main__':
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)
    wind = MainWindow()
    mw = qtmodern.windows.ModernWindow(wind)
    mw.show()
    sys.exit(app.exec_())
