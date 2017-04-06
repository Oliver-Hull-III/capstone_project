import sys,os,time,signal
import cv2
import numpy as np
from PyQt4 import QtGui, QtCore, Qt
from gui.ui import Ui_MainWindow
import opencv_stuff.video as video
import mossetest as mosse
import pidController as pid
import thread
from time import sleep
import squareWave


xError = 0
yError = 0
xFrequency = 0
yFrequency = 0


def generateWave(isX):
    sq = squareWave.squareWave(isX)
    while(1):
        if(xFrequency!=0):
            sq.run(xFrequency)

    

def updatePid(isX):
    controller = pid.pid(sys.argv[1],sys.argv[2],sys.argv[3])
    while(1):
        if(isX):
            global xFrequency
            err = xError
            xFrequency = controller.update(err)

        else:
            global yFrequency
            err = yError
            yFrequency = controller.update(err)
        sleep(5)
            
class Gui(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

        self.cap = video.create_capture()
        _, self.frame = self.cap.read()
        self.currentFrame=np.array([])
        
        self.x0 = int(self.cap.get(3) / 2)
        self.y0 = int(self.cap.get(4) / 2)
        
        frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.tracker = mosse.MOSSE(frame_gray, (self.x0-40,self.y0-40,self.x0+40,self.y0+40))
   






        self.ui = Ui_MainWindow()
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.black)

        self.setPalette(palette)

        self.ui.setupUi(self)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(27)
        self.update()

        
 
    def play(self):
        ret, self.frame=self.cap.read()
        frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.tracker.update(frame_gray)


        vis = self.frame.copy()

        if(self.tracker.pos[0]-self.x0):
            direction = 0
        else:
            direction = 1
        
        self.tracker.draw_state(vis)
        global xError
        global yError

        xError = self.tracker.pos[0] - self.x0 
        yError = self.tracker.pos[1] - self.y0


        """     converts frame to format suitable for QtGui            """

        
        self.currentFrame=cv2.cvtColor(vis,cv2.COLOR_BGR2RGB)
        self.height,self.width=self.currentFrame.shape[:2]
        img=QtGui.QImage(self.currentFrame,self.width,self.height,QtGui.QImage.Format_RGB888)
        img=QtGui.QPixmap.fromImage(img)
        self.ui.videoFrame.setPixmap(img)
        self.ui.videoFrame.setScaledContents(True)


 
def main():
    
    args = sys.argv
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    ex.show()
#   ex.showFullScreen()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    thread.start_new_thread(updatePid, (True,))
    #thread.start_new_thread(updatePid, (False,))
    thread.start_new_thread(generateWave, (True,))    
    

    sys.exit(app.exec_())

         
if __name__ == '__main__':
    main()
