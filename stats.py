#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

class Stats():
	stats = []
	histogram = {}
	activate = True
	successRate = 100


	def __init__(self, nbQuestions):
		self.weightList = [i for i in range(nbQuestions)]

	def updateStats(self, conf):
		successRate = 0
		progressRate =  0
		if conf.question != 0:
			print(conf.nbCorrectAnswer, conf.question)
			success = float(conf.nbCorrectAnswer) / float(conf.nbFields) * float(100)
			if conf.question == 1: success = float(100)
			self.successRate = (self.successRate + success) / float(2)
		if conf.nbQuestions != 0:
			progressRate = int((float(conf.question-1)/float(conf.nbQuestions))*100)
		self.stats[0].setValue(self.successRate)
		self.stats[1].setText("Without mistake: " + str(conf.schlem))
		self.stats[2].setValue(progressRate)

	def saveStats(self):
		statsFile = open("stats.txt", "a")
		res = ""
		for e in self.stats:
			res += str(e.text()) + "\n"
		res += "\n"
		statsFile.write(res)
		statsFile.close()

	def dumpHistogram(self):
		f = open("histogram.txt", "w")
		f.write(str(self.histogram))
		f.close()

	def addWordToHistogram(self, word, wordList):
		idx = self.getIdxFrom(word[0], wordList)
		self.weightList.append(idx)
		if word[0] in self.histogram:
			self.histogram[word[0]] += 1
		else:
			self.histogram.update({word[0]: 1})

	def delWordFromHistogram(self, word, wordList):
		if word in self.histogram:
			if self.histogram[word] > 0:
				self.histogram[word] -= 1
				print("before", self.weightList)
				for i, e in enumerate(self.weightList):
					if e == word:
						self.weightList.pop(i)
						print("after", self.weightList)
						return



	def getIdxFrom(self, word, wordList):
		for i, serie in enumerate(wordList):
			if word == serie[0]:
				return i
		return None


	def openHistogram(self):
		fileName = "histogram.txt"
		try:
			with open(fileName, newline='\n', encoding='iso-8859-1',errors='ignore') as csvfile:
				fileReader = csv.reader(csvfile, delimiter=';', quotechar=':')
				for i, row in enumerate(fileReader):
					if i in range(self.startIdx, self.endIdx):
						for idx in self.columnToFilter:
							row.pop(idx)
						self.histogram.update(row)
		except OSError: # 'File not found' error message.
			print("File not found")
