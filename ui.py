from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
from time import sleep




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
                self.setAutoRepeatInterval(10) 


                print 'pressed'
            else:
                self.setAutoRepeatInterval(1) 
                print 'sent signal to motor'
                
        elif self._state == 1:
            self._state = 0
            self.setAutoRepeatInterval(10)
            print 'released'
        else:
            print 'click'



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
 
        self.leftButton = QtGui.QPushButton('<-',MainWindow)
        self.leftButton.clicked.connect(self.left)
        self.leftButton.setGeometry(QtCore.QRect(620, 430,50,30))
        self.leftButton.setObjectName(_fromUtf8("leftButton"))

        self.downButton = QtGui.QPushButton('v',MainWindow)
        self.downButton.clicked.connect(self.down)
        self.downButton.setGeometry(QtCore.QRect(675, 430,50,30))
        self.downButton.setObjectName(_fromUtf8("downButton"))
        
        self.rightButton = QtGui.QPushButton('->',MainWindow)
        self.rightButton.clicked.connect(self.right)
        self.rightButton.setGeometry(QtCore.QRect(730, 430,50,30))
        self.rightButton.setObjectName(_fromUtf8("rightButton"))


        self.upButton = Button('^',MainWindow)
        self.upButton.setGeometry(QtCore.QRect(675, 395,50,30))
        self.upButton.setObjectName(_fromUtf8("upButton"))                


        self.trackingButton = QtGui.QPushButton('Start\nTracking',MainWindow)
        self.trackingButton.clicked.connect(self.startTracking)
        self.trackingButton.setGeometry(QtCore.QRect(20,400,80,60))
        self.trackingButton.setObjectName(_fromUtf8("trackingButton"))

        #self.quitButton = QtGui.QPushButton('Quit',MainWindow)
        #self.quitButton.clicked.connect(self.quit)
        #self.quitButton.setGeometry(QtCore.QRect(20,355,40,40))
        #self.quitButton.setObjectName(_fromUtf8("quitButton"))
        
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
        print("d")
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

