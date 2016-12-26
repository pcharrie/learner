#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv


def belong2wordList(word, ListOfwordList):
	for wordSet in ListOfwordList:
		if word in wordSet: return True
	return False

class Stats():
	stats = []
	histogram = {}
	activate = True
	successRate = 100

	def __init__(self, infEdge, supEdge, wordsList):
		if supEdge >= len(wordsList): supEdge = len(wordsList) - 1
		self.weightList = [i-infEdge for i in range(infEdge, supEdge)]
		self.loadHistogram()
		self.updateWeightList(wordsList)
		print("Histogram:")
		for k, v in sorted(self.histogram.items()):
			print(k, v)
		print()

	def updateStats(self, conf):
		progressRate =  0
		if conf.question != 0:
			success = (float(conf.nbCorrectAnswer) / float(conf.nbFields)) * float(100)
			if conf.question == 1:success = float(100)
			sR = self.successRate
			self.successRate = (sR + success) / float(2)
		if conf.nbQuestions != 0:
			progressRate = int((float(conf.question)/float(conf.nbQuestions))*100)
		self.stats[0].setValue(self.successRate)
		self.stats[1].setText("Without mistake: " + str(conf.schlem))
		self.stats[2].setValue(progressRate)

	def saveStats(self):
		fileName = "stats.txt"
		statsFile = open(fileName, "a+")
		data = str(self.successRate)+"\n"
		statsFile.write(data)
		statsFile.close()

	def dumpHistogram(self):
		fileName = "histogram.txt"
		f = open(fileName, 'w+', encoding='iso-8859-1')
		for k,v in self.histogram.items():
			data = str(k)+":"+str(v)+"\n"
			f.write(data)
		f.close()

	def loadHistogram(self):
		fileName = "histogram.txt"
		try:
			with open(fileName, newline='\n', encoding='iso-8859-1',errors='ignore') as csvfile:
				fileReader = csv.reader(csvfile, delimiter=':', quotechar=';')
				for i, data in enumerate(fileReader):
					word = data[0]
					weight = int(data[1])
					self.histogram.update({word:weight})
		except OSError: # 'File not found' error message.
			print("File not found")

	def updateWeightList(self, wordList):
		for word, weight in self.histogram.items():
			if belong2wordList(word, wordList):
				idx = self.getIdxFrom(word, wordList)
				for _ in range(weight):
					self.weightList.append(idx)

	def addWordToHistogram(self, word, wordList):
		idx = self.getIdxFrom(word, wordList)
		self.weightList.append(idx)
		if word in self.histogram:
			if self.histogram[word] <= 20:
				self.histogram[word] += 1
		else:
			self.histogram.update({word: 1})

	def delWordFromHistogram(self, word, wordList):
		if word in self.histogram.keys():
			if self.histogram[word] > 0:
				self.histogram[word] -= 1
				idx = self.getIdxFrom(word, wordList)
				self.weightList.pop(idx)
				return

	def getIdxFrom(self, word, wordList):
		for i, serie in enumerate(wordList):
			if word == serie[0]:
				return i
		raise SystemError("Word was not found "+str(word))

