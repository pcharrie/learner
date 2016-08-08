#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QInputDialog, QDesktopWidget, QGridLayout, QAction
from PyQt5.QtCore    import pyqtSignal, pyqtSlot, Qt, QObject
from PyQt5.QtGui     import QKeyEvent, QIcon

from stats import Stats
from values import *
from myWidgets import LineEdit, MyProgressBar

import sys
import random

from log import printLog

class Communicate(QObject):
	validTrig = pyqtSignal()

class MyWindow(QWidget):
	solution = []  # The list of string with the word solution
	guiSolution = []  # The answer in case of mistakes
	userSolution = []  # What the user has texted
	nbClickValid = 0
	grid = QGridLayout() # gridLayout
	stats = Stats(3)
	isFinished = False

	def __init__(self, conf):
		super().__init__()
		self.conf = conf
		self.initUI()

	def initUI(self):
		#####################
		# Windows           #
		#####################
		self.setTitle()
		self.center()
		self.setWindowTitle('Verben Prünfung')
		self.setWindowIcon(QIcon('germanFlag.jpg'))
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
		key = event.key()+1
		if key == Qt.Key_Enter:
			if not self.isFinished:
				self.validAction.validTrig.emit()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def setTitle(self):
		assert len(self.conf.wordsList) > 0
		titleList = self.conf.wordsList.pop(0)
		for row, t in enumerate(titleList):
			if row >= NB_MAX_ROW: continue
			labelTitle = QLabel(self)
			labelTitle.setText(t)
			userAnswer = LineEdit(self)
			self.userSolution.append(userAnswer.member)
			self.grid.addWidget(userAnswer.member, row, 1)
			self.grid.addWidget(labelTitle, row, 0)
		self.createQuestion()

	def chooseSerie(self):
		random.seed()
		print("weight list", self.stats.weightList)
		idx = random.choice(self.stats.weightList)
		serieChosen = self.conf.wordsList[idx]
		return serieChosen

	def createQuestion(self):
		serieChosen = self.chooseSerie()
		for i, s in enumerate(serieChosen):
			answer = QLabel(self)
			answer.setText("")
			self.guiSolution.append(answer)
			self.solution.append(s)
			self.grid.addWidget(answer, i, 2)
		self.setQuestion(serieChosen)

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
		print()
		self.erase()
		if self.conf.question >= self.conf.nbQuestions:
			self.isFinished = True
		if not self.isFinished:
			self.conf.question += 1
			self.stats.updateStats(self.conf)
			if self.conf.wordsList != []:
				serieChosen = self.chooseSerie()
				for i, s in enumerate(serieChosen):
					if i != 0: self.guiSolution[i].setText(s)
					self.solution[i] = s
					self.userSolution[i].setEnabled(True)
				self.setQuestion(serieChosen)
		else:
			self.finishGame()

	def setQuestion(self, serieChosen):
		indexChosen = 0  # random.randint(0, len(serieChosen)-1)
		wordChosen = serieChosen[indexChosen]
		self.guiSolution[0].setText(wordChosen)
		qLineQuestion= self.userSolution[indexChosen]
		qLineQuestion.setText(wordChosen)
		qLineQuestion.setEnabled(False)
		qLineQuestion.setStyleSheet("""QLineEdit { background-color: white; color: green }""")
		self.grid.addWidget(qLineQuestion, 0, 1)

	def isApproximatelyCorrect(self, caseN):
		isGood = False
		solution = []
		solution.extend(self.solution[caseN].split(","))
		solution.extend(self.solution[caseN].split(" "))
		if self.userSolution[caseN].text() not in solution:
			isGood = True
		return isGood

	def erase(self):
		for i in range(len(self.solution)):
			self.userSolution[i].setStyleSheet(
				"""QLineEdit { background-color: white; color: black }""")
			self.userSolution[i].setText("")
			self.guiSolution[i].setText("")

	def areAllCorrectAnswers(self):
		allGood = True
		for caseN in range(1, len(self.solution)):
			isGood = True
			if caseN != 3:
				if self.userSolution[caseN].text() != self.solution[caseN]:
					isGood = False
					if self.userSolution[caseN].text() != "":
						self.userSolution[caseN].setStyleSheet("""QLineEdit { background-color: white; color: red }""")
					self.guiSolution[caseN].setText(self.solution[caseN])
					allGood = False
			elif (caseN == 3):  # One of the word is correct is count as a right answer
				if self.isApproximatelyCorrect(caseN):
					isGood = False
					if self.userSolution[caseN].text() != "":
						self.userSolution[caseN].setStyleSheet("""QLineEdit { background-color: white; color: red }""")
					self.guiSolution[caseN].setText(self.solution[caseN])
					allGood = False
			if isGood:
				self.userSolution[caseN].setStyleSheet("""QLineEdit { background-color: white; color: green }""")
				self.userSolution[caseN].setEnabled(False)
				self.guiSolution[caseN].setText("")
		return allGood

	def valid(self):
		if self.isFinished: return
		assert len(self.solution) == len(self.userSolution)
		assert len(self.solution) == len(self.guiSolution)
		self.nbClickValid += 1
		print("nb click valid", self.nbClickValid)
		allGood = self.areAllCorrectAnswers()
		if allGood:
			print("case a")
			self.nbClickValid = 0
			self.stats.delWordFromHistogram(self.solution[0], self.conf.wordsList)
			self.conf.nbCorrectAnswer = 3
			self.conf.schlem += 1
			self.nextQuestion()
		elif self.nbClickValid == self.conf.nbClickValidMax:  # nb of tries
			self.nbClickValid = 0
			self.conf.nbCorrectAnswer = 0
			self.stats.addWordToHistogram(self.solution, self.conf.wordsList)
			self.nextQuestion()
		else:
			print("case c")
			self.conf.nbCorrectAnswer = 0
			self.conf.schlem = 0

	def finishGame(self):
		self.stats.saveStats()
		self.stats.dumpHistogram()
		for i in range(1, len(self.solution)):
			self.userSolution[i].setEnabled(False)
			self.guiSolution[i].setText("")
		print("End of game")
		sys.exit()




