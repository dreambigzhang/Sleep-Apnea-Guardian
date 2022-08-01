"""
This graphs EEG data, live. 
"""

import csv
import logging
import pdb
import random
import sys
import time
from dataclasses import dataclass
import matplotlib.pyplot as plt

from SleepApneaDetect import *

from Board import Board, get_board_id
from utils.save_to_csv import save_to_csv

log_file = "boiler.log"
logging.basicConfig(level=logging.INFO, filemode="a")

f = logging.Formatter(
    "Logger: %(name)s: %(levelname)s at: %(asctime)s, line %(lineno)d: %(message)s"
)
stdout = logging.StreamHandler(sys.stdout)
boiler_log = logging.FileHandler(log_file)
stdout.setFormatter(f)
boiler_log.setFormatter(f)

logger = logging.getLogger("GraphWindow")
logger.addHandler(boiler_log)
logger.addHandler(stdout)
logger.info("Program started at {}".format(time.time()))

import statistics as stats
from multiprocessing import Process, Queue

# from pyqtgraph.Qt import QtGui, QtCore
from random import randint

import brainflow
import numpy as np
#import pyqtgraph as pg
from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, DetrendOperations, FilterTypes
from PyQt5.QtCore import QTimer
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import *


from pyqtgraph.Qt import QtCore



SIMULATE = 0
FILE = 1
LIVESTREAM = 2

class graph_win():
    def __init__(
        self,
        setIndicator=lambda:print("no callback provided!"),
        hardware=None,
        model=None,
        sim_type=None,
        data_type=None,
        serial_port=None,
        save_file=None,
        parent=None,
        board_id=None,
    ):
        # read from csv file
        self.sim_data = self.read_csv()
        self.detector = SleepApneaDetect()
        lines = 256

        self.setIndicator = setIndicator
        self.state = True

        for i in range(27):
            #print(i)
            self.sim_update(self.sim_data[lines*i:lines*(i+1),:])
            time.sleep(0.1)
    

    def read_csv(self):
        data = np.genfromtxt('record.csv',delimiter=',')
        print(data.shape)
        return data
    
    def sim_update(self, data):
        #logger.debug("Graph window is updating")
        #print(data.shape)
        #print(data)
        # subtracting forehead channels to minimize REM interference

        ### TESTING callback
        
        self.sleep_apnea_bool = False
        
        delta1 = self.sim_getAverage(1,data,1)
        delta2 = self.sim_getAverage(4,data,1)
        beta1 = self.sim_getAverage(1,data,3)
        beta2 = self.sim_getAverage(4,data,3)
        averageDeltaToBeta = ((delta1+delta2)/2)/((beta1+beta2)/2)
        print(averageDeltaToBeta)
        
        state = self.detector.update(averageDeltaToBeta)
        self.setIndicator(state)
        
    def sim_getAverage(self, channelNum, data, band):

        # this is data to be graphed. It is the most recent data, of the length that we want to graph
        channelData = data[:,channelNum-1]
        yourFftData = np.fft.fft(channelData)
        yourFreq = np.fft.fftfreq(len(channelData))*256

        # Step 2: Remove the Powerline
        # =============================
        # To help make flexible code, let's define some variables
        cutFreq = 60
        tolerance = 2 # You want to cut a small range around the target frequency to account for inaccuaracies in measuring

        # Use slicing to set a range of values to 0 amplitude
        yourFftData[ cutFreq-tolerance: cutFreq+tolerance] = 0

        # Plot our result - This is the same code as above!
        yourPlotFreq = yourFreq[1:int(len(yourFreq)/2)]
        yourPlotFftData = yourFftData[1:int(len(yourFftData)/2)]

        bandTotals = [0,0,0,0,0]
        bandCounts = [0,0,0,0,0]

        for point in range(len(yourFreq)):
            if(yourFreq[point] < 4):
                bandTotals[0] += abs(yourFftData[point])
                bandCounts[0] += 1
            elif(yourFreq[point] < 8):
                bandTotals[1] += abs(yourFftData[point])
                bandCounts[1] += 1
            elif(yourFreq[point] < 12  ):
                bandTotals[2] += abs(yourFftData[point])
                bandCounts[2] += 1
            elif(yourFreq[point] < 30 ):
                bandTotals[3] += abs(yourFftData[point])
                bandCounts[3] += 1
            elif(yourFreq[point] < 100 ):
                bandTotals[4] += abs(yourFftData[point])
                bandCounts[4] += 1
    
        return (bandTotals[band])/(bandCounts[band])
