import logging
import os
import random
import sys
import time

import numpy as np
from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from voice_assistant import *

from Board import (
    BCI,
    CONNECT,
    CYTON,
    CYTON_DAISY,
    GANGLION,
    MUSE,
    MUSE_2,
    MUSE_S,
    SIMULATE,
    get_board_id,
)

# Creates the global logger
log_file = "boiler.log"
logging.basicConfig(level=logging.INFO, filemode="a")

f = logging.Formatter(
    "Logger: %(name)s: %(levelname)s at: %(asctime)s, line %(lineno)d: %(message)s"
)
stdout = logging.StreamHandler(sys.stdout)
boiler_log = logging.FileHandler(log_file)
stdout.setFormatter(f)
boiler_log.setFormatter(f)

logger = logging.getLogger("MenuWindow")
logger.addHandler(boiler_log)
logger.addHandler(stdout)
logger.info("Program started at {}".format(time.time()))

# results not implemented yet
from sim_graph_window import graph_win
#from impedance_window import impedance_win

if False:  # debugging... remebeber to put the tf imports back in session_window
    import tensorflow as tf


# let's make a menu window class
class MenuWindow(QMainWindow):
    def __init__(self, parent=None):
        """The init function, creates the user interface for the main menu.

        Args:
            parent (QWindow, optional): The parent of the main window. Defaults to None.
        """
        super().__init__()
        logger.info("Initializing")

        ####################################
        ##### Init Main Window Globals #####
        ####################################

        """
        -------------------INPUTS-------------------|    
        |                  TITLE                    |
        |       HARDWARE              TYPE          |
        |       MODEL                 PORT          |
        |       CSV                   ARDUINO       |
        |                                           |
        |------------------ACTIONS------------------|
        |       arduino       graph        imped    |
        |-------------------------------------------|

        """

        self.setMinimumSize(453, 477)

        # self.setStyleSheet("background-color: gray;")
        # setting window title and icon
        self.setWindowTitle("Sleep Apnea Guardian")
        self.setWindowIcon(QtGui.QIcon("utils/logo_icon.jpg"))

        # init layout
        self.layout = QGridLayout()
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        ### DEBUG ###
        self.debug = False

        if self.debug == True:
            self.bci_serial_port = "COM1"
            self.arduino_con = "Debug"
            self.arduino_serial_port = "COM2"

        ###################################
        ##### Init GUI Input Elements #####
        ###################################

        ### INIT INPUT LAYOUTS ###
        # Create layouts explicitly for all GUI input fields
        self.header_layout = QVBoxLayout()
        self.hardware_layout = QVBoxLayout()
        self.model_layout = QVBoxLayout()
        self.type_layout = QVBoxLayout()
        self.port_layout = QVBoxLayout()
        self.csv_layout = QVBoxLayout()
        self.arduino_layout = QVBoxLayout()

        self.indicator_layout = QVBoxLayout()

        """
        |------------------INPUTS-------------------|    
        |                                           |
        |       HARDWARE              TYPE          |
        |       MODEL                 PORT          |
        |       CSV                   ARDUINO       |
        |                                           |
        |-------------------------------------------|
        """

        self.hardware = None
        self.model = None
        self.data_type = None
        self.board_id = None

        ### HEADER ###

        ## LOGO ##
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("res/logo3.png").scaled(200, 200, Qt.KeepAspectRatio))
        self.logo.setAlignment(Qt.AlignCenter)
        self.header_layout.addWidget(self.logo)

        ### TITLE ###
        self.title = QLabel()
        self.title.setFont(QtGui.QFont("Arial", 32))
        self.title.setText("Sleep Apnea Guardian")
        self.title.setAlignment(Qt.AlignCenter)
        self.header_layout.addWidget(self.title)
  
        ### END HEADER ###

        ### HARDWARE ###
        # drop down menu to decide what hardware
        self.hardware_dropdown = QComboBox()
        #self.hardware_dropdown.setSizeAdjustPolicy()
        self.hardware_dropdown.setPlaceholderText("Select hardware")
        self.hardware_dropdown.addItems([BCI, MUSE])
        self.hardware_dropdown.activated.connect(self.handle_hardware_choice)
        self.hardware_label = QLabel("Select hardware")
        self.hardware_layout.addWidget(self.hardware_label)
        self.hardware_layout.addWidget(self.hardware_dropdown)

        ### MODEL ###
        # drop down menu for model of hardware
        self.model_dropdown = QComboBox()
        self.model_dropdown.setPlaceholderText("Select model")
        self.model_label = QLabel("Select model")
        self.model_dropdown.setEnabled(False)  # starts disabled
        self.model_dropdown.activated.connect(self.handle_model_choice)
        self.model_layout.addWidget(self.model_label)
        self.model_layout.addWidget(self.model_dropdown)
        ### CSV ###
        self.csv_name = "eeg_" + log_file[:-4] + ".csv"
        self.csv_name_edit = QLineEdit(self.csv_name)
        self.csv_name_edit.returnPressed.connect(self.csv_name_changed)
        self.csv_label = QLabel(
            "Prefix of session's CSV file.\nHit 'Enter' to update filename."
        )
        self.csv_layout.addWidget(self.csv_label)
        self.csv_layout.addWidget(self.csv_name_edit)

        ### DATATYPE ###
        # drop down menu for simulate or live (previously included file step through)
        self.type_dropdown = QComboBox()
        self.type_dropdown.setPlaceholderText("Select data type")
        self.type_dropdown.addItems([CONNECT, SIMULATE])
        self.type_dropdown.activated.connect(self.handle_type_choice)
        self.type_label = QLabel("Select data type")
        self.type_layout.addWidget(self.type_label)
        self.type_layout.addWidget(self.type_dropdown)
        if self.debug == True:
            self.type_dropdown.setEnabled(True)  # start disabled
        else:
            self.type_dropdown.setEnabled(False)  # start disabled

        ### PORT ###
        self.bci_port_label = QLabel("BCI Serial Port")
        self.bci_port = QLineEdit()
        self.bci_port.setEnabled(False)
        '''
        self.port_layout.addWidget(self.bci_port_label)
        self.port_layout.addWidget(self.bci_port)
        '''
        self.bci_port.setPlaceholderText("Enter Port # (Integers Only)")
        self.bci_port.textEdited.connect(self.handle_bci_port)
        self.bci_serial_port = None  # if None gets passed to the graph window, it will look for a working port

        
        # self.arduino_process = None

        ### INDICATOR ###
        self.indicator_label = QLabel("Sleep Apnea Detected:")

        self.indicator = QPushButton()
        self.indicator.setCheckable(True)
        self.indicator.setChecked(True)
        self.indicator.setProperty("isIndicator", True)
        self.indicator_layout.addWidget(self.indicator_label)
        self.indicator_layout.addWidget(self.indicator)

        ### ADD INPUT SUBLAYOUTS TO MAIN ###
        self.layout.setContentsMargins(10, 30, 10, 30)
        self.hardware_layout.setContentsMargins(10, 10, 10, 10)
        self.model_layout.setContentsMargins(10, 10, 10, 10)
        self.csv_layout.setContentsMargins(10, 10, 10, 10)
        self.type_layout.setContentsMargins(10, 10, 10, 10)
        self.port_layout.setContentsMargins(10, 10, 10, 10)
        self.arduino_layout.setContentsMargins(10, 10, 10, 10)
        self.indicator_layout.setContentsMargins(10, 10, 10, 10)
        self.layout.addLayout(self.header_layout, 0, 0, 1, -1, QtCore.Qt.AlignHCenter)
        self.layout.addLayout(self.hardware_layout, 1, 0)
        self.layout.addLayout(self.model_layout, 2, 0)
        self.layout.addLayout(self.csv_layout, 3, 0)
        self.layout.addLayout(self.type_layout, 1, 1)
        # self.layout.addLayout(self.port_layout, 2, 1)
        self.layout.addLayout(self.indicator_layout, 2, 1);
        self.layout.addLayout(self.arduino_layout, 3, 1)

        ####################################
        ##### Init GUI Action Elements #####
        ####################################

        """
        |------------------ACTIONS------------------|
        |                                           |
        |    arduino       graph        imped       |
        |                 baseline                  |
        |-------------------------------------------|
        """

        # here is a button to actually start a impedance window
        self.impedance_window_button = QPushButton("Impedance Check")
        self.impedance_window_button.setEnabled(False)
        '''
        self.layout.addWidget(
            self.impedance_window_button, 5, 1, 1, 1, QtCore.Qt.AlignHCenter
        )
        '''
        self.impedance_window_button.clicked.connect(self.open_impedance_window)
        
        

        # here is a button to start the arduino window
        self.arduino_window_button = QPushButton("Turn on Arduino")
        self.arduino_window_button.setEnabled(False)
        '''
        self.layout.addWidget(
            self.arduino_window_button, 5, 0, 1, 1, QtCore.Qt.AlignHCenter
        )
        '''
        self.arduino_window_button.clicked.connect(self.open_arduino_window)

        # here is a button to display graph
        self.graph_window_button = QPushButton("Activate Voice Assistant")
        self.graph_window_button.setEnabled(False)
        self.layout.addWidget(
            self.graph_window_button, 5, 0, QtCore.Qt.AlignHCenter
        )
        self.graph_window_button.clicked.connect(self.open_graph_window)

        # this is a variable to show whether we have a data window open
        self.data_window_open = False

        # this is a variable to show whether we have a impedance window open
        self.impedance_window_open = False

        # here is a button for the baseline window
        self.baseline_window_button = QPushButton("Baseline")
        self.baseline_window_button.setEnabled(False)
        self.layout.addWidget(
            self.baseline_window_button, 5, 1, QtCore.Qt.AlignHCenter
        )
        self.baseline_window_button.clicked.connect(self.open_baseline_window)

        # targ limb
        self.targ_limb = None

        self.demo = True
        if self.demo:
            self.hardware_dropdown.setCurrentText("Muse")
            self.handle_hardware_choice()
            self.model_dropdown.setCurrentText("Muse 2")
            self.handle_model_choice()
            self.type_dropdown.setCurrentText("Task simulate")
            self.handle_type_choice()

    def closeEvent(self, event):
        """Autoruns before the window closes. Ensures that all running streams are terminated.

        Args:
            event (?): The close event.
        """

        event.ignore()
        return

        # this code will autorun just before the window closes
        # we will check whether streams are running, if they are we will close them
        logger.info("Closing")
        if self.data_window_open:
            self.data_window.close()
        if self.impedance_window_open:
            self.impedance_window.close()
        event.accept()

    #########################################
    ##### Functions for Handling Inputs #####
    #########################################

    def handle_hardware_choice(self):
        """Handles changes to the hardware dropdown"""
        self.hardware = self.hardware_dropdown.currentText()
        for btn in [
            self.graph_window_button,
            self.baseline_window_button,
            self.impedance_window_button,
        ]:
            btn.setEnabled(False)
        # handle the choice of hardware - by opening up model selection
        self.model_dropdown.setEnabled(True)
        self.type_dropdown.setEnabled(False)
        self.type_dropdown.setCurrentIndex(-1)
        # self.title.setText("Select model")
        self.model_dropdown.clear()
        if self.hardware_dropdown.currentText() == BCI:
            self.model_dropdown.addItems([GANGLION, CYTON, CYTON_DAISY])
        elif self.hardware_dropdown.currentText() == MUSE:
            self.model_dropdown.addItems([MUSE_2, MUSE_S])
        elif self.hardware_dropdown.currentText() == "Blueberry":
            self.model_dropdown.addItem("Prototype")

    def handle_model_choice(self):
        """Handles changes to the model dropdown"""
        # handle the choice of model by opening up data type selection
        self.model = self.model_dropdown.currentText()
        for btn in [
            self.graph_window_button,
            self.baseline_window_button,
            self.impedance_window_button,
        ]:
            btn.setEnabled(False)
        self.bci_port.setEnabled(False)
        self.type_dropdown.setEnabled(True)
        self.type_dropdown.setCurrentIndex(-1)
        # self.title.setText("Select data type")

    def csv_name_changed(self):
        """Handles changes to the csv_name text field."""
        # Ensures that the file is a csv file (the format to be written)
        if not self.csv_name_edit.text().endswith(".csv"):
            # add .csv ending if absent
            self.csv_name_edit.setText(self.csv_name_edit.text() + ".csv")

        # Ensures that the filename does not exist on the system
        filename = self.csv_name_edit.text()
        if os.path.isfile(filename):
            root = os.path.splitext(filename)[0]  # <name>.csv -> <name>
            i = 1
            while os.path.isfile(filename):
                filename = f"{root}_{i}.csv"
                i += 1

        # Prompts the user to select a directory for file saving
        save_directory = QFileDialog.getExistingDirectory()
        self.csv_name = os.path.join(save_directory, filename)
        logger.info("Selected save location: {}".format(self.csv_name))

    def handle_type_choice(self):
        """Handles changes to the data type drop down."""
        # handle the choice of data type
        self.data_type = self.type_dropdown.currentText()
        self.graph_window_button.setEnabled(True)
        self.baseline_window_button.setEnabled(True)
        self.impedance_window_button.setEnabled(True)
        if self.data_type == CONNECT:
            # self.title.setText("Select BCI Hardware Port")
            self.bci_port.setEnabled(True)
            self.board_id = get_board_id(self.data_type, self.hardware, self.model)
        elif self.data_type == SIMULATE:
            # self.title.setText("Check impedance or graph")
            self.board_id = -1

    def handle_bci_port(self):
        """Handles actions made within the bci_port text field"""
        # check for correct value entering and enable type dropdown menu
        if self.bci_port.text().isdigit():
            self.type_dropdown.setEnabled(True)
            self.bci_serial_port = "COM" + self.bci_port.text()
            if self.data_type == CONNECT:
                self.impedance_window_button.setEnabled(True)
            # self.title.setText("Check impedance or graph")
        else:
            self.bci_serial_port = None
            # print("Error: OpenBCI port # must be an integer.")
            # self.title.setText("Select BCI Hardware Port")

    def handle_arduino_dropdown(self):
        """Handles actions within the arduino dropdown"""
        # check if arduino checkbox is enabled
        self.arduino_con = self.arduino_dropdown.currentText()
        self.arduino_port.setEnabled(True)
        if self.arduino_port.text().isdigit():
            self.arduino_window_button.setEnabled(True)
            self.arduino_serial_port = "COM" + self.arduino_port.text()
        else:
            self.arduino_window_button.setEnabled(False)

    def handle_arduino_port(self):
        """Handles changes to input in the arduino port field"""
        # check for correct value entering and enable type dropdown menu
        if self.arduino_port.text().isdigit():
            self.arduino_window_button.setEnabled(True)
            self.arduino_serial_port = "COM" + self.arduino_port.text()
        else:
            self.arduino_window_button.setEnabled(False)

    #########################################
    ##### Functions for Opening Windows #####
    #########################################

    def open_arduino_window(self):
        """Opens the arduino window."""
        # this actually starts the arduino testing window
        # called by user pressing button, which is enabled by selecting from dropdowns
        # if self.arduino_process is not None:
        #     self.arduino_process.terminate()
        #     while self.arduino_process.is_alive():
        #         time.sleep(0.1)
        #     self.arduino_process.close()
        #     self.arduino_process = None
        logger.info("creating arduino window")
        if self.arduino_port.text().isdigit() != True:
            logger.warning(
                "failed to create arduino window because arduino port was not an integer"
            )
        else:
            self.data_window = ard_turn_on(
                parent=self,
                arduino_con=self.arduino_con,
                arduino_port=self.arduino_serial_port,
            )
            self.data_window.show()
            self.data_window_open = True
            logger.info("created arduino window")

    def open_impedance_window(self):
        """Opens the impedance window, moves program control over."""
        if self.hardware == MUSE:
            logger.error("Cannot use Muse hardware with impedances.")
        elif self.checks_for_window_creation():
            logger.info("creating impedance window")
            self.impedance_window = impedance_win(
                parent=self,
                hardware=self.hardware,
                model=self.model,
                data_type=self.data_type,
                serial_port=self.bci_serial_port,
                board_id=self.board_id,
            )
            self.impedance_window.show()
            self.impedance_window_open = True
            logger.info("created impedance window")
        else:
            logger.info("User must fix errors before impedance window can be created.")

    def open_graph_window(self):
        """Opens the graph window, moves program control over."""
        self.apnea  = VoiceAssistant()

        if self.checks_for_window_creation():
            logger.info("MenuWindow is creating graph window")
            self.graph_window = graph_win(setIndicator=lambda state: self.indicator.setChecked(state))
        if self.apnea.listen_for_morning():
            # palot sleep record graph
            pass

        self.graph_window.detector.plot_summary()



    def open_baseline_window(self):
        """Opens the baseline window, moves program control over."""
        if self.checks_for_window_creation():
            logger.info("MenuWindow is creating baseline window")
            self.baseline_window = baseline_win(
                parent=self,
                board_id=self.board_id,
                csv_name=self.csv_name,
                serial_port=self.bci_serial_port,
            )
            self.baseline_window.show()
            logger.info("Created baseline window")
        else:
            logger.info("User must fix error before baseline window can be created.")

    def checks_for_window_creation(self):
        """Checks that all attributes are properly set for both the impedance and graph window and baseline.
        Logs a warning message about what must be fixed.

        Returns:
            bool: True if the window can be opened, False otherwise
        """
        if self.hardware is None:
            logger.warning(
                "Hardware attribute is not set. Please fix before running graph."
            )
            return False
        elif self.model is None:
            logger.warning(
                "Model attribute is not set. Please fix before running graph."
            )
            return False
        elif self.data_type is None:
            logger.warning(
                "Data Type attribute is not set. Please fix before running graph."
            )
            return False
            # TODO: Check if simulation file exists, alert if not true
        elif self.data_type == SIMULATE and self.csv_name is None:
            logger.warning(
                "CSV file to read for simulation is not provided. Please fix before running graph."
            )
            return False

        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qss="res/style.css"
    with open(qss,"r") as fh:
        app.setStyleSheet(fh.read())

    app.setStyle("macintosh")
    win = MenuWindow()
    logger.info("MenuWindow created")
    win.show()
    print(win.width(), win.height())
    sys.exit(app.exec())
