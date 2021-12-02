from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Information(object):
    def setupUi(self, Information):
        Information.setObjectName("Information")
        Information.resize(700, 300)
        Information.setMinimumSize(QtCore.QSize(700, 300))
        Information.setMaximumSize(QtCore.QSize(700, 300))
        self.gridLayout = QtWidgets.QGridLayout(Information)
        self.gridLayout.setObjectName("gridLayout")
        self.OkButton = QtWidgets.QPushButton(Information)
        self.OkButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.OkButton.setObjectName("OkButton")
        self.gridLayout.addWidget(self.OkButton, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(Information)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 3)
        self.th = QtWidgets.QLabel(Information)
        self.th.setText("")
        self.th.setObjectName("ImageLabel")
        self.gridLayout.addWidget(self.th, 1, 0, 1, 1)
        self.th = QtWidgets.QLabel(Information)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.th.setFont(font)
        self.th.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.th.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.th.setWordWrap(True)
        self.th.setOpenExternalLinks(True)
        self.th.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.th.setObjectName("textLabel")
        self.gridLayout.addWidget(self.th, 0, 0, 1, 3)

        self.retranslateUi(Information)
        QtCore.QMetaObject.connectSlotsByName(Information)

    def retranslateUi(self, Information):
        _translate = QtCore.QCoreApplication.translate
        Information.setWindowTitle(_translate("Information", "О создателях"))
        self.OkButton.setText(_translate("Information", "Закрыть"))
        self.th.setText(_translate("Information", "Программа написана двумя студентами АФТИ НГУ 2021\n"
                                                  "\n"
                                                  "Контакты:\n"
                                                  "Дударь Максим: m.dudar@g.nsu.ru\n"
                                                  "Пищев Иван: i.pishchev@g.nsu.ru"))
