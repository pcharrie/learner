#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets  import QLineEdit, QProgressBar

class LineEdit(QLineEdit):
	def __init__(self, obj):
		super().__init__()
		self.member = QLineEdit(obj)

	def __getitem__(self, index):
		return self.member[index]

	def __setitem__(self, index, value):
		self.member[index] = value

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