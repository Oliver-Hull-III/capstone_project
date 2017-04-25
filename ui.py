from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
az_step = 40
az_direction = 38
el_step = 37
el_direction = 35


GPIO.setup(az_step, GPIO.OUT)
GPIO.setup(az_direction, GPIO.OUT)
GPIO.setup(el_step, GPIO.OUT)
GPIO.setup(el_direction, GPIO.OUT)



class Button(QtGui.QPushButton):
    def __init__(self, *args, **kwargs):
        QtGui.QPushButton.__init__(self, *args, **kwargs)
        self.setAutoRepeat(True)
        self.setAutoRepeatInterval(100) #change value to set speed 
        self.clicked.connect(self.handleClicked)
        self._state = 0
        self.direction = args[0]


    def handleClicked(self):
        if self.isDown():
            if self._state == 0:
                self._state = 1
                self.setAutoRepeatInterval(10)
                if(self.direction is '^'):
                    GPIO.output(el_direction, GPIO.LOW)
                    
                elif(self.direction is 'v'):
                    GPIO.output(el_direction, GPIO.HIGH)

                elif(self.direction is '<'):
                    GPIO.output(az_direction, GPIO.HIGH)

                elif(self.direction is '>'):
                    GPIO.output(az_direction, GPIO.LOW)
                    

                
            else:
                self.setAutoRepeatInterval(4)
                for i in range(0,10):
                    if(self.direction is 'v' or self.direction is '^'):
                        GPIO.output(el_step, GPIO.HIGH)
                        sleep(.001)
                        GPIO.output(el_step, GPIO.LOW)
                    else:
                        GPIO.output(az_step, GPIO.HIGH)
                        sleep(.001)
                        GPIO.output(az_step, GPIO.LOW)
     
                
        elif self._state == 1:
            self._state = 0
            self.setAutoRepeatInterval(10)
            print 'released'
        else:
            if(self.direction is '^'):
                GPIO.output(el_direction, GPIO.HIGH)
                GPIO.output(el_step, GPIO.HIGH)
                sleep(.001)
                GPIO.output(el_step, GPIO.LOW)

                
            elif(self.direction is 'v'):
                GPIO.output(el_direction, GPIO.LOW)
                GPIO.output(el_step, GPIO.HIGH)
                sleep(.001)
                GPIO.output(el_step, GPIO.LOW)



            elif(self.direction is '<'):
                GPIO.output(az_direction, GPIO.HIGH)
                GPIO.output(az_step, GPIO.HIGH)
                sleep(.001)
                GPIO.output(az_step, GPIO.LOW)


            elif(self.direction is '>'):
                GPIO.output(az_direction, GPIO.LOW)

                GPIO.output(az_step, GPIO.HIGH)
                sleep(.001)
                GPIO.output(az_step, GPIO.LOW)
    


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.videoFrame = QtGui.QLabel(self.centralwidget)
        self.videoFrame.setGeometry(QtCore.QRect(80, 0, 640, 480))
        self.videoFrame.setObjectName(_fromUtf8("videoFrame"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.tracking = False
 
        self.leftButton =Button('<',MainWindow)
        self.leftButton.setGeometry(QtCore.QRect(620, 430,50,30))
        self.leftButton.setObjectName(_fromUtf8("leftButton"))

        self.downButton = Button('v',MainWindow)
        self.downButton.setGeometry(QtCore.QRect(675, 430,50,30))
        self.downButton.setObjectName(_fromUtf8("downButton"))
        
        self.rightButton = Button('>',MainWindow)
        self.rightButton.setGeometry(QtCore.QRect(730, 430,50,30))
        self.rightButton.setObjectName(_fromUtf8("rightButton"))


        self.upButton = Button('^',MainWindow)
        self.upButton.setGeometry(QtCore.QRect(675, 395,50,30))
        self.upButton.setObjectName(_fromUtf8("upButton"))                


        self.trackingButton = QtGui.QPushButton('Start\nTracking',MainWindow)
        self.trackingButton.clicked.connect(self.startTracking)
        self.trackingButton.setGeometry(QtCore.QRect(20,400,80,60))
        self.trackingButton.setObjectName(_fromUtf8("trackingButton"))
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.videoFrame.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))


   

    def startTracking(self, MainWindow):
        if self.tracking:
            self.trackingButton.setText("Stop\nTracking")
            self.trackingButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
            self.tracking = False
            self.MainWindow.startTracking()
        else:
            self.trackingButton.setText("Start\nTracking")
            self.trackingButton.setStyleSheet('')
            self.tracking = True
            self.MainWindow.stopTracking()

