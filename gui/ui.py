from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
import RPi.GPIO as GPIO
from time import sleep


step = 29
direction = 31
MS1 = 33
MS2 = 35
enable = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setup(step, GPIO.OUT)
GPIO.setup(direction, GPIO.OUT)
GPIO.setup(MS1, GPIO.OUT)
GPIO.setup(MS2, GPIO.OUT)
GPIO.setup(enable, GPIO.OUT)
GPIO.output(enable, GPIO.LOW)
GPIO.output(MS1, GPIO.LOW)
GPIO.output(MS2, GPIO.LOW)



class Button(QtGui.QPushButton):
    def __init__(self, *args, **kwargs):
        QtGui.QPushButton.__init__(self, *args, **kwargs)
        self.setAutoRepeat(True)
        self.setAutoRepeatInterval(100) #change value to set speed 
        self.clicked.connect(self.handleClicked)
        self._state = 0

    def handleClicked(self):
        if self.isDown():
            if self._state == 0:
                self._state = 1
                self.setAutoRepeatInterval(100) 


                print 'pressed'
            else:
                print 'sent signal to motor'
                self.xForward()

        elif self._state == 1:
            self._state = 0
            self.setAutoRepeatInterval(100)
            print 'released'
        else:
            print 'click'

    def xForward(self):
        GPIO.output(direction, GPIO.LOW)
        sleep(0.001)
        GPIO.output(step, GPIO.HIGH)
        sleep(0.001)
        GPIO.output(step, GPIO.LOW)
        sleep(0.001)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 500)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.videoFrame = QtGui.QLabel(self.centralwidget)
        self.videoFrame.setGeometry(QtCore.QRect(0, 0, 800, 500))
        self.videoFrame.setObjectName(_fromUtf8("videoFrame"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.leftButton = QtGui.QPushButton('<-',MainWindow)
        self.leftButton.clicked.connect(self.left)
        self.leftButton.setGeometry(QtCore.QRect(600, 390,50,30))
        self.leftButton.setObjectName(_fromUtf8("leftButton"))

        self.downButton = QtGui.QPushButton('v',MainWindow)
        self.downButton.clicked.connect(self.down)
        self.downButton.setGeometry(QtCore.QRect(655, 390,50,30))
        self.downButton.setObjectName(_fromUtf8("downButton"))
        
        self.rightButton = QtGui.QPushButton('->',MainWindow)
        self.rightButton.clicked.connect(self.right)
        self.rightButton.setGeometry(QtCore.QRect(710, 390,50,30))
        self.rightButton.setObjectName(_fromUtf8("rightButton"))


        self.upButton = Button('^',MainWindow)
        self.upButton.setGeometry(QtCore.QRect(655, 350,50,30))
        self.upButton.setObjectName(_fromUtf8("upButton"))                


        self.trackingButton = QtGui.QPushButton('Start\nTracking',MainWindow)
        self.trackingButton.clicked.connect(self.startTracking)
        self.trackingButton.setGeometry(QtCore.QRect(40,350,70,60))
        self.trackingButton.setObjectName(_fromUtf8("trackingButton"))

        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.videoFrame.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))


    def left(self, MainWindow):
        print("left")

    def right(self, MainWindow):
        print("right")

    def up(self, MainWindow):
        print("up")

    def down(self, MainWindow):
        print("down")

    def startTracking(self, MainWindow):
        print("tracking")
