# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '01.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(670, 620)
        MainWindow.setMinimumSize(QtCore.QSize(670, 620))
        MainWindow.setMaximumSize(QtCore.QSize(670, 620))
        MainWindow.setStyleSheet("background-color: rgb(245, 222, 179)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(200, 150, 311, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.give_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.give_button.setStyleSheet("background-color: rgb(253, 245, 230)")
        self.give_button.setObjectName("give_button")
        self.verticalLayout.addWidget(self.give_button)
        self.put_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.put_button.setStyleSheet("background-color: rgb(253, 245, 230)")
        self.put_button.setObjectName("put_button")
        self.verticalLayout.addWidget(self.put_button)
        self.add_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.add_button.setStyleSheet("background-color: rgb(253, 245, 230)")
        self.add_button.setObjectName("add_button")
        self.verticalLayout.addWidget(self.add_button)
        self.data_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.data_button.setStyleSheet("background-color: rgb(253, 245, 230)")
        self.data_button.setObjectName("data_button")
        self.verticalLayout.addWidget(self.data_button)
        self.student_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.student_button.setStyleSheet("background-color: rgb(253, 245, 230)")
        self.student_button.setObjectName("student_button")
        self.verticalLayout.addWidget(self.student_button)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 100, 311, 31))
        self.label.setStyleSheet("background-color: rgb(253, 245, 230)")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.menu.addSeparator()
        self.menu_2.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.give_button.setText(_translate("MainWindow", "Выдать книгу"))
        self.put_button.setText(_translate("MainWindow", "Принять книгу"))
        self.add_button.setText(_translate("MainWindow", "Добавить книгу"))
        self.data_button.setText(_translate("MainWindow", "Книжная полка"))
        self.student_button.setText(_translate("MainWindow", "Ученики"))
        self.label.setText(_translate("MainWindow", "                           Выберете действие"))
        self.menu.setTitle(_translate("MainWindow", " "))
        self.menu_2.setTitle(_translate("MainWindow", " "))
        self.action.setText(_translate("MainWindow", " "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
