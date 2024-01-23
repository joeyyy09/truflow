# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'landingpage.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

import basicdetails


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("TrueFlow")
        MainWindow.resize(404, 349)
        MainWindow.setStyleSheet("background-color:rgb(12, 4, 4);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 180, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("color:rgb(255, 255, 255)")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Enter your Username")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(260, 180, 93, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("color:rgb(255, 255, 255);\n"
"border:1px solid white;")
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(lambda: self.username_On_Continue(MainWindow))

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 120, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setStyleSheet("color:rgb(255, 255, 255);\n"
"\n"
"")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TrueFlow"))
        
        self.pushButton.setText(_translate("MainWindow", "Continue"))
        self.label.setText(_translate("MainWindow", "TruFlow"))

    def username_On_Continue(self, MainWindow):
        print(self.lineEdit.text()) #ToDo: To store username and move to next 
        self.window = QtWidgets.QMainWindow()
        self.ui = basicdetails.Ui_BasicDetailsWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        MainWindow.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
