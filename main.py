#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
from graphicUnit import Widget
from myWidgets import CheckBox, SpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QAction, QWidget,\
	QVBoxLayout, QHBoxLayout, QFileDialog, QDialog
from PyQt5.QtGui     import QIcon

def removeNullString(wordsList):
	result = []
	for word in wordsList:
		if word != "":
			result.append(word)
	return result

def saveFile(fileName, data):
	file = open(fileName, "w")
	file.write(data)
	file.close()

def openFile(fileName):
	with open(fileName, "r") as f:
		data = f.read()
		f.close()
		return data

class Configuration():

	def __init__(self):
		self.titleList       = None
		self.wordsList       = []
		self.nbFields        = 0 # variable to know the number of columns of the file
		self.columnToFilter  = []
		self.endIdx          = 100 # wr number of rows of the file
		self.startIdx        = 0 # rd
		self.question        = 1 # wr/rd
		self.nbQuestions     = 10 # rd
		self.nbClickValidMax = 2 # rd
		self.withAnswer      = True
		self.nbWordSerie     = 0 # wr
		self.nbCorrectAnswer = 0 #
		self.schlem          = 0 # wr

	def openCsvFile(self, fileName):

		try:
			with open(fileName, newline='\n', encoding='iso-8859-1',errors='ignore') as csvfile:
				fileReader = csv.reader(csvfile, delimiter=';', quotechar='|')
				for i, row in enumerate(fileReader):
					if i == 0: self.nbFields = len(row) # The size is set by the header of the word list
					if (i in range(self.startIdx, self.endIdx)) or (i == 0 and self.startIdx != 0 ):
						row = removeNullString(row)
						if row == []: continue
						row = self.normaliseListWidth(row)
						for idx in self.columnToFilter:
							if idx >= len(row): continue
							row.pop(idx)
							print("poping ", row, idx)
						print(row)
						self.wordsList.append(row)
						self.nbWordSerie += 1
				assert len(self.wordsList) > 1
				self.titleList = self.wordsList.pop(0)
				self.endIdx -= 1
		except OSError: # 'File not found' error message.
			print("File not found")

	def saveConf(self):
		fileName = "configuration.txt"
		data = str(self.nbFields)+" - "\
		       +str(self.columnToFilter)+" - "\
		       +str(self.endIdx)+" - "\
		       +str(self.startIdx)+" - "\
		       +str(self.nbQuestions)+" - "\
		       +str(self.nbClickValidMax)+" - "\
		       +str(self.withAnswer)
		saveFile(fileName, data)

	def openConf(self):
		data = openFile(fileName="configuration.txt")
		dumpStructure =  data.split(" - ")
		assert len(dumpStructure) == 7
		self.nbFields = int(dumpStructure[0])
		if len(dumpStructure[1]) > 2:
			for value in dumpStructure[1][1:-1].split(","):
				self.columnToFilter.append(int(value))
		else:
			self.columnToFilter = []
		self.endIdx = int(dumpStructure[2])
		self.startIdx = int(dumpStructure[3])
		self.nbQuestions = int(dumpStructure[4])
		self.nbClickValidMax = int(dumpStructure[5])
		self.withAnswer = True if dumpStructure[6] == "True" else False


	def normaliseListWidth(self, myList):
		assert self.nbFields > 0 # should at least have one element in the list
		assert len(myList) >= self.nbFields # impossible to have less than the nb max of rows
		result = []
		if len(myList) > self.nbFields:
			for idx in range(0, self.nbFields):
				assert isinstance(myList[idx], str)
				result.append(myList[idx])
			for idx in range(self.nbFields, len(myList)):
				assert isinstance(myList[idx], str)
				result[-1] += myList[idx]
			return result
		else:
			return myList


