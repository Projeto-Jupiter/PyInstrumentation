import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph import widgets


class Widget:

    def __init__(self):
        self.app = QtGui.QApplication([])

        view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
        view.pg.setConfigOptions(antialias=True)
        view.setWindowTitle('Test Platform')

        pview = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
        pview.pg.setConfigOptions(antialias=True)
        pview.setWindowTitle('Test Platform')

        self.layout = pg.LayoutWidget()
        self.layout.addWidget(view, row=1, col=0, colspan=6)
        self.layout.addWidget(pview, row=2, col=0, colspan=6)
        self.layout.resize(800, 800)

        from ButtonFunctions.fire import ignition, supress
        from ButtonFunctions.save import save_curve
        
        self.add_button('&Ignition', ignition)
        self.add_button('Su&press', supress)
        self.add_button('&Reset')
        self.add_button('&Save', save_curve)
        self.add_button('&START')
        self.layout.show()

        rplt = view.pg.PlotItem()
        rplt._setProxyOptions(deferGetattr=True)
        view.setCentralItem(rplt)

        self.add_plot_pannel(pview)
        self.add_plot_pannel(pview)

        lastUpdate = pg.ptime.time()
        avgFps = 0.0

        timer = QtCore.QTimer()
        # timer.timeout.connect(update)
        timer.start(0)
        self.show()

    def add_plot_pannel(self, pview: widgets.RemoteGraphicsView.RemoteGraphicsView) -> None:
        new_plot_pannel = pview.pg.PlotItem()
        new_plot_pannel._setProxyOptions(deferGetattr=True)
        pview.setCentralItem(new_plot_pannel)

    def show(self) -> None:
        QtGui.QApplication.instance().exec_()

    def add_button(self, name, function=None, visible=True) -> None:
        new_button = QtGui.QPushButton(name)
        new_button.setDefault(True)
        new_button.toggle()
        if function:
            new_button.clicked.connect(function)
        if not visible:
            new_button.hide()
        self.layout.addWidget(new_button)

# def ss():
#    global rec, ptimes, pforces, t0, times
#    if rec:  # Stop
#        rec = False
#        l2.setText("")
#        b1.setText("&Start")
#        # print("Stop")

#    else:  # Start
#        t0 = times[-1]
#        rec = True
#        l2.setText("REC")
#        b1.setText("&Stop")
#        # print("Start")
#        ptimes = []
#        pforces = []
