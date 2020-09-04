import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph import widgets

from ButtonFunctions.update import update


class Application:
    """Application is the orquestrator class, responsible for the graphical
    and data layer, this design facilitates to classes to access both the
    data and the graphical components, dispensing global value, which
    are a bad design usually.

    Attributes
    ----------
        Other classes:
        Application.app : PyQt5.QtWidgets.QApplication
            PyQt5 object application, check PyQt5 documentation for more details.
        Application.buttons : Dict[str, PyQt5.QtWidgets.QPushButton]
            Dictionary relating a button to a name, used to have easy access
            to the buttons instantiated.
        Application.connection:
            Connection Handler object used to communicate with the microcontroller
        Application.forces: List[float]
            Forces list fetched from the connection.
        Application.layout: pyqtgraph.LayoutWidget
            PyQt5 object used to handle layout objects.
        Application.plot_pannels: Dict[str, pyqtgraph.graphicsItems.PlotItem.PlotItem.PlotItem]
            Dictionary relating a graph pannel to a name, used to have easy.
            access to the graphs pannels
        Application.times: List[float]
            Time list fetched from the connection.
    """

    def __init__(self, connection):
        self.app = QtGui.QApplication([])
        self.connection = connection

        ######## Data initialization
        self.update = False
        self.forces = []
        self.times = []

        self.update_cell = False
        self.forces = []
        self.times = []
        ### ver como que funciona aquele delay do tempo
        
        ######## Graphical initialization
        view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
        view.pg.setConfigOptions(antialias=True)
        view.setWindowTitle('Test Platform')

        pview = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
        pview.pg.setConfigOptions(antialias=True)
        pview.setWindowTitle('Test Platform')

        self.layout = pg.LayoutWidget()
        self.layout.addWidget(view, row=2, col=0, colspan=6)
        self.layout.addWidget(pview, row=4, col=0, colspan=6)
        self.layout.resize(800, 800)

        self.plot_pannels = {}
        self.buttons = {}

        self.pannels_initialization(view, pview)
        self.button_initialization()

        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: update(self))
        timer.setInterval((10 ** 3) * (10 ** 3))
        timer.start(20)
        self.show()

    def pannels_initialization(self, view , pview) -> None:
        """Initialize the pannels required for the application"""
        self.plot_pannels.update({'plot1': self.add_plot_pannel(view)})
        self.plot_configuration('plot1', 'Pressure Curve', 'Time (s)', 'Pressure (bar)')
        self.plot_pannels.update({'plot2': self.add_plot_pannel(pview)})
        self.plot_configuration('plot2', 'Thrust Curve', 'Time (s)', 'Force (N)')

    def plot_configuration(self, plot: str, title: str, xlabel: str, ylabel: str) -> None:
        """Set labels and titles to an assigned PlotItem"""
        self.plot_pannels[plot].setTitle(title)
        self.plot_pannels[plot].setLabel('bottom', xlabel)
        self.plot_pannels[plot].setLabel('left', ylabel)

    def button_initialization(self) -> None:
        """Initialize the buttons required for the application and assign their functions"""
        from ButtonFunctions import ignition, save_curve, supress, reset, start_transducer, cell_switch

        self.buttons.update({'ignition': self.add_button('&Ignition', ignition)})
        #self.buttons.update({'supress': self.add_button('Su&press', supress)})
        self.buttons.update({'reset': self.add_button('&Reset', reset)})
        self.buttons.update({'save': self.add_button('&Save', save_curve)})
        self.buttons.update({'start_transducer': self.add_button('&START Transducer', start_transducer)})
        self.buttons.update({'update_cell': self.add_button('&START Cell', cell_switch)})
        #self.buttons.update({'stop_cell': self.add_button('&STOP Cell', stop_cell)})
        self.layout.show()

    def add_plot_pannel(self, pview: widgets.RemoteGraphicsView.RemoteGraphicsView) -> None:
        """Adds a new plot pannel"""
        new_plot_pannel = pview.pg.PlotItem()
        new_plot_pannel._setProxyOptions(deferGetattr=True)
        pview.setCentralItem(new_plot_pannel)
        return new_plot_pannel

    def show(self) -> None:
        """Exhibits the app"""
        QtGui.QApplication.instance().exec_()

    def add_button(self, name: str, function=None, visible: bool = True):
        """Creates a button on the layout"""
        new_button = QtGui.QPushButton(name)
        new_button.setDefault(True)
        new_button.toggle()
        font = QtGui.QFont("Arial", 12)
        new_button.setFont(font)
        if function:
            new_button.clicked.connect(lambda: function(self))
        if not visible:
            new_button.hide()
        self.layout.addWidget(new_button)
        return new_button

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
