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
# creating a thread class
class WorkerThread(QThread):
    #finished = pyqtSignal()
    change_value = pyqtSignal(int)
    def run(self):
        count = 0
        while count < 100:
            count+=1
            time.sleep(0.05)
            self.change_value.emit(count)
# creating a MDE-Missing data estimation class, a subclass of QMainWindow   
class MDE(QMainWindow):
    def __init__(self, parent = None):
        super(MDE, self).__init__(parent)
        fileh = QFile(':/ui/Appui.ui')
        fileh.open(QFile.ReadOnly)
        loadUi(fileh, self)
        fileh.close()
        #Load the data containing the missing data
        self.loadDataButton.clicked.connect(self.loadData)

    def comboChanged(self):
        self.Posting_Category_Label.setFont(QFont('Times',16))
        text = self.comboBox.currentText()
        if self.comboBox.currentText() == "Last Observation Carried Forward":
            self.specialPosting_groupBox.hide()
            self.posting_label.setText(text + ' ' + 'SELECTED')
            #self.Posting_Category_Label.setFont(QFont('Times',16))
            self.Posting_Category_Label.setText(text + ' ' + 'INTERFACE')
        if self.comboBox.currentText() == "Next Observation Carried Backward":
            self.specialPosting_groupBox.show()
            self.posting_label.setText(text + ' ' + 'SELECTED')
            self.Posting_Category_Label.setText(text + ' ' + 'INTERFACE')
        if self.comboBox.currentText() == "Mean substitution":
            self.specialPosting_groupBox.hide()
            self.posting_label.setText(text + ' ' + 'SELECTED')
            #self.Posting_Category_Label.setFont(QFont('Times',16))
            #self.Posting_Category_Label.setText(radiobut.text())
            self.Posting_Category_Label.setText(text + ' ' + 'INTERFACE')
        if self.comboBox.currentText() == "Median substitution":
            self.specialPosting_groupBox.hide()
            self.posting_label.setText(text + ' ' + 'SELECTED')
            #self.Posting_Category_Label.setFont(QFont('Times',16))
            self.Posting_Category_Label.setText(text + ' ' + 'INTERFACE')
        if self.comboBox.currentText() == "Bayesian ridge model":
            self.specialPosting_groupBox.show()
            self.posting_label.setText(text + ' ' + 'SELECTED')
            self.Posting_Category_Label.setText(text + ' ' + 'INTERFACE')
        if self.comboBox.currentText() == "Random Forest model":
            self.specialPosting_groupBox.hide()
            self.posting_label.setText(text + ' ' + 'SELECTED')
            #self.Posting_Category_Label.setFont(QFont('Times',16))
            #self.Posting_Category_Label.setText(radiobut.text())
            self.Posting_Category_Label.setText(text + ' ' + 'INTERFACE')
            
    def clearAll(self):
        self.inputLabel.setText(" ")
        self.outputLabel.setText(" ")
        self.progressBar.hide()
        #self.Posting_Category_Label.setText(self.general_radioButton.text())
        #self.general_radioButton.setChecked(True)

    def loadData(self):
        #self.inputFilename = QFileDialog.getOpenFileName(self, "Open image file","c\\","Excel Workbook(*.xls *.xlsx)")
        #def loadFiles(self)
        self.inputFilename = QFileDialog.getOpenFileName(self, "Open the csv file containing the records of the staffs","c\\","Comma Seperated Value File(*.csv)")
        self.inputLabel.setText(str(self.inputFilename[0]))
        self.input_data =  str(self.inputFilename[0])
        #print(self.input_data)
        
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
    def repost(self):
        self.progressBar.show()
        self.nis_data = pd.read_csv(self.input_data,encoding='ISO-8859-1')
        self.outputFilename = QFileDialog.getSaveFileName(self, "Save the csv file containg the reposting records of the staffs","c\\","Comma Seperated Value File(*.csv)")
        self.estimate_label.setText(self.outputFilename[0])
        #self.output_data =  str(self.outputFilename[0])
        self.estimate_label =  str(self.outputFilename[0])
        print(self.output_data)
        self.myThread = WorkerThread()
        self.myThread.change_value.connect(self.setProgressValue)
        self.myThread.start()
        

        
        self.nis_data.to_csv(self.output_data)
        self.myThread.finished.connect(lambda:self.showMessage("Success","Successful reposting"))

        
     
        
        
        
app = QApplication(sys.argv)
app.setStyle("Fusion")
screen = MDE()
screen.show()
sys.exit(app.exec_())