class MainWindow(QMainWindow):

	def __init__(self, conf, parent=None):
		super(MainWindow, self).__init__(parent)
		self.theWidget = Widget(self, conf)
		_widget = QWidget()
		_layout = QVBoxLayout(_widget)
		_layout.addWidget(self.theWidget)
		self.theLayout = _layout
		self.setCentralWidget(_widget)
		self.conf = conf
		self.initUI()

	def initUI(self):
		#####################
		# Exit menu    #
		#####################
		exitAction = QAction(QIcon('exit.png'), 'Exit Ctrl+Q', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.triggered.connect(qApp.quit)
		self.toolbar = self.addToolBar('Exit')
		self.toolbar.addAction(exitAction)

		#####################
		# File open menu    #
		#####################
		openFileAction = QAction(QIcon('openFile.png'), 'Open File Ctrl+O', self)
		openFileAction.setShortcut('Ctrl+O')
		openFileAction.triggered.connect(self.showOpenFileMenu)
		self.toolbar = self.addToolBar('Open File')
		self.toolbar.addAction(openFileAction)

		######################
		# Configuration menu #
		######################
		def showConfigurationMenu():
			dialog = QDialog()
			widget = QWidget(dialog)
			self.truc = widget
			layout = QHBoxLayout(widget)
			self.widgetSpinBoxes = {
				"Filter" : SpinBox("Filter" , self.conf, 0, 5   ),
				"Click"  : SpinBox("Click"  , self.conf, 0, 5   ),
				"Row min": SpinBox("Row min", self.conf, 0, None),
				"Row max": SpinBox("Row max", self.conf, 0, 100 ),
				"Nb Q"   : SpinBox("Nb Q"   , self.conf, 1, 50  ),
				"Check answer": CheckBox("With answer", self.conf, dialog)}
			for k, v in sorted(self.widgetSpinBoxes.items()):
				layout.addWidget(v)
			widget.adjustSize()
			dialog.setWindowTitle("Configuration tool")
			dialog.setWindowModality(Qt.ApplicationModal)
			dialog.exec_()
		configurationAction = QAction(QIcon('config.png'), 'Configuration tool Ctrl+K', self)
		configurationAction.setShortcut('Ctrl+K')
		configurationAction.triggered.connect(showConfigurationMenu)
		self.toolbar = self.addToolBar('Configuration tool')
		self.toolbar.addAction(configurationAction)

		self.setWindowTitle('Verben Prünfung')
		self.setWindowIcon(QIcon('germanFlag.jpg'))
		self.center()
		self.show()

	def showOpenFileMenu(self):
		fileName = QFileDialog.getOpenFileName(self, 'Open file', '/home/pierre/PycharmProjects/Verben','Coma separated value files (*.csv)')
		if fileName[0]:
			for i in range(len(self.theWidget.stats.stats)):
				self.theWidget.stats.stats[i].deleteLater()
			for i in range(len(self.theWidget.solution)):
				self.theWidget.solution.pop(-1)
			for i in range(len(self.theWidget.userSolution)):
				self.theWidget.userSolution[i].deleteLater()
			while self.theWidget.userSolution:
				self.theWidget.userSolution.pop(-1)
			for i in range(len(self.theWidget.guiSolution)):
				self.theWidget.guiSolution[i].deleteLater()
			while self.theWidget.guiSolution:
				self.theWidget.guiSolution.pop(-1)
			while self.theWidget.grid.count():
				item = self.theWidget.grid.takeAt(0)
				item.widget().deleteLater()
			while self.theLayout.count():
				item = self.theLayout.takeAt(0)
				if item.widget() is None: continue
				item.widget().deleteLater()
			conf = self.conf
			conf.__init__()
			conf.openCsvFile(fileName[0])
			self.__init__(conf)

	def center(self):
		frameGm = self.frameGeometry()
		screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
		centerPoint = QApplication.desktop().screenGeometry(screen).center()
		frameGm.moveCenter(centerPoint)
		self.move(frameGm.topLeft())

def main():
	conf = Configuration()
	conf.openCsvFile(fileName='Tieren Deutsch.csv')
	# Step 1 : Creation of the application
	app = QApplication(sys.argv)
	# Step 2 : Creation of the main window
	myMainWindow = MainWindow(conf)
	myMainWindow.show()
	# Step 3 : Preparing the exit
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()