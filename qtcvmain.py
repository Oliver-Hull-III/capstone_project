import sys
import cv2
import numpy as np
from PyQt4 import QtGui, QtCore, Qt
from gui.ui import Ui_MainWindow
import opencv_stuff.video as video
import mossetest as mosse
import RPi.GPIO as GPIO
import time
import pidController as pid
from PIGPIO import pigpio

step = 29
direction = 31
MS1 = 33
MS2 = 35
enable = 37



 
class Gui(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)

        args = sys.argv

        self.pid = pid.pid(args[1],args[2],args[3])
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
        freq = self.pid.update(abs(self.tracker.pos[0]-self.x0))

        #create sq wave w/ freq
        #GPIO = 21
        #square = []

        #period = freq

        #                           ON      OFF         TIME
        #square.append(pigpio.pulse(1<<GPIO, 0, period/2))
        #square.append(pigpio.pulse(0, 1<<GPIO, period/2))

#        pi = pigpio.pi()
#        pi.set_mode(GPIO, pigpio.OUTPUT)
#        pi.wave_add_generic(square)

#        wid = pi.wave_create()

#        if wid >= 0:
#            pi.wave_send_repeat(wid)
#            time.sleep(60)
#            pi.wave_tx_stop()
#            pi.wave_delete(wid)

#        pi.stop()
        
        #if(abs(self.tracker.pos[0]-self.x0) > 40):



        """     converts frame to format suitable for QtGui            """

        
        self.currentFrame=cv2.cvtColor(vis,cv2.COLOR_BGR2RGB)
        self.height,self.width=self.currentFrame.shape[:2]
        img=QtGui.QImage(self.currentFrame,self.width,self.height,QtGui.QImage.Format_RGB888)
        img=QtGui.QPixmap.fromImage(img)
        self.ui.videoFrame.setPixmap(img)
        self.ui.videoFrame.setScaledContents(True)


 
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    ex.show()
#   ex.showFullScreen()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()
