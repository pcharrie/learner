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
	endIdx        = 4 # wr
	columnToFilter= [2]
	nbColumns     = 3 # rd
	nbRows        = 5 # rd
	nbClickValidMax = 2 # rd


	def __init__(self):
		self.wordsList = []
		self.nbFields = 4

	def openCsvFile(self, fileName):
		try:
			with open(fileName, newline='\n', encoding='iso-8859-1',errors='ignore') as csvfile:
				fileReader = csv.reader(csvfile, delimiter=';', quotechar='|')
				for i, row in enumerate(fileReader):
					if i == 0 and self.startIdx != 0:
						for idx in self.columnToFilter:
							row.pop(idx)
						self.wordsList.append(row)
						self.nbWordSerie += 1
					if i in range(self.startIdx, self.endIdx):
						for idx in self.columnToFilter:
							row.pop(idx)
						self.wordsList.append(row)
						self.nbWordSerie += 1
		except OSError: # 'File not found' error message.
			print("File not found")

def main():
	conf = Configuration()
	conf.openCsvFile(fileName='test.csv')
	app = QApplication(sys.argv)
	win = MyWindow(conf)
	win.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

