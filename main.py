#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
from graphicUnit import MyWindow
from PyQt5.QtWidgets import QApplication

class Configuration():
	nbWordSerie   = 0 # wr
	question      = 1 # wr/rd
	nbCorrectAnswer = 0 #
	nbQuestions   = 10 # rd
	schlem        = 0 # wr
	startIdx      = 1 # rd
	endIdx        = 8 # wr
	columnToFilter= [4]
	nbClickValidMax = 2 # rd

	def __init__(self):
		self.wordsList = []
		self.nbFields = 3 # variable

	def openCsvFile(self, fileName):
		try:
			with open(fileName, newline='\n', encoding='iso-8859-1',errors='ignore') as csvfile:
				fileReader = csv.reader(csvfile, delimiter=';', quotechar='|')
				for i, row in enumerate(fileReader):
					if (i in range(self.startIdx, self.endIdx)) or (i == 0 and self.startIdx != 0 ):
						for idx in self.columnToFilter:
							print(row, idx)
							row.pop(idx)
						self.wordsList.append(row)
						self.nbWordSerie += 1
		except OSError: # 'File not found' error message.
			print("File not found")

def main():
	conf = Configuration()
	conf.openCsvFile(fileName='Sex.csv')
	# Step 1 : Creation of the application
	app = QApplication(sys.argv)
	# Step 2 : Creation of the widget
	win = MyWindow(conf)
	win.show()
	# Step 3 : Preparing the exit
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

# set menu to load file
# set menu to configure columnToFilter, nbClickMax, startIdx, endIdx, nbQuestions, ..
# fix bug with stranges character and spaces
# take off the answer of the selected index
# variate indexChosen value
# solution print just before the last try and tick menu to disable