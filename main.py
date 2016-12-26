#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
from graphicUnit import Widget
from PyQt5.QtWidgets import QApplication, QMainWindow, qApp, QAction, QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtGui     import QIcon

def removeNullString(wordsList):
	result = []
	for word in wordsList:
		if word != "":
			result.append(word)
	return result

class Configuration():
	nbWordSerie   = 0 # wr
	question      = 1 # wr/rd
	nbCorrectAnswer = 0 #
	nbQuestions   = 10 # rd
	schlem        = 0 # wr
	startIdx      = 0 # rd
	endIdx        = 100 # wr number of rows of the file
	columnToFilter= []
	nbClickValidMax = 2 # rd

	def __init__(self):
		self.wordsList = []
		self.nbFields = 3 # variable to know the number of columns of the file

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
							print("poping ",row, idx)
							row.pop(idx)
						print(row)
						self.wordsList.append(row)
						self.nbWordSerie += 1
		except OSError: # 'File not found' error message.
			print("File not found")

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
		self.initUI()
		self.conf = conf

	def initUI(self):
		#####################
		# Exit menu    #
		#####################
		exitAction = QAction(QIcon('exit.png'), 'Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.triggered.connect(qApp.quit)
		self.toolbar = self.addToolBar('Exit')
		self.toolbar.addAction(exitAction)

		#####################
		# File open menu    #
		#####################
		openFileAction = QAction(QIcon('openFile.png'), 'Open File', self)
		openFileAction.setShortcut('Ctrl+O')
		openFileAction.triggered.connect(self.showDialog)
		self.toolbar = self.addToolBar('Open File')
		self.toolbar.addAction(openFileAction)

		self.setWindowTitle('Verben Prünfung')
		self.setWindowIcon(QIcon('germanFlag.jpg'))
		self.setGeometry(300, 300, 300, 200)
		self.show()

	def showDialog(self):
		fileName = QFileDialog.getOpenFileName(self, 'Open file', '/home/pierre/PycharmProjects/Verben','Excel files (*.csv)')
		if fileName[0]:
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
				item.widget().deleteLater()
			conf = Configuration()
			conf.openCsvFile(fileName[0])
			self.theWidget = Widget(self, conf)
			_widget = QWidget()
			_layout = QVBoxLayout(_widget)
			_layout.addWidget(self.theWidget)
			self.theLayout = _layout
			self.setCentralWidget(_widget)

def main():
	conf = Configuration()
	conf.openCsvFile(fileName='Tieren Deutsch.csv') # 'ver.csv')#
	# Step 1 : Creation of the application
	app = QApplication(sys.argv)
	# Step 2 : Creation of the main window
	myMainWindow = MainWindow(conf)
	myMainWindow.show()
	# Step 3 : Preparing the exit
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

# set menu to configure columnToFilter, nbClickMax, startIdx, endIdx, nbQuestions, ..
# fix bug with stranges character and spaces
# take off the answer of the selected index
# variate indexChosen value
# solution print just before the last try and tick menu to disable
# do not put the previous word
# choose vertical or horizontal layout