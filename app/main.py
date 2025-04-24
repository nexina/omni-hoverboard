from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget,  QFileIconProvider, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import hoverboard
import pathlib
import os,sys
import webbrowser
from win32com.client import Dispatch
import getpass
USER_NAME = getpass.getuser()

current_directory = str(pathlib.Path(__file__).parent.absolute())

if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

class Ui_MainWindow(object):
    
    def show_form(self):
        self.main.show()
        self.main.activateWindow()
        self.main.setFocus(QtCore.Qt.PopupFocusReason)
        self.main.setFocus(True)
        self.main.transition_in.start()
        self.main.leaveEvent = lambda e: self.main.transition_out.start()

    def setupUi(self, MainWindow):
        shell = Dispatch('WScript.Shell')
        path = os.path.join(r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" % USER_NAME, "Hover Board.lnk")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = current_directory + "\Hover Board.exe"
        shortcut.WorkingDirectory = current_directory
        shortcut.IconLocation = current_directory + "\Hover Board.exe"
        shortcut.save()
        
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(61, 10)
        MainWindow.setWindowTitle('Hover Board')
        MainWindow.setWindowIcon(QIcon("resources/omni_hoverboard.png"))
        MainWindow.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint |  QtCore.Qt.Tool)

        shortcut_open = QShortcut(QKeySequence('Ctrl+`'), MainWindow)
        shortcut_open.activated.connect(self.show_form)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setStyleSheet("background:transparent;");
        MainWindow.setAttribute(Qt.WA_TranslucentBackground);
        self.centralwidget.setObjectName("centralwidget")
        self.hover_widget = QtWidgets.QLabel(self.centralwidget)
        self.hover_widget.setGeometry(QtCore.QRect(0, 0, 61, 10))
        self.hover_widget.setText("")
        self.hover_widget.setStyleSheet("#hover_widget{border-image : url(resources/hover_icon.png);background-repeat: no-repeat;}")

        MainWindow.transition_in = QPropertyAnimation(MainWindow, b"geometry")
        MainWindow.transition_in.setDuration(500)
        MainWindow.transition_in.setStartValue(QRect(QApplication.desktop().screenGeometry().width() - 180, -9, 61, 10))
        MainWindow.transition_in.setEndValue(QRect(QApplication.desktop().screenGeometry().width() - 180, 0, 61, 10))
        MainWindow.transition_in.finished.connect(self.show_form)
        
        MainWindow.transition_out = QPropertyAnimation(MainWindow, b"geometry")
        MainWindow.transition_out.setDuration(1000)
        MainWindow.transition_out.setEndValue(QRect(QApplication.desktop().screenGeometry().width() - 180, -9, 61, 10))
        MainWindow.transition_out.setStartValue(QRect(QApplication.desktop().screenGeometry().width() - 180, 0, 61, 10))  
        MainWindow.transition_out.start()


        self.main = QtWidgets.QMainWindow()
        self.ui = hoverboard.Ui_main()
        self.ui.setupUi(self.main)
        

        self.hover_widget.enterEvent = lambda e: MainWindow.transition_in.start()
        self.hover_widget.leaveEvent = lambda e: MainWindow.transition_out.start()


        self.hover_widget.setAlignment(QtCore.Qt.AlignCenter)
        self.hover_widget.setObjectName("hover_widget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hover Widget"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    icon = QIcon("resources/omni_hoverboard.png")

    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    menu = QMenu()

    option1 = menu.addAction("Check Our Website !")
    option1.triggered.connect(lambda e: webbrowser.open("https://nexina.github.io/omni"))

    option2 = menu.addAction("Exit")
    option2.triggered.connect(sys.exit)

    tray.setContextMenu(menu)
    tray.show()

    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setGeometry(app.desktop().screenGeometry().width() - 180,0,0,0)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
