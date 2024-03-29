from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import telnetlib
import numpy as np
import pyqtgraph.widgets.RemoteGraphicsView
import urllib
import time
import pyqtgraph.exporters
import serial


sp = False #Use serial port
ip = "192.168.1.42"

serialport = 'COM3'
baudrate = 57600

pforce = 0.0
force = 0.0

def startserial():
    ser = serial.Serial()
    ser.baudrate = baudrate
    ser.port = serialport
    ser.open()
    time.sleep(2)
    for i in range (100):
        msg = ser.readline() #Flush serial buffer
    return ser

ptimes = []
pforces = []
t0 = 0.0

times = [-100]
forces = []

if sp:
    ser = startserial()


else:
    tn = telnetlib.Telnet(ip,1000)


tn.write("Ola")

rec = False
on = False




def ss():
    global rec, ptimes, pforces, t0, times
    if rec: #Stop
        rec = False





        l2.setText("")
        b1.setText("&Start")
        #print("Stop")

    else:# Start
        t0 = times[-1]
        rec = True
        l2.setText("REC")
        b1.setText("&Stop")
        #print("Start")
        ptimes = []
        pforces = []

def fire():
    global on
    if on: #Supress command
        on = False
        b4.setText("&Ignition")
        if not sp:
            tn.write("sup\r\n")
        else:
            ser.write("sup\r\n")


    else:# Fire command
        on = True
        b4.setText("Su&press")
        if not sp:
            tn.write("fire\r\n")
        else:
            ser.write("fire\r\n")
            print("passei")

def arm():
    global on
    if on: #Supress command
        on = False
        b5.setText("&Arm")
        if not sp:
            tn.write("sup2\r\n")
        else:
            ser.write("sup2\r\n")


    else:# Fire command
        on = True
        b5.setText("Su&press")
        if not sp:
            tn.write("arm\r\n")
        else:
            ser.write("arm\r\n")
            print("passei")


def rst():
    global times, forces, ptimes, pforces, tn, rec, ser
    if rec: # if recording then stop
        ss()
    #print("Reset")
    ptimes = []
    pforces = []
    times = [-100]
    forces = []

    if not sp:
        urllib.urlopen("http://%s/console/reset" %ip)
        time.sleep(2)
        tn = telnetlib.Telnet(ip,1000)
    else:
        ser.close()
        time.sleep(2)
        ser = startserial()


def save():
    global ptimes, pforces
    nome = raw_input("Digite o nome do arquivo: ")
    nome = nome + ".txt"
    myfile = open(nome, 'w')
    for i in range(len(ptimes)):
        pair = str(ptimes[i]) + "," + str(pforces[i]) + '\n'
        #print(pair)
        myfile.write(pair)
    myfile.close()

app = QtGui.QApplication([])


view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
view.pg.setConfigOptions(antialias=True)  ## prettier plots at no cost to the main process!
view.setWindowTitle('Test Platform')

pview = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
pview.pg.setConfigOptions(antialias=True)  ## prettier plots at no cost to the main process!
pview.setWindowTitle('Test Platform')

layout = pg.LayoutWidget()
layout.addWidget(view, row=1, col=0, colspan=6)
layout.addWidget(pview, row=2, col=0, colspan=6)
layout.resize(800,800)

#

b4 = QtGui.QPushButton("&Ignition")
b4.setDefault(True)
b4.toggle()
b4.clicked.connect(fire)
layout.addWidget(b4)

b5 = QtGui.QPushButton("&Arm")
b5.setDefault(True)
b5.toggle()
b5.clicked.connect(arm)
layout.addWidget(b5)

label = QtGui.QLabel()
layout.addWidget(label)

l2 = QtGui.QLabel()
layout.addWidget(l2)

b2 = QtGui.QPushButton("&Reset")
b2.setDefault(True)
b2.toggle()
b2.clicked.connect(rst)
layout.addWidget(b2)

b3 = QtGui.QPushButton("Save")
b3.setDefault(True)
b3.toggle()
b3.clicked.connect(save)
layout.addWidget(b3)

b1 = QtGui.QPushButton("&Start")
b1.setDefault(True)
b1.toggle()
b1.clicked.connect(ss)
layout.addWidget(b1)



#

layout.show()


## Create a PlotItem in the remote process that will be displayed locally
rplt = view.pg.PlotItem()
rplt._setProxyOptions(deferGetattr=True)  ## speeds up access to rplt.plot
view.setCentralItem(rplt)

prplt = pview.pg.PlotItem()
prplt._setProxyOptions(deferGetattr=True)  ## speeds up access to rplt.plot
pview.setCentralItem(prplt)

lastUpdate = pg.ptime.time()
avgFps = 0.0

def update():
    global label, plt, lastUpdate, avgFps, rpltfunc, rec, forces, times, rcheck, force, pforce

    if not sp:
        msg = tn.read_until("\n")[:-2]
    else:
        msg = ser.readline()[:-2]

    pair = msg.split(";")
    if len(pair) == 2:
        pforce, time = pair

        try:
            pforce = float(pforce)
            force = pforce
            """if ((pforce < 4000.0) and (pforce > -5.0)): # and not(pforce == 35.88)and not(pforce == 53.31)and not(pforce == 51.77)and not(pforce == 51.61)):
                force = pforce"""


        except:
            print("check connection")



        try:
            time = float(time)/1000
        except:
            print("check connection")



        if time - times[0] > 10:
            times = times[1:]
            forces = forces[1:]
            times.append(time)
            forces.append(force)
        else:
            times.append(time)
            forces.append(force)


        if rec:
            pforces.append(force)
            ptimes.append(time - t0)
            pydata = np.asarray(pforces)
            pxdata = np.asarray(ptimes)
            prplt.plot(pxdata, pydata, clear=True, _callSync='off')

        ydata = np.asarray(forces)
        xdata = np.asarray(times)

        rplt.plot(xdata, ydata, clear=True, _callSync='off')  ## We do not expect a return value.
                                                              ## By turning off callSync, we tell
                                                              ## the proxy that it does not need to
                                                              ## wait for a reply from the remote
                                                              ## process.
        now = pg.ptime.time()
        fps = 1.0 / (now - lastUpdate)
        lastUpdate = now
        avgFps = avgFps * 0.8 + fps * 0.2
        label.setText("Generating %0.2f fps" % avgFps)
    else:
        pass
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)




QtGui.QApplication.instance().exec_()
