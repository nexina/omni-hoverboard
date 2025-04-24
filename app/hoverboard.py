from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QRect, QFileInfo, QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QFileIconProvider
from datetime import datetime
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import psutil
import pickle
import os
import screen_brightness_control as sbc
import socket
import sys 
import time
import gc
import netifaces
import requests
from requests import get
from json import *
import bluetooth
import pyrebase
from getpass import getpass


if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

IPaddress=socket.gethostbyname(socket.gethostname())
if IPaddress!="127.0.0.1":
    app_version = "0.1"

class WorkerThread(QtCore.QThread):
    signalExample = QtCore.pyqtSignal(str, str,str,str)

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.is_running = True

    @QtCore.pyqtSlot()
    def run(self):
        while True:
                cpu = str(psutil.cpu_percent(interval=0.5))
                ram = str(psutil.virtual_memory().percent)
                times = datetime.now().strftime('%I:%M %p')
                date = datetime.now().strftime('%d %B %Y')
                self.signalExample.emit(cpu,ram,times,date)
                time.sleep(3)
  

class Ui_main(object):

    def shutdown(self):
         os.system("shutdown /s /t 1")

    def reboot(self):
         os.system("shutdown /r /t 1")

    def hibernate(self):
         os.system(r'rundll32.exe powrprof.dll,SetSuspendState Hibernate')

    def brightnessvaluechange(self, br):
         sbc.set_brightness(br)

    def volumevaluechange(self, vl):
         
         interface = AudioUtilities.GetSpeakers().Activate(
         IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
         volume = cast(interface, POINTER(IAudioEndpointVolume))
         try:
            volume.SetMasterVolumeLevel(vl, None)
         except:
            print("")
    
    def textchange(self):
         pickle.dump(self.note_textbox.toPlainText(),open("log",'wb'))

    def internetcheck(self):
         IPaddress=socket.gethostbyname(socket.gethostname())
         if IPaddress!="127.0.0.1":
                self.internet.setStyleSheet("#internet{border-image : url(resources/internet_avail.png);background-repeat: no-repeat;}")
         else:
                self.internet.setStyleSheet("#internet{border-image : url(resources/no_internet.png);background-repeat: no-repeat;}")
    
    def wificheck(self):
        devices = psutil.net_if_stats()
        for device_name, device in devices.items():
                if device.isup:
                        if "WiFi" in device_name:
                                self.wifi.setStyleSheet("#wifi{border-image : url(resources/wifi_avail.png);background-repeat: no-repeat;}")
                        else:
                                self.wifi.setStyleSheet("#wifi{border-image : url(resources/no_wifi.png);background-repeat: no-repeat;}")
    
    def ethernetcheck(self):
        devices = psutil.net_if_stats()
        for device_name, device in devices.items():
                if device.isup:
                        if "Ethernet" in device_name:
                               self.ethernet.setStyleSheet("#ethernet{border-image : url(resources/ethernet_avail.png);background-repeat: no-repeat;}")  
                        else:
                                self.ethernet.setStyleSheet("#ethernet{border-image : url(resources/no_ethernet.png);background-repeat: no-repeat;}")
                continue

    def bluetoothcheck(self):
        nearby_devices = bluetooth.discover_devices(lookup_names=True)
        if len(nearby_devices) == 0:
                self.bluetooth.setStyleSheet("#bluetooth{border-image : url(bluetooth_avail.png);background-repeat: no-repeat;}")
        else:
                self.bluetooth.setStyleSheet("#bluetooth{border-image : url(resources/no_bluetooth.png);background-repeat: no-repeat;}")
    


    def refreshUI(self,cpu,ram,times,date):   
        _translate = QtCore.QCoreApplication.translate
        self.cpu_label.setText(_translate("main", "CPU: " + cpu + "%"))
        self.ram_label.setText(_translate("main", "RAM: "  + ram + "%"))
        self.time_label.setText(_translate("main", times))
        self.date_label.setText(_translate("main", date))
        self.internetcheck()
        self.wificheck()
        self.ethernetcheck()
        gc.collect()

    def close(self):
        QtCore.QCoreApplication.exit()


    def loadurl(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://nexina.github.io/omni'))
        QtWidgets.QMainWindow().hide() 

    def loadfb(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://www.facebook.com/'))
        QtWidgets.QMainWindow().hide() 
        
    def loadyt(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://www.youtube.com'))
        QtWidgets.QMainWindow().hide() 
        
    def loadpn(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://www.pinterest.com/'))
        QtWidgets.QMainWindow().hide() 
        
    def loadtw(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://www.twitter.com/'))
        QtWidgets.QMainWindow().hide() 
        
    def loadnx(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://nexina.github.io/'))
        QtWidgets.QMainWindow().hide() 

    def hwgit(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://github.com/nexina/omni-hoverboard'))
        QtWidgets.QMainWindow().hide() 

        

    def appfive_openFileNameDialog(self):
        if os.path.isfile("app5"):
                app5_url = pickle.load(open("app5",'rb'))
                os.startfile(app5_url)
        else:
                options = QFileDialog.Options()
                fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);", options=options)
                if fileName:
                        pickle.dump(fileName,open("app5",'wb'))
                        app_icon = QFileIconProvider().icon(QFileInfo(fileName))
                else:
                        return
                self.app5_img.setIcon(app_icon)


    def appfour_openFileNameDialog(self):
        if os.path.isfile("app4"):
                app4_url = pickle.load(open("app4",'rb'))
                os.startfile(app4_url)
        else:
                options = QFileDialog.Options()
                fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);", options=options)
                if fileName:
                        pickle.dump(fileName,open("app4",'wb'))
                        app_icon = QFileIconProvider().icon(QFileInfo(fileName))
                else:
                        return
                self.app4_img.setIcon(app_icon)


    def appthree_openFileNameDialog(self):
        if os.path.isfile("app3"):
                app3_url = pickle.load(open("app3",'rb'))
                os.startfile(app3_url)
        else:
                options = QFileDialog.Options()
                fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);", options=options)
                if fileName:
                        pickle.dump(fileName,open("app3",'wb'))
                        app_icon = QFileIconProvider().icon(QFileInfo(fileName))
                else:
                        return
                self.app3_img.setIcon(app_icon)


    def apptwo_openFileNameDialog(self):
        if os.path.isfile("app2"):
                app2_url = pickle.load(open("app2",'rb'))
                os.startfile(app2_url)
        else:
                options = QFileDialog.Options()
                fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);", options=options)
                if fileName:
                        pickle.dump(fileName,open("app2",'wb'))
                        app_icon = QFileIconProvider().icon(QFileInfo(fileName))
                else:
                        return
                self.app2_img.setIcon(app_icon)

    def appone_openFileNameDialog(self):
        if os.path.isfile("app1"):
                app1_url = pickle.load(open("app1",'rb'))
                os.startfile(app1_url)
        else:
                options = QFileDialog.Options()
                fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);", options=options)
                if fileName != "":
                        pickle.dump(fileName,open("app1",'wb'))
                        app_icon = QFileIconProvider().icon(QFileInfo(fileName))
                else:
                        return
                self.app1_img.setIcon(app_icon)
    
    def opennotice(self):
        IPaddress=socket.gethostbyname(socket.gethostname())
        if IPaddress!="127.0.0.1":
            QtWidgets.QMainWindow().hide() 
    
    def setupUi(self, main):
        IPaddress=socket.gethostbyname(socket.gethostname())
        
        height = QApplication.desktop().screenGeometry().height()
        main.setObjectName("main")
        main.resize(280, height)
        main.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint |  QtCore.Qt.Tool)
        main.setWindowModality(Qt.ApplicationModal)
        main.setStyleSheet("")
        main.activateWindow()
        main.setFocus(QtCore.Qt.PopupFocusReason)
        main.setFocus(True)
        
        main.transition_in = QPropertyAnimation(main, b"geometry")
        main.transition_in.setDuration(700)
        main.transition_in.setStartValue(QRect(QApplication.desktop().screenGeometry().width(), 0, 280, QApplication.desktop().screenGeometry().height()))
        main.transition_in.setEndValue(QRect(QApplication.desktop().screenGeometry().width() - 280, 0, 280, QApplication.desktop().screenGeometry().height()))
        main.transition_in.start()
        
        main.transition_out = QPropertyAnimation(main, b"geometry")
        main.transition_out.setDuration(700)
        main.transition_out.setEndValue(QRect(QApplication.desktop().screenGeometry().width(), 0, 280, QApplication.desktop().screenGeometry().height()))
        main.transition_out.setStartValue(QRect(QApplication.desktop().screenGeometry().width() - 280, 0, 280, QApplication.desktop().screenGeometry().height()))
        main.transition_out.start()
        main.transition_out.finished.connect(main.hide)
        
        self.worker = WorkerThread()
        self.workerThread = QtCore.QThread()
        self.workerThread.started.connect(self.worker.run)
        self.worker.signalExample.connect(self.refreshUI) 
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()
        
        self.centralwidget = QtWidgets.QWidget(main)
        self.centralwidget.setStyleSheet("QWidget{background-color: rgb(0, 0, 0);}")
        self.centralwidget.setObjectName("centralwidget")
        
        QtGui.QFontDatabase.addApplicationFont("resources/Roboto-Regular.ttf")
        
        self.background = QtWidgets.QFrame(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 280, height))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(False)
        font.setWeight(50)
        self.background.setFont(font)
        self.background.setStyleSheet("background-color: rgb(49, 49, 49);font-family:Roboto-Regular;")
        self.background.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.background.setFrameShadow(QtWidgets.QFrame.Raised)
        self.background.setObjectName("background")
        
        self.cpu_ram_frame = QtWidgets.QFrame(self.background)
        self.cpu_ram_frame.setGeometry(QtCore.QRect(80, height - 270, 201, 35))
        self.cpu_ram_frame.setStyleSheet("background-color: rgb(21, 21, 21);")
        self.cpu_ram_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cpu_ram_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cpu_ram_frame.setObjectName("cpu_ram_frame")
        
        self.ram_label = QtWidgets.QLabel(self.cpu_ram_frame)
        self.ram_label.setGeometry(QtCore.QRect(120, 0, 70, 35))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(7)
        self.ram_label.setFont(font)
        self.ram_label.setStyleSheet("QLabel{\n"
"    color: rgb(255, 255, 255);font-family:Roboto-Regular;\n"
"}")
        self.ram_label.setScaledContents(True)
        self.ram_label.setWordWrap(True)
        self.ram_label.setObjectName("ram_label")
        
        self.cpu_label = QtWidgets.QLabel(self.cpu_ram_frame)
        self.cpu_label.setGeometry(QtCore.QRect(30, 0, 70, 35))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(7)
        self.cpu_label.setFont(font)
        self.cpu_label.setStyleSheet("QLabel{\n"
"    color: rgb(255, 255, 255);font-family:Roboto-Regular;\n"
"}")
        self.cpu_label.setScaledContents(True)
        self.cpu_label.setWordWrap(True)
        self.cpu_label.setObjectName("cpu_label")
        
        self.cpu_ram_line = QtWidgets.QFrame(self.cpu_ram_frame)
        self.cpu_ram_line.setGeometry(QtCore.QRect(0, 0, 3, 35))
        self.cpu_ram_line.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.cpu_ram_line.setFrameShape(QtWidgets.QFrame.VLine)
        self.cpu_ram_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.cpu_ram_line.setObjectName("cpu_ram_line")
        
        self.note_frame = QtWidgets.QFrame(self.background)
        self.note_frame.setGeometry(QtCore.QRect(80, 305, 181, 131))
        self.note_frame.setStyleSheet("background-color: transparent;font-family:Roboto-Regular;")
        self.note_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.note_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.note_frame.setObjectName("note_frame")
        
        self.note_label = QtWidgets.QLabel(self.note_frame)
        self.note_label.setGeometry(QtCore.QRect(0, 0, 41, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.note_label.setFont(font)
        self.note_label.setStyleSheet("QLabel{\n"
"    color: rgb(255, 255, 255);font-family:Roboto-Regular;\n"
"}")
        self.note_label.setScaledContents(True)
        self.note_label.setWordWrap(True)
        self.note_label.setObjectName("note_label")
        
        self.note_textbox = QtWidgets.QPlainTextEdit(self.note_frame)
        self.note_textbox.setGeometry(QtCore.QRect(0, 20, 181, 111))
        self.note_textbox.setStyleSheet("border: 1px solid white;font-family:Roboto-Regular;\n"
"color : white")
        self.note_textbox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.note_textbox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.note_textbox.textChanged.connect(self.textchange)
        if not os.path.isfile("log"):
                 with open("log",'wb') as file:
                        pickle.dump("", file)


        self.note_textbox.setPlainText(pickle.load(open("log",'rb')))
        self.note_textbox.setObjectName("note_textbox")
        
        self.app_frame = QtWidgets.QFrame(self.background)
        self.app_frame.setGeometry(QtCore.QRect(0, 170, 281, 81))
        self.app_frame.setStyleSheet("background-color: transparent;")
        self.app_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.app_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.app_frame.setObjectName("app_frame")
        
        self.apps_label = QtWidgets.QLabel(self.app_frame)
        self.apps_label.setGeometry(QtCore.QRect(30, 16, 55, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        self.apps_label.setFont(font)
        self.apps_label.setStyleSheet("QLabel{\n"
"    color: rgb(255, 255, 255);font-family:Roboto-Regular;\n"
"}")
        self.apps_label.setScaledContents(True)
        self.apps_label.setWordWrap(True)
        self.apps_label.setObjectName("apps_label")
        
        self.app5_img = QtWidgets.QPushButton(self.app_frame)
        self.app5_img.setGeometry(QtCore.QRect(210, 40, 17, 17))
        if os.path.isfile("app5"):
                app5_url = pickle.load(open("app5",'rb'))
                app_icon = QFileIconProvider().icon(QFileInfo(app5_url))
                self.app5_img.setIcon(app_icon)
        else:
                app_icon = QFileIconProvider().icon(QFileInfo("resources/empty.ico"))
                self.app5_img.setIcon(app_icon)

        self.app5_img.clicked.connect(self.appfive_openFileNameDialog)
        self.app5_img.setObjectName("app5_img")
        
        self.app4_img = QtWidgets.QPushButton(self.app_frame)
        self.app4_img.setGeometry(QtCore.QRect(170, 40, 17, 17))
        if os.path.isfile("app4"):
                app4_url = pickle.load(open("app4",'rb'))
                app_icon = QFileIconProvider().icon(QFileInfo(app4_url))
                self.app4_img.setIcon(app_icon)
        else:
                app_icon = QFileIconProvider().icon(QFileInfo("resources/empty.ico"))
                self.app4_img.setIcon(app_icon)

        self.app4_img.clicked.connect(self.appfour_openFileNameDialog)
        self.app4_img.setObjectName("app4_img")
        
        self.app3_img = QtWidgets.QPushButton(self.app_frame)
        self.app3_img.setGeometry(QtCore.QRect(130, 40, 17, 17))
        if os.path.isfile("app3"):
                app3_url = pickle.load(open("app3",'rb'))
                app_icon = QFileIconProvider().icon(QFileInfo(app3_url))
                self.app3_img.setIcon(app_icon)
        else:
                app_icon = QFileIconProvider().icon(QFileInfo("resources/empty.ico"))
                self.app3_img.setIcon(app_icon)

        self.app3_img.clicked.connect(self.appthree_openFileNameDialog)

        self.app3_img.setObjectName("app3_img")
        
        self.app2_img = QtWidgets.QPushButton(self.app_frame)
        self.app2_img.setGeometry(QtCore.QRect(90, 40, 17, 17))
        if os.path.isfile("app2"):
                app2_url = pickle.load(open("app2",'rb'))
                app_icon = QFileIconProvider().icon(QFileInfo(app2_url))
                self.app2_img.setIcon(app_icon)
        else:
                app_icon = QFileIconProvider().icon(QFileInfo("resources/empty.ico"))
                self.app2_img.setIcon(app_icon)

        self.app2_img.clicked.connect(self.apptwo_openFileNameDialog)
        self.app2_img.setObjectName("app2_img")
        
        self.app1_img = QtWidgets.QPushButton(self.app_frame)
        self.app1_img.setGeometry(QtCore.QRect(50, 40, 17, 17))
        if os.path.isfile("app1"):
                app1_url = pickle.load(open("app1",'rb'))
                app_icon = QFileIconProvider().icon(QFileInfo(app1_url))
                self.app1_img.setIcon(app_icon)
        else:
                app_icon = QFileIconProvider().icon(QFileInfo("resources/empty.ico"))
                self.app1_img.setIcon(app_icon)

        self.app1_img.clicked.connect(self.appone_openFileNameDialog)
        self.app1_img.setObjectName("app1_img")
        
        self.mot_img_line = QtWidgets.QFrame(self.background)
        self.mot_img_line.setGeometry(QtCore.QRect(0, 170, 280, 2))
        self.mot_img_line.setStyleSheet("background-color: rgb(255, 255, 255);z")
        self.mot_img_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.mot_img_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.mot_img_line.setObjectName("mot_img_line")
        
        self.power_frame = QtWidgets.QFrame(self.background)
        self.power_frame.setGeometry(QtCore.QRect(0, 290, 55, height - 290))
        self.power_frame.setStyleSheet("background-color: rgb(21, 21, 21);")
        self.power_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.power_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.power_frame.setObjectName("power_frame")
        
        self.fb_btn = QtWidgets.QPushButton(self.power_frame)
        self.fb_btn.setGeometry(QtCore.QRect(17,42, 17, 17))
        self.fb_btn.setStyleSheet("border-image : url(resources/facebook.png);\n"
"background-repeat: no-repeat;")
        self.fb_btn.setText("")
        self.fb_btn.clicked.connect(self.loadfb)
        self.fb_btn.setObjectName("fb_btn")
        
        self.yt_btn = QtWidgets.QPushButton(self.power_frame)
        self.yt_btn.setGeometry(QtCore.QRect(17,82, 17, 17))
        self.yt_btn.setStyleSheet("border-image : url(resources/youtube.png);\n"
"background-repeat: no-repeat;")
        self.yt_btn.setText("")
        self.yt_btn.clicked.connect(self.loadyt)
        self.yt_btn.setObjectName("yt_btn")
        
        self.tw_btn = QtWidgets.QPushButton(self.power_frame)
        self.tw_btn.setGeometry(QtCore.QRect(17,122, 17, 17))
        self.tw_btn.setStyleSheet("border-image : url(resources/twitter.png);\n"
"background-repeat: no-repeat;")
        self.tw_btn.setText("")
        self.tw_btn.clicked.connect(self.loadtw)
        self.tw_btn.setObjectName("tw_btn")
        
        self.pn_btn = QtWidgets.QPushButton(self.power_frame)
        self.pn_btn.setGeometry(QtCore.QRect(17,162, 17, 17))
        self.pn_btn.setStyleSheet("border-image : url(resources/pinterest.png);\n"
"background-repeat: no-repeat;")
        self.pn_btn.setText("")
        self.pn_btn.clicked.connect(self.loadpn)
        self.pn_btn.setObjectName("pn_btn")
        
        self.nx_btn = QtWidgets.QPushButton(self.power_frame)
        self.nx_btn.setGeometry(QtCore.QRect(17,202, 17, 17))
        self.nx_btn.setStyleSheet("border-image : url(resources/nexina.png);\n"
"background-repeat: no-repeat;")
        self.nx_btn.setText("")
        self.nx_btn.clicked.connect(self.loadnx)
        self.nx_btn.setObjectName("nx_btn")
        
        self.shutdown_btn = QtWidgets.QPushButton(self.power_frame)
        self.shutdown_btn.setGeometry(QtCore.QRect(17,self.power_frame.frameGeometry().height() - 72, 20, 20))
        self.shutdown_btn.setStyleSheet("border-image : url(resources/shutdown.png);\n"
"background-repeat: no-repeat;")
        self.shutdown_btn.setText("")
        self.shutdown_btn.clicked.connect(self.shutdown)
        self.shutdown_btn.setObjectName("shutdown_btn")
        
        self.reboot_btn = QtWidgets.QPushButton(self.power_frame)
        self.reboot_btn.setGeometry(QtCore.QRect(17, self.power_frame.frameGeometry().height() - 128, 20, 20))
        self.reboot_btn.setStyleSheet("border-image : url(resources/reboot.png);\n"
"background-repeat: no-repeat;")
        self.reboot_btn.setText("")
        self.reboot_btn.clicked.connect(self.reboot)
        self.reboot_btn.setObjectName("reboot_btn")
        
        self.hibernate_btn = QtWidgets.QPushButton(self.power_frame)
        self.hibernate_btn.setGeometry(QtCore.QRect(17, self.power_frame.frameGeometry().height() - 182, 20, 20))
        self.hibernate_btn.setStyleSheet("border-image : url(resources/hibernate.png);\n"
"background-repeat: no-repeat;")
        self.hibernate_btn.setText("")
        self.hibernate_btn.clicked.connect(self.hibernate)
        self.hibernate_btn.setObjectName("hibernate_btn")
        
        self.status_frame = QtWidgets.QFrame(self.background)
        self.status_frame.setGeometry(QtCore.QRect(50, height - 80, 231, 38))
        self.status_frame.setStyleSheet("background-color: rgb(82, 82, 82);")
        self.status_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.status_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.status_frame.setObjectName("status_frame")
        
        self.wifi = QtWidgets.QFrame(self.status_frame)
        self.wifi.setGeometry(QtCore.QRect(28, 10, 17, 17))
        self.wifi.setStyleSheet("border-image : url(resources/no_wifi.png);\n"
"background-repeat: no-repeat;")
        self.wifi.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.wifi.setFrameShadow(QtWidgets.QFrame.Raised)
        self.wifi.setObjectName("wifi")
        
        self.internet = QtWidgets.QFrame(self.status_frame)
        self.internet.setGeometry(QtCore.QRect(78, 10, 17, 17))
        self.internet.setStyleSheet("border-image : url(resources/no_internet.png);\n"
"background-repeat: no-repeat;")
        self.internet.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.internet.setFrameShadow(QtWidgets.QFrame.Raised)
        self.internet.setObjectName("internet")
        
        self.bluetooth = QtWidgets.QFrame(self.status_frame)
        self.bluetooth.setGeometry(QtCore.QRect(128, 10, 17, 17))
        self.bluetooth.setStyleSheet("border-image : url(resources/no_bluetooth.png);\n"
"background-repeat: no-repeat;")
        self.bluetooth.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bluetooth.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bluetooth.setObjectName("bluetooth")
        
        self.ethernet = QtWidgets.QFrame(self.status_frame)
        self.ethernet.setGeometry(QtCore.QRect(178, 10, 17, 17))
        self.ethernet.setStyleSheet("border-image : url(resources/no_ethernet.png);\n"
"background-repeat: no-repeat;")
        self.ethernet.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ethernet.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ethernet.setObjectName("ethernet")
        
        self.pp_frame = QtWidgets.QFrame(self.background)
        self.pp_frame.setGeometry(QtCore.QRect(220, 145, 50, 50))
        self.pp_frame.setStyleSheet("\n"
"background-repeat: no-repeat;\n"
"border-radius:25px;\n"
"border: 3px solid white")
        self.pp_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pp_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pp_frame.setObjectName("pp_frame")
        
        self.usr_pic = QtWidgets.QFrame(self.pp_frame)
        self.usr_pic.setGeometry(QtCore.QRect(0, 0, 50, 50))
        self.usr_pic.setStyleSheet("border-image : url(resources/default.png);\n"
"background-repeat: no-repeat;")
        self.usr_pic.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.usr_pic.setFrameShadow(QtWidgets.QFrame.Raised)
        self.usr_pic.setObjectName("usr_pic")
        
        self.clock_frame = QtWidgets.QFrame(self.background)
        self.clock_frame.setGeometry(QtCore.QRect(0, 0, 280, 171))
        self.clock_frame.setStyleSheet("border-image : url(resources/pic1.jpg);\n"
"background-repeat: no-repeat;")
        self.clock_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.clock_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.clock_frame.setObjectName("clock_frame")
        
        self.time_label = QtWidgets.QLabel(self.clock_frame)
        self.time_label.setGeometry(QtCore.QRect(15, 108, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.time_label.setFont(font)
        self.time_label.setStyleSheet("QLabel{\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"    border-image : none;\n"
"    background-repeat: no-repeat;font-family:Roboto-Regular;\n"
"}")
        self.time_label.setScaledContents(True)
        self.time_label.setWordWrap(True)
        self.time_label.setObjectName("time_label")
        
        self.date_label = QtWidgets.QLabel(self.clock_frame)
        self.date_label.setGeometry(QtCore.QRect(20, 140, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.date_label.setFont(font)
        self.date_label.setStyleSheet("QLabel{\n"
"    color: rgb(255, 255, 255);font-family:Roboto-Regular;\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"    border-image : none;\n"
"    background-repeat: no-repeat;\n"
"}")
        self.date_label.setScaledContents(True)
        self.date_label.setWordWrap(True)
        self.date_label.setObjectName("date_label")
        
        self.royal_frame = QtWidgets.QFrame(self.clock_frame)
        self.royal_frame.setGeometry(QtCore.QRect(179, 10, 101, 25))
        self.royal_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 187, 0, 255), stop:1 rgba(255, 117, 0, 255));\n"
"border-image : NONE;\n"
"background-repeat: no-repeat;")
        self.royal_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.royal_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.royal_frame.setObjectName("royal_frame")
        
        self.join_royal_lbl = QtWidgets.QLabel(self.royal_frame)
        self.join_royal_lbl.setGeometry(QtCore.QRect(20, 0, 81, 25))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        font.setWeight(75)
        self.join_royal_lbl.setFont(font)
        self.join_royal_lbl.setStyleSheet("color: rgb(255, 255, 255);font-family:Roboto-Regular;")
        self.join_royal_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.join_royal_lbl.setObjectName("join_royal_lbl")
        
        self.royal_icn = QtWidgets.QLabel(self.royal_frame)
        self.royal_icn.setGeometry(QtCore.QRect(8, 5, 13, 13))
        self.royal_icn.setStyleSheet("border-image : url(resources/internet_avail.png);\n"
"background-repeat: no-repeat;")
        self.royal_icn.setText("")
        self.royal_icn.setObjectName("royal_icn")
        
        self.notice_frame = QtWidgets.QFrame(self.background)
        self.notice_frame.setGeometry(QtCore.QRect(80, height - 130, 201, 31))
        self.notice_frame.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(226, 166, 0, 255), stop:1 rgba(165, 76, 0, 255));")
        self.notice_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.notice_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.notice_frame.setObjectName("notice_frame")
        
        self.alert_no = QtWidgets.QLabel(self.notice_frame)
        self.alert_no.setGeometry(QtCore.QRect(10, 10, 13, 13))
        self.alert_no.setStyleSheet("border-image : url(resources/crown.png);background-repeat: no-repeat;background-color:transparent")
        self.alert_no.setObjectName("alert_no")
        
        self.open_notice = QtWidgets.QPushButton(self.notice_frame)
        self.open_notice.setGeometry(QtCore.QRect(40, 0, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(7)
        self.open_notice.setFont(font)
        self.open_notice.setStyleSheet("color: rgb(255, 255, 255);font-family:Roboto-Regular;")
        self.open_notice.setFlat(True)
        self.open_notice.setObjectName("open_notice")
        self.open_notice.setText("OMNI PROJECTS")
        self.open_notice.clicked.connect(self.loadurl)
        
        self.control_frame = QtWidgets.QFrame(self.background)
        self.control_frame.setGeometry(QtCore.QRect(79, height - 225, 201, 91))
        self.control_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.control_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.control_frame.setObjectName("control_frame")
        
        self.vol_img = QtWidgets.QLabel(self.control_frame)
        self.vol_img.setGeometry(QtCore.QRect(20, 13, 17, 17))
        self.vol_img.setStyleSheet("border-image : url(resources/volume.png);\n"
"background-repeat: no-repeat;")
        self.vol_img.setText("")
        self.vol_img.setObjectName("vol_img")
        
        self.bright_img = QtWidgets.QLabel(self.control_frame)
        self.bright_img.setGeometry(QtCore.QRect(20, 53, 17, 17))
        self.bright_img.setStyleSheet("border-image : url(resources/brightness.png);\n"
"background-repeat: no-repeat;")
        self.bright_img.setText("")
        self.bright_img.setObjectName("bright_img")
        
        self.vol_0_btn = QtWidgets.QPushButton(self.control_frame)
        self.vol_0_btn.setGeometry(QtCore.QRect(45, 10, 31, 23))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(6)
        self.vol_0_btn.setFont(font)
        self.vol_0_btn.setStyleSheet("background-color:transparent;\n"
"color:white")
        self.vol_0_btn.setFlat(True)
        self.vol_0_btn.setObjectName("vol_0_btn")
        self.vol_0_btn.clicked.connect(lambda: self.volumevaluechange(-60.0))
        
        self.vol_25_btn = QtWidgets.QPushButton(self.control_frame)
        self.vol_25_btn.setGeometry(QtCore.QRect(80, 10, 31, 23))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(6)
        self.vol_25_btn.setFont(font)
        self.vol_25_btn.setStyleSheet("background-color:transparent;\n"
"color:white")
        self.vol_25_btn.setFlat(True)
        self.vol_25_btn.clicked.connect(lambda: self.volumevaluechange(-30.0))
        self.vol_25_btn.setObjectName("vol_25_btn")
        
        self.vol_50_btn = QtWidgets.QPushButton(self.control_frame)
        self.vol_50_btn.setGeometry(QtCore.QRect(115, 10, 31, 23))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(6)
        self.vol_50_btn.setFont(font)
        self.vol_50_btn.setStyleSheet("background-color:transparent;\n"
"color:white")
        self.vol_50_btn.setFlat(True)
        self.vol_50_btn.clicked.connect(lambda: self.volumevaluechange(-15.0))
        self.vol_50_btn.setObjectName("vol_50_btn")
        
        self.vol_100_btn = QtWidgets.QPushButton(self.control_frame)
        self.vol_100_btn.setGeometry(QtCore.QRect(150, 10, 31, 23))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(6)
        self.vol_100_btn.setFont(font)
        self.vol_100_btn.setStyleSheet("background-color:transparent;\n"
"color:white")
        self.vol_100_btn.setFlat(True)
        self.vol_100_btn.clicked.connect(lambda: self.volumevaluechange(0.0))
        self.vol_100_btn.setObjectName("vol_100_btn")
        
        self.bright_100_btn = QtWidgets.QPushButton(self.control_frame)
        self.bright_100_btn.setGeometry(QtCore.QRect(150, 50, 31, 23))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(6)
        self.bright_100_btn.setFont(font)
        self.bright_100_btn.setStyleSheet("background-color:transparent;\n"
"color:white")
        self.bright_100_btn.setFlat(True)
        self.bright_100_btn.setObjectName("bright_100_btn")
        self.bright_100_btn.clicked.connect(lambda : self.brightnessvaluechange(100))
        self.bright_0_btn = QtWidgets.QPushButton(self.control_frame)
        self.bright_0_btn.setGeometry(QtCore.QRect(45, 50, 31, 23))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(6)
        self.bright_0_btn.setFont(font)
        self.bright_0_btn.setStyleSheet("background-color:transparent;\n"
"color:white")
        self.bright_0_btn.setFlat(True)
        self.bright_0_btn.clicked.connect(lambda : self.brightnessvaluechange(0))
        self.bright_0_btn.setObjectName("bright_0_btn")
        
        self.bright_25_btn = QtWidgets.QPushButton(self.control_frame)
        self.bright_25_btn.setGeometry(QtCore.QRect(80, 50, 31, 23))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(6)
        self.bright_25_btn.setFont(font)
        self.bright_25_btn.setStyleSheet("background-color:transparent;\n"
"color:white")
        self.bright_25_btn.setFlat(True)
        self.bright_25_btn.clicked.connect(lambda : self.brightnessvaluechange(25))
        self.bright_25_btn.setObjectName("bright_25_btn")
        
        self.bright_50_btn = QtWidgets.QPushButton(self.control_frame)
        self.bright_50_btn.setGeometry(QtCore.QRect(115, 50, 31, 23))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(6)
        self.bright_50_btn.setFont(font)
        self.bright_50_btn.setStyleSheet("background-color:transparent;\n"
"color:white")
        self.bright_50_btn.setFlat(True)
        self.bright_50_btn.clicked.connect(lambda : self.brightnessvaluechange(50))
        self.bright_50_btn.setObjectName("bright_50_btn")
        
        self.quote_frame = QtWidgets.QFrame(self.background)
        self.quote_frame.setGeometry(QtCore.QRect(0, 250, 281, 41))
        self.quote_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.quote_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.quote_frame.setStyleSheet("QFrame{\n"
"    color: rgb(255, 255, 255);\n"
"    \n"
"    background-color: rgb(37, 37, 37);\n"
"}")
        self.quote_frame.setObjectName("quote_frame")
        
        self.quote_label = QtWidgets.QLabel(self.quote_frame)
        self.quote_label.setGeometry(QtCore.QRect(-10, 0, 291, 41))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(8)
        self.quote_label.setFont(font)
        self.quote_label.setScaledContents(True)
        self.quote_label.setAlignment(QtCore.Qt.AlignCenter)
        self.quote_label.setWordWrap(False)
        self.quote_label.setStyleSheet("font-family:Roboto-Regular;")
        self.quote_label.enemyAnimation = QtCore.QSequentialAnimationGroup()
        first = QtCore.QPropertyAnimation(self.quote_label, b'pos')
        first.setEndValue(QtCore.QPoint(-380, 0))
        first.setDuration(10000)
        second = QtCore.QPropertyAnimation(self.quote_label, b'pos')
        second.setEndValue(QtCore.QPoint(0, 0))
        second.setDuration(10000)
        self.quote_label.enemyAnimation.addAnimation(first)
        self.quote_label.enemyAnimation.addAnimation(second)
        self.quote_label.enemyAnimation.setLoopCount(-1)
        self.quote_label.enemyAnimation.start()
        if IPaddress!="127.0.0.1":
                quote_text = "Know Thyself"
                _translate = QtCore.QCoreApplication.translate
                self.quote_label.setText(_translate("main", quote_text))
                self.internet.setStyleSheet("#internet{border-image : url(resources/internet_avail.png);background-repeat: no-repeat;}")
        else:
                _translate = QtCore.QCoreApplication.translate
                self.internet.setStyleSheet("#internet{border-image : url(resources/no_internet.png);background-repeat: no-repeat;}")
                self.quote_label.setText(_translate("main","Know Thyself"))

        self.quote_label.setObjectName("quote_label")
        
        self.quote_top_right_line = QtWidgets.QFrame(self.quote_frame)
        self.quote_top_right_line.setGeometry(QtCore.QRect(160, 0, 118, 1))
        self.quote_top_right_line.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.quote_top_right_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.quote_top_right_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.quote_top_right_line.setObjectName("quote_top_right_line")
        
        self.quote_bottom_left_line = QtWidgets.QFrame(self.quote_frame)
        self.quote_bottom_left_line.setGeometry(QtCore.QRect(0, 40, 118, 1))
        self.quote_bottom_left_line.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.quote_bottom_left_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.quote_bottom_left_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.quote_bottom_left_line.setObjectName("quote_bottom_left_line")
        
        self.update_btn = QtWidgets.QPushButton(self.background)
        self.update_btn.setGeometry(QtCore.QRect(60, height -28, 117, 17))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        font.setWeight(15)
        self.update_btn.setFont(font)
        self.update_btn.setStyleSheet("color: rgb(255, 197, 21);font-family:Roboto-Regular;")
        self.update_btn.setFlat(True)
        self.update_btn.clicked.connect(self.loadurl)
        self.update_btn.setObjectName("update_btn")
        
        self.hover_widget = QtWidgets.QPushButton(self.background)
        self.hover_widget.setGeometry(QtCore.QRect(170, height -35, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setBold(True)
        font.setWeight(75)
        self.hover_widget.setFont(font)
        self.hover_widget.setStyleSheet("color: rgb(255, 255, 255);font-family:Roboto-Regular;")
        self.hover_widget.setFlat(True)
        self.hover_widget.clicked.connect(self.hwgit)
        self.hover_widget.setObjectName("hover_widget")
        
        self.status_frame.raise_()
        self.power_frame.raise_()
        self.cpu_ram_frame.raise_()
        self.note_frame.raise_()
        self.app_frame.raise_()
        self.mot_img_line.raise_()
        self.clock_frame.raise_()
        self.pp_frame.raise_()
        self.notice_frame.raise_()
        self.control_frame.raise_()
        self.quote_frame.raise_()
        self.hover_widget.raise_()
        main.setCentralWidget(self.centralwidget)

        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate("main", "main"))
        self.ram_label.setText(_translate("main", "RAM"))
        self.cpu_label.setText(_translate("main", "CPU"))
        self.note_label.setText(_translate("main", "Notes"))
        self.apps_label.setText(_translate("main", "Apps"))
        self.time_label.setText(_translate("main", "12 : 00 pm"))
        self.date_label.setText(_translate("main", datetime.now().strftime('%d %B %Y')))
        self.join_royal_lbl.setText(_translate("main", "SUPPORT US"))
        self.alert_no.setText(_translate("main", ""))
        self.vol_0_btn.setText(_translate("main", "0%"))
        self.vol_25_btn.setText(_translate("main", "25%"))
        self.vol_50_btn.setText(_translate("main", "50%"))
        self.vol_100_btn.setText(_translate("main", "100%"))
        self.bright_100_btn.setText(_translate("main", "100%"))
        self.bright_0_btn.setText(_translate("main", "0%"))
        self.bright_25_btn.setText(_translate("main", "25%"))
        self.bright_50_btn.setText(_translate("main", "50%"))
        IPaddress=socket.gethostbyname(socket.gethostname())
        if IPaddress!="127.0.0.1":
                quote_text = "Know Thyself"
                try:
                        self.quote_label.setText(_translate("main", quote_text))
                except ValueError:
                        self.quote_label.setText(_translate("main","Know Thyself"))

        else:
                self.quote_label.setText(_translate("main","Know Thyself"))
                self.open_notice.setText(_translate("main", "No Notice Available"))
                
        self.update_btn.setText(_translate("main", "UPDATE AVAILABLE !"))
        self.hover_widget.setText(_translate("main", "HOVER BOARD"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = QtWidgets.QMainWindow()
    ui = Ui_main()
    ui.setupUi(main)
    main.show()
    sys.exit(app.exec_())
