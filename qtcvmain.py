import sys
import cv2
import numpy as np
from PyQt4 import QtGui, QtCore, Qt
from gui.ui import Ui_MainWindow
import opencv_stuff.video as video
import mossetest as mosse


#D:\vbshare\Codes\opencv\qtcvpy>D:\vbshare\Python27\Lib\site-packages\PyQt4\pyuic4.bat mainWindow.ui -o ui.py
#http://wrdeoftheday.com/?page_id=2




            
 
class Gui(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)


        self.cap = video.create_capture()
        _, self.frame = self.cap.read()
        self.width = self.cap.get(3)
        self.height = self.cap.get(4)
        self.currentFrame=np.array([])
        x0 = int((self.width/2)-40)
        y0 = int((self.height/2)-40)
        x1 = int((self.width/2)+40)
        y1 = int((self.height/2)+40)
        
        frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.tracker = mosse.MOSSE(frame_gray, (x0,y0,x1,y1))
     






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

        self.tracker.draw_state(vis)


    


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
    #ex.showFullScreen()
    ex.show()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()
