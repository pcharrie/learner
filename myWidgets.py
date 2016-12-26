#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QWidget, QCheckBox, QVBoxLayout, \
	QLabel, QSpinBox, QProgressBar

class LineEdit(QLineEdit):

	def __init__(self, obj):
		super().__init__()
		self.member = QLineEdit(obj)

	def __getitem__(self, index):
		return self.member[index]

	def __setitem__(self, index, value):
		self.member[index] = value


class CheckBox(QWidget):

	def __init__(self, name, conf, parent=None):
		super(CheckBox, self).__init__(parent)
		self.conf = conf
		layout = QVBoxLayout()
		self.b1 = QCheckBox(name)
		self.b1.setChecked(self.conf.withAnswer)
		self.b1.stateChanged.connect(lambda: self.btnstate(self.b1))
		layout.addWidget(self.b1)
		self.setLayout(layout)

	def btnstate(self, b):
		if b.text() == "With answer":
			self.conf.withAnswer = b.isChecked()
			self.conf.saveConf()

class SpinBox(QWidget):

	def __init__(self, name, conf, min, max, parent=None):
		super(SpinBox, self).__init__(parent)
		self.conf = conf
		layout = QVBoxLayout()
		self.l = QLabel(name)
		self.l.setAlignment(Qt.AlignCenter)
		layout.addWidget(self.l)
		self.sp = QSpinBox()
		if self.l.text() == "Filter":
			if len(self.conf.columnToFilter):
				self.sp.setValue(self.conf.columnToFilter[0])
		if self.l.text() == "Click":
			self.sp.setValue(self.conf.nbClickValidMax)
		if self.l.text() == "Row min":
			self.sp.setValue(self.conf.startIdx)
		if self.l.text() == "Row max":
			self.sp.setValue(self.conf.endIdx)
		if self.l.text() == "Nb Q":
			self.sp.setValue(self.conf.nbQuestions)
		if min is None:
			self.sp.setMaximum(max)
		elif max is None:
			self.sp.setMinimum(min)
		else:
			self.sp.setRange(min, max)
		layout.addWidget(self.sp)
		self.sp.valueChanged.connect(self.valuechange)
		self.setLayout(layout)

	def valuechange(self):
		if self.l.text() == "Filter":
			self.conf.columnToFilter = [self.sp.value()]
		if self.l.text() == "Click":
			self.conf.nbClickValidMax = self.sp.value()
		if self.l.text() == "Row min":
			self.conf.startIdx = self.sp.value()
		if self.l.text() == "Row max":
			self.conf.endIdx = self.sp.value()
		if self.l.text() == "Nb Q":
			self.conf.nbQuestions = self.sp.value()
		self.conf.saveConf()


DEFAULT_STYLE = """
QProgressBar{
    border: 1px;
    border-radius: 1px;
    height: 1px;
    text-align: center
}

QProgressBar::chunk {
    width: 1px;
    margin: 1px;
}
"""

COMPLETED_STYLE = """
QProgressBar{
    border: 1px solid grey;
    border-radius: 1px;
    height: 1px;
    text-align: center
}

QProgressBar::chunk {
    background-color: red;
    width: 5px;
    margin: 1px;
}
"""

class MyProgressBar(QProgressBar):

    def __init__(self, parent = None):
        QProgressBar.__init__(self, parent)
        #self.setStyleSheet(DEFAULT_STYLE)

    def setValue(self, value):
	    QProgressBar.setValue(self, value)
	    #if value == self.maximum():
		#    self.setStyleSheet(COMPLETED_STYLE)