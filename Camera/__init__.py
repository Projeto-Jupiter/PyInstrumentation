import cv2
import numpy as np
import socket
import struct
from pyqtgraph.Qt import QtGui, QtCore

class CameraHandler(QtCore.QThread):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 42069)) 
    
    signal = QtCore.pyqtSignal(QtGui.QImage)
    
    def run(self):
        self.ThreadActive = True
        self.flush_buffer()
        dat = b''
        while self.ThreadActive:
            seg, addr = self.sock.recvfrom(2**16) # UDP datagram is 2^16 = 65536 bytes
            if struct.unpack('b', seg[0:1])[0] > 1:
                dat += seg[1:]
            else:
                dat += seg[1:]
                img = cv2.imdecode(np.frombuffer(dat, dtype=np.uint8), 1)  
                try:
                    treated_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    qImg = QtGui.QImage(treated_img.data, treated_img.shape[1], treated_img.shape[0], QtGui.QImage.Format_RGB888)
                    resized_qImg = qImg.scaled(600, 300, QtCore.Qt.KeepAspectRatio)
                    self.signal.emit(resized_qImg)
                except cv2.error:
                    self.flush_buffer()
                dat = b''
    
    def flush_buffer(self):
        while True:
            seg, addr = self.sock.recvfrom(2**16)
            if struct.unpack('b', seg[0:1])[0] == 1:
                break

    def stop(self):
        self.ThreadActive = False
        self.quit()
