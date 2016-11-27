#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QDesktopWidget, QGridLayout, QFileDialog
from PyQt5.QtCore    import pyqtSignal, Qt, QObject
from PyQt5.QtGui     import QIcon

from stats import Stats
from values import *
from myWidgets import LineEdit, MyProgressBar

import sys
import random

class Communicate(QObject):
	validTrig = pyqtSignal()

class CommunicateOpening(QObject):
	opening = pyqtSignal()

class MyWindow(QWidget):
	solution = []  # The list of string with the word solution
	guiSolution = []  # The answer in case of mistakes
	userSolution = []  # What the user has texted
	nbClickValid = 0
	grid = QGridLayout() # gridLayout
	isFinished = False

	def __init__(self, conf):
		super().__init__()
		self.indexChosen = 0
		self.conf = conf
		self.stats = Stats(self.conf.startIdx, self.conf.endIdx, self.conf.wordsList)
		self.initUI()

	def initUI(self):
		#####################
		# Windows           #
		#####################
		self.center()
		self.setWindowTitle('Verben Prünfung')
		self.setWindowIcon(QIcon('germanFlag.jpg'))
		#####################
		# File open menu    #
		#####################
		self.openingAction = CommunicateOpening()
		self.openingAction.opening.connect(self.showDialog)
		#####################
		# Title menu        #
		#####################
		self.setTitle()
		#####################
		# Button validation #
		#####################
		self.validAction = Communicate()
		self.validAction.validTrig.connect(self.valid)

		self.pushButtonValid = QPushButton(self)
		self.pushButtonValid.setText("Valid")
		self.pushButtonValid.setDefault(True)
		self.pushButtonValid.setAutoDefault(True)

		self.grid.addWidget(self.pushButtonValid, 30, 0, 10, 3)
		self.pushButtonValid.clicked.connect(self.valid)

		self.createStatsArea()
		self.setLayout(self.grid)
		self.grid.setSpacing(10)

	def keyPressEvent(self, event):
		key = event.key()
		if key == Qt.Key_Enter-1:
			if not self.isFinished:
				self.validAction.validTrig.emit()
		if key == Qt.Key_O:
			self.openingAction.opening.emit()

	def showDialog(self):
		fileName = QFileDialog.getOpenFileName(self, 'Open file', '/home')
		if fileName[0]:
			self.conf.openCsvFile(fileName[0])

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def setTitle(self):
		assert len(self.conf.wordsList) > 0
		titleList = self.conf.wordsList.pop(0)
		self.conf.endIdx -= 1
		for row, t in enumerate(titleList):
			if row >= NB_MAX_ROW: continue
			labelTitle = QLabel(self)
			labelTitle.setText(t)
			userAnswer = LineEdit(self)
			self.userSolution.append(userAnswer.member)
			self.grid.addWidget(userAnswer.member, row, 1)
			self.grid.addWidget(labelTitle, row, 0)
		self.createQuestion()

	def createQuestion(self):
		serieChosen = self.chooseSerie()
		for i, s in enumerate(serieChosen):
			answerQtLabel = QLabel(self)
			answerQtLabel.setText("")
			self.guiSolution.append(answerQtLabel)
			self.solution.append(s)
			self.grid.addWidget(answerQtLabel, i, 2)
		self.setQuestion(serieChosen)

	def chooseSerie(self):
		random.seed()
		idx = random.choice(self.stats.weightList)
		serieChosen = self.conf.wordsList[idx]
		return serieChosen

	def setQuestion(self, serieChosen):
		self.indexChosen = 0  # random.randint(0, len(serieChosen)-1)
		wordChosen = serieChosen[self.indexChosen]
		qLineQuestion= self.userSolution[self.indexChosen]
		qLineQuestion.setText(wordChosen)
		qLineQuestion.setEnabled(False)
		qLineQuestion.setStyleSheet(waitResult)
		self.grid.addWidget(qLineQuestion, 0, 1)

	def createStatsArea(self):
		nbPercCorrectAnswerGui      = MyProgressBar(self)
		nbConsecutivesCorrectAnswer = QLabel(self)
		progress                    = MyProgressBar(self)
		self.stats.stats = [nbPercCorrectAnswerGui, nbConsecutivesCorrectAnswer, progress]
		for i, e in enumerate(self.stats.stats):
			if i == 0: self.grid.addWidget(e, 10, 0, 4, 3)
			if i == 1: self.grid.addWidget(e, 14, 0, 6, 3)
			if i == 2: self.grid.addWidget(e, 20, 0, 8, 3)
		a = QLabel(self)
		a.setText("  ")
		self.stats.updateStats(self.conf)

	def nextQuestion(self):
		self.erase()
		if self.conf.question >= self.conf.nbQuestions:
			self.isFinished = True
		if not self.isFinished:
			self.conf.question += 1
			self.stats.updateStats(self.conf)
			self.conf.nbCorrectAnswer = 0
			if self.conf.wordsList != []:
				serieChosen = self.chooseSerie()
				for i, s in enumerate(serieChosen):
					if i != self.indexChosen and self.nbClickValid != 0: self.guiSolution[i].setText(s)
					self.solution[i] = s
					self.userSolution[i].setEnabled(True)
				self.setQuestion(serieChosen)
		else:
			self.finishGame()

	def erase(self):
		for i in range(len(self.solution)):
			self.userSolution[i].setStyleSheet(waitResult)
			self.userSolution[i].setText("")
			self.guiSolution[i].setText("")

	# One of the word is correct is count as a right answer
	def isApproximatelyCorrect(self, caseN):
		solution = []
		solution.extend(self.solution[caseN].split(","))
		solution.extend(self.solution[caseN].split(" "))
		return self.userSolution[caseN].text() in solution

	def areAllCorrectAnswers(self):
		nbBadAnswer = 0
		idxQuestion = 1
		nbMaxCase = 3
		for caseN in range(idxQuestion, len(self.solution)):
			conditionA = ((caseN != nbMaxCase) and (self.userSolution[caseN].text() != self.solution[caseN]))
			conditionB = ((caseN == nbMaxCase) and (not self.isApproximatelyCorrect(caseN)))
			if conditionA or conditionB:
				nbBadAnswer += 1
				if self.userSolution[caseN].text() != "":
					self.userSolution[caseN].setStyleSheet(badResult)
				self.guiSolution[caseN].setText(self.solution[caseN])
			else:
				self.userSolution[caseN].setStyleSheet(goodResult)
				self.userSolution[caseN].setEnabled(False)
				self.guiSolution[caseN].setText("")
		return nbBadAnswer

	def valid(self):
		if self.isFinished: return
		if len(self.solution) != len(self.userSolution):
			for e in self.solution:	print(e)
			for e in self.userSolution: print(e)
		assert len(self.solution) == len(self.userSolution)
		assert len(self.solution) == len(self.guiSolution)
		self.nbClickValid += 1
		nbBadAnswer = self.areAllCorrectAnswers()
		if nbBadAnswer == 0:
			self.nbClickValid = 0
			self.stats.delWordFromHistogram(self.solution[0], self.conf.wordsList)
			self.conf.schlem += 1
			self.conf.nbCorrectAnswer += self.conf.nbFields - nbBadAnswer
			self.nextQuestion()
		elif self.nbClickValid == self.conf.nbClickValidMax:  # nb of tries
			self.nbClickValid = 0
			self.stats.addWordToHistogram(self.solution[0], self.conf.wordsList)
			self.conf.nbCorrectAnswer += self.conf.nbFields - nbBadAnswer
			self.nextQuestion()
		else:
			self.conf.schlem = 0

	def finishGame(self):
		self.stats.saveStats()
		self.stats.dumpHistogram()
		for i in range(1, len(self.solution)):
			self.userSolution[i].setEnabled(False)
		print("End of game")
		sys.exit()




