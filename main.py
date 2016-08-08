#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import csv
from graphicUnit import MyWindow
from PyQt5.QtWidgets import QApplication

class Configuration():
	nbWordSerie   = 0
	question      = 1
	nbCorrectAnswer = 0
	nbQuestions   = 3
	schlem        = 0
	max_word_size = 20
	startIdx      = 0
	endIdx        = 4
	userName      = "pierre"
	columnToFilter= [2]
	nbColumns     = 3
	nbRows        = 5
	nbClickValidMax = 2


	def __init__(self):
		self.wordsList = []
		self.nbFields = 3

	def openCsvFile(self, fileName):
		try:
			with open(fileName, newline='\n', encoding='iso-8859-1',errors='ignore') as csvfile:
				fileReader = csv.reader(csvfile, delimiter=';', quotechar='|')
				for i, row in enumerate(fileReader):
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

