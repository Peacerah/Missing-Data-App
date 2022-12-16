#import the required modules
import sys
import os
from PyQt5.QtWidgets import * #QMainWindow, QDialog, QFileDialog, QMessageBox, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import * #QFile, QFont
from PyQt5.uic import *
from numpy import random
import sqlite3
import pandas as pd
import numpy as np
import time
import resources
class WorkerThread(QThread):
    #finished = pyqtSignal()
    change_value = pyqtSignal(int)
    def run(self):
        count = 0
        while count < 100:
            count+=1
            time.sleep(0.05)
            self.change_value.emit(count)

class MDE(QMainWindow):
    def __init__(self, parent = None):
        super(MDE, self).__init__(parent)
        fileh = QFile(':/ui/AppMiss.ui')
        fileh.open(QFile.ReadOnly)
        loadUi(fileh, self)
        fileh.close()
        self.progressBar.hide()
        #Load the data containing the missing data
        self.loadButton.clicked.connect(self.loadData)
        self.estimateButton.clicked.connect(self.estimate)

    def loadData(self):
        #self.inputFilename = QFileDialog.getOpenFileName(self, "Open image file","c\\","Excel Workbook(*.xls *.xlsx)")
        #def loadFiles(self)
        self.inputFilename = QFileDialog.getOpenFileName(self, "Open the csv file containing the missing data ","c\\","Comma Seperated Value File(*.csv)")
        self.loadLineEdit.setText(str(self.inputFilename[0]))
        self.input_data =  str(self.inputFilename[0])
        #print(self.input_data)
        self.dataset = pd.read_csv(self.input_data)
        columns_name = []
        for col in self.dataset.columns:
            columns_name.append(col)
            #if isinstance(test_string, str)
        self.indexComboBox.addItems(columns_name)
        self.dataComboBox.addItems(columns_name)

    def showMessage(self, title, text):
        mesgbox = QMessageBox()
        mesgbox.setIcon(QMessageBox.Information)
        mesgbox.setWindowTitle(title)
        mesgbox.setText(text)
        mesgbox.setStandardButtons(QMessageBox.Ok)
        mesgbox.exec_()
        
    def setProgressValue(self,val):
        #self.progressBar.setValue(val)
        self.progressBar.setValue(val)
            
    def estimate(self):
        self.outputFilename = QFileDialog.getSaveFileName(self, "Save the csv file of the filled data","c\\","Comma Seperated Value File(*.csv)")
        self.fillLineEdit.setText(str(self.outputFilename[0]))
        self.output_data =  str(self.outputFilename[0])
        self.progressBar.show()
        self.myThread = WorkerThread()
        self.myThread.change_value.connect(self.setProgressValue)
        self.myThread.start()
        self.dataset = pd.read_csv(self.input_data,encoding='ISO-8859-1')
       
        if self.methodComboBox.currentText() == "Next Observation Carried Backward":
            Estimated = self.dataComboBox.currentText() +"_NOCB"
            print(Estimated)
            self.dataset[Estimated]= self.dataset[self.dataComboBox.currentText()].fillna(method ='bfill')
            print("Sucess - filled by NOCB")
            self.dataset = self.dataset[[self.indexComboBox.currentText(), self.dataComboBox.currentText(),Estimated]]
            print("Sucess - Column created")
            self.dataset.to_csv(self.output_data)
            print("Sucess - converted output to csv")
        if self.methodComboBox.currentText() == "Last Observation Carried Forward":
            Estimated = self.dataComboBox.currentText() +"_LOCF"
            print(Estimated)
            self.dataset[Estimated]= self.dataset[self.dataComboBox.currentText()].fillna(method ='ffill')
            print("Sucess - filled by NOCB")
            self.dataset = self.dataset[[self.indexComboBox.currentText(), self.dataComboBox.currentText(),Estimated]]
        self.dataset.to_csv(self.output_data)
        print("Sucess - converted output to csv")
        self.myThread.finished.connect(lambda:self.showMessage("Success",f"The missing data have been sucessfully filled by {self.methodComboBox.currentText()} Method"))
            #self.progressBar.hide()
            
app = QApplication(sys.argv)
app.setStyle("Fusion")
screen = MDE()
screen.show()
sys.exit(app.exec_())
