import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph import widgets

from ButtonFunctions.update import update
from constants import LOAD_CELL_REFF, PRESSURE_TRANSDUCER_REF


class Data:
    """Data is a class which handles the data from each of the connections
    managed by the main application. More speciffically, it stores retrieved data
    in lists, besides indicating if the specifc connection is currenly being updated
    or not.
    """
    def __init__(self, name, plot: bool, title: str = None, xlabel: str = None, ylabel: str = None):
        self.name = name
        self.data = []
        self.times = []

        self.updateStatus = False
        self.plot = plot

        # initialize optional args
        self.framework, self.title, self.xlabel, self.ylabel = None, None, None, None

        if plot:
            self.plot_attributes(title, xlabel, ylabel)

    def plot_attributes(self, title: str, xlabel: str, ylabel: str) -> None:
        """Set plot attributes for Data component"""
        self.framework = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
        self.framework.pg.setConfigOptions(antialias=True)
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

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
        Application.layout: pyqtgraph.LayoutWidget
            PyQt5 object used to handle layout objects.
        Application.plot_pannels: Dict[str, pyqtgraph.graphicsItems.PlotItem.PlotItem.PlotItem]
            Dictionary relating a graph pannel to a name, used to have easy
            access to the graphs pannels.
    """

    def __init__(self, connection):
        self.app = QtGui.QApplication([])
        self.app.setApplicationName("PyInstrumentation")
        self.app.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.connection = connection

        ######## Data initialization
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.plot_pannels = {}
        self.data_initialization()
        self.layout = pg.LayoutWidget()
        for i, sensor in enumerate(self.sensor_data):
            if sensor.plot:
                self.layout.addWidget(sensor.framework, row=0, col=2*i)
                self.pannels_initialization(sensor)
        self.layout.addWidget(self.CameraWidget(), row= 0, col=4)
        self.layout.addWidget(self.SensoriamentoWidget(), row=1, col=0, rowspan=2)
        self.layout.addWidget(self.ReservatorioWidget(), row=1, col=2, rowspan=1)
        self.layout.addWidget(self.TanqueWidget(), row=2, col=2, rowspan=1)
        self.layout.addWidget(self.ComandosWidget(), row=1, col=4, rowspan=2)     
        
        self.layout.resize(1366, 768)
        self.buttons = {}
        self.button_initialization()

        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: update(self))
        timer.setInterval((10 ** 3) * (10 ** 3))
        timer.start(20)
        self.show()

    def data_initialization(self):
        """Intializes all objects to be instatiaded by the Data class"""
        LoadCell = Data(name=LOAD_CELL_REFF,
                        plot=True,
                        title='Thrust Curve',
                        xlabel='Time (s)',
                        ylabel='Force (N)')

        PressureTransducer = Data(name=PRESSURE_TRANSDUCER_REF,
                                  plot=True,
                                  title='Pressure Curve',
                                  xlabel='Time (s)',
                                  ylabel='Pressure (bar)')

        Termopar = Data(name='Termopar',
                        plot=False)

        self.sensor_data = [LoadCell, PressureTransducer, Termopar]

    def get_sensor_info(self, ref):
        """Retrives a sensor from sensor_data list by searching for its name"""
        for sensor in self.sensor_data:
            if ref == sensor.name:
                return sensor


    def pannels_initialization(self, sensor) -> None:
        """Initialize the pannels required for the application"""
        self.plot_pannels.update({sensor.name: self.add_plot_pannel(sensor.framework)})
        self.plot_configuration(sensor.name, sensor.title, sensor.xlabel, sensor.ylabel)

    def add_plot_pannel(self, pview: widgets.RemoteGraphicsView.RemoteGraphicsView) -> None:
        """Adds a new plot pannel"""
        new_plot_pannel = pview.pg.PlotItem()
        new_plot_pannel._setProxyOptions(deferGetattr=True)
        pview.setCentralItem(new_plot_pannel)
        return new_plot_pannel

    def plot_configuration(self, plot: str, title: str, xlabel: str, ylabel: str) -> None:
        """Set labels and titles to an assigned PlotItem"""
        self.plot_pannels[plot].setTitle(title)
        self.plot_pannels[plot].setLabel('bottom', xlabel)
        self.plot_pannels[plot].setLabel('left', ylabel)

    def button_initialization(self) -> None:
        """Initialize the buttons required for the application and assign their functions"""
        from ButtonFunctions import ignition, save_curve, supress, reset, data_switch

        self.buttons.update({'ignition': self.add_button('&Ignition', ignition)})
        # self.buttons.update({'supress': self.add_button('Su&press', supress)})
        self.buttons.update({'reset': self.add_button('&Reset', reset)})
        self.buttons.update({'save': self.add_button('&Save', save_curve)})
        for sensor in self.sensor_data:
            self.buttons.update(
                {sensor.name + 'Switch': self.add_button('&START ' + sensor.name, data_switch, sensor.name)})
        self.layout.show()

    def add_button(self, name: str, function=None, ref=None, visible: bool = True):
        """Creates a button on the layout"""
        new_button = QtGui.QPushButton(name)
        new_button.setDefault(True)
        new_button.toggle()
        font = QtGui.QFont("Arial", 12)
        new_button.setFont(font)
        if function:
            if ref:
                new_button.clicked.connect(lambda: function(self, ref))
            else:
                new_button.clicked.connect(lambda: function(self))
        if not visible:
            new_button.hide()
        self.buttonLayout.addWidget(new_button, len(self.buttons)//2, len(self.buttons)%2)
        return new_button

    def add_prompt(self, title: str, text: str):
        """Creates a pop-up when pressing a button, requesting confirmation"""
        popup = QtGui.QMessageBox()
        popup.setWindowTitle(title)
        popup.setText(text)
        popup.setIcon(QtGui.QMessageBox.Warning)
        popup.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        returnValue = popup.exec_()
        if returnValue == QtGui.QMessageBox.Yes:
            prompt = True
        else:
            prompt = False
        return prompt

    def show(self) -> None:
        """Exhibits the app"""
        QtGui.QApplication.instance().exec_()

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


###############################################################
###############################################################
###############################################################
###############################################################
###############################################################

    # Widgets

    def CameraWidget(self):
        from Camera import CameraHandler
        
        cameraFeed = QtGui.QGroupBox("Feed de Câmera")
        self.cameraLabel = QtGui.QLabel()
        
        self.cameraHandler = CameraHandler()
        self.cameraHandler.start()
        self.cameraHandler.signal.connect(lambda image: self.cameraLabel.setPixmap(QtGui.QPixmap.fromImage(image)))

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.cameraLabel)
        cameraFeed.setLayout(layout)

        return cameraFeed
    
    def SensoriamentoWidget(self):
        sensoresLinhaGroupBox = QtGui.QGroupBox("Sensores de Linha")
        
        lineLabel1 = QtGui.QLabel("Temperatura:")
        #label1.setStyleSheet("border: 1px solid black;") 
        lineLabel2 = QtGui.QLabel("0 °C") 
        lineLabel2.setStyleSheet("background-color: white; border: 3px solid black; font: bold 14px;")  
        lineLabel2.setFixedSize(70,25)
        lineLabel3 = QtGui.QLabel("Pressão:")
        lineLabel4 = QtGui.QLabel("0 bar")
        lineLabel4.setStyleSheet("background-color: white; border: 3px solid black; font: bold 14px;")
        lineLabel4.setFixedSize(70,25)
        lineLabel5 = QtGui.QLabel("Temperatura Crítica:")
        lineLabel6 = QtGui.QLabel("37 °C")
        lineLabel6.setStyleSheet("color: red;")
        lineLabel7 = QtGui.QLabel("Pressão Crítica:")
        lineLabel8 = QtGui.QLabel("65 bar")
        lineLabel8.setStyleSheet("color: red;")
        
        lineLayout = QtGui.QGridLayout()
        lineLayout.addWidget(lineLabel1,0,0)
        lineLayout.addWidget(lineLabel2,0,1)
        lineLayout.addWidget(lineLabel3,0,3)
        lineLayout.addWidget(lineLabel4,0,4)
        lineLayout.addWidget(lineLabel5,1,0)
        lineLayout.addWidget(lineLabel6,1,1)
        lineLayout.addWidget(lineLabel7,1,3)
        lineLayout.addWidget(lineLabel8,1,4)
        lineLayout.setColumnStretch(2,100)
        #layout.addStretch(1)

        sensoresLinhaGroupBox.setLayout(lineLayout)

        #############################################################################
        
        tankLabel1 = QtGui.QLabel("Temperatura:")
        tankLabel2 = QtGui.QLabel("0 °C") 
        tankLabel2.setStyleSheet("background-color: white; border: 3px solid black; font: bold 14px;")
        tankLabel2.setFixedSize(70,25)  
        tankLabel3 = QtGui.QLabel("Pressão:")
        self.tankLabel4 = QtGui.QLabel("0 bar")
        self.tankLabel4.setStyleSheet("background-color: white; border: 3px solid black; font: bold 14px;")
        self.tankLabel4.setFixedSize(70,25)
        tankLabel5 = QtGui.QLabel("Temperatura Crítica:")
        tankLabel6 = QtGui.QLabel("37 °C")
        tankLabel6.setStyleSheet("color: red;")
        tankLabel7 = QtGui.QLabel("Pressão Crítica:")
        tankLabel8 = QtGui.QLabel("65 bar")
        tankLabel8.setStyleSheet("color: red;")
        
        tankLayout = QtGui.QGridLayout()
        tankLayout.addWidget(tankLabel1,0,0)
        tankLayout.addWidget(tankLabel2,0,1)
        tankLayout.addWidget(tankLabel3,0,3)
        tankLayout.addWidget(self.tankLabel4,0,4)
        tankLayout.addWidget(tankLabel5,1,0)
        tankLayout.addWidget(tankLabel6,1,1)
        tankLayout.addWidget(tankLabel7,1,3)
        tankLayout.addWidget(tankLabel8,1,4)
        tankLayout.setColumnStretch(2,100)

        sensoresTanqueGroupBox = QtGui.QGroupBox("Sensores do Tanque")
        sensoresTanqueGroupBox.setLayout(tankLayout)

        ###################################################
        sensoriamentoGroupBox = QtGui.QGroupBox("Sensoriamento")

        layout = QtGui.QVBoxLayout()
        layout.addWidget(sensoresLinhaGroupBox)
        layout.addWidget(sensoresTanqueGroupBox)

        sensoriamentoGroupBox.setLayout(layout)

        return sensoriamentoGroupBox

    def ReservatorioWidget(self):
        labelQV1 = QtGui.QLabel("QV1 (Linha)")
        openButtonQV1 = QtGui.QRadioButton("ABERTA")
        closedButtonQV1 = QtGui.QRadioButton("FECHADA")
        closedButtonQV1.setChecked(True)
        
        QV1widget = QtGui.QWidget()
        layoutQV1 = QtGui.QHBoxLayout(QV1widget)
        layoutQV1.addWidget(labelQV1)
        layoutQV1.addWidget(openButtonQV1)
        layoutQV1.addWidget(closedButtonQV1)

        labelQV3 = QtGui.QLabel("QV3 (Exterior)")
        openButtonQV3 = QtGui.QRadioButton("ABERTA")
        closedButtonQV3 = QtGui.QRadioButton("FECHADA")
        closedButtonQV3.setChecked(True)

        QV3widget = QtGui.QWidget()
        layoutQV3 = QtGui.QHBoxLayout(QV3widget)
        layoutQV3.addWidget(labelQV3)
        layoutQV3.addWidget(openButtonQV3)
        layoutQV3.addWidget(closedButtonQV3)

        layoutSolenoid = QtGui.QVBoxLayout()
        layoutSolenoid.addWidget(QV1widget)
        layoutSolenoid.addWidget(QV3widget)

        solenoidGroupBox = QtGui.QGroupBox("Válvulas Solenoides")
        solenoidGroupBox.setLayout(layoutSolenoid)

        ##############################################################


        proportionalGroupBox = QtGui.QGroupBox("Válvula Proporcional")

        radioButton1 = QtGui.QRadioButton("ABERTA 0%")
        radioButton2 = QtGui.QRadioButton("ABERTA 25%")
        radioButton3 = QtGui.QRadioButton("ABERTA 75%")
        radioButton4 = QtGui.QRadioButton("ABERTA 100%")
        radioButton1.setChecked(True)

        layoutProportional = QtGui.QGridLayout()
        layoutProportional.addWidget(radioButton1,0,0)
        layoutProportional.addWidget(radioButton2,0,1)
        layoutProportional.addWidget(radioButton3,1,0)
        layoutProportional.addWidget(radioButton4,1,1)
        
        proportionalGroupBox.setLayout(layoutProportional)

        ##########################################        

        layout = QtGui.QVBoxLayout()
        layout.addWidget(solenoidGroupBox)
        layout.addWidget(proportionalGroupBox)

        reservatorioGroupBox = QtGui.QGroupBox("Reservatório")
        reservatorioGroupBox.setLayout(layout)

        return reservatorioGroupBox
    
    def TanqueWidget(self):
        labelQV2 = QtGui.QLabel("    QV2")
        openButtonQV2 = QtGui.QRadioButton("ABERTA")
        closedButtonQV2 = QtGui.QRadioButton("FECHADA")
        closedButtonQV2.setChecked(True)   

        layoutSolenoid = QtGui.QHBoxLayout()
        layoutSolenoid.addWidget(labelQV2)
        layoutSolenoid.addWidget(openButtonQV2)
        layoutSolenoid.addWidget(closedButtonQV2)

        solenoidGroupBox = QtGui.QGroupBox("Válvulas Solenoides")
        solenoidGroupBox.setLayout(layoutSolenoid)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(solenoidGroupBox)

        tanqueGroupBox = QtGui.QGroupBox("Tanque de Voo")     
        tanqueGroupBox.setLayout(layout)

        return tanqueGroupBox

    def ComandosWidget(self):
        self.buttonLayout = QtGui.QGridLayout()

        comandosGroupBox = QtGui.QGroupBox("Comandos")
        comandosGroupBox.setLayout(self.buttonLayout)

        return comandosGroupBox



