# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *

from line import QALine

class QAReport():

	def __init__(self, task):
		print "QAReport constructor called"
		self.passed = None
		self.number_passed = 0
		self.number_failed = 0
		self.task = task
		self.lines = list()


	def add(self, header, desc, passed=None):
		"""Adds line of task test information to report.
		passed=None for general reporting, default value
		passed=True for successful tests
		passed=False for failed tests
		"""
		line = QALine(passed, header, desc)
		self.lines.append(line)
		return self

	def finalize(self):
		"""Update QAReport after running test and return QAReport
		If all tasks neither pass nor fail, returns a general report.
		If any task has failed, returns fail.
		If all tasks succeed, returns pass.
		"""
		for line in self.lines:
			if line.passed is not None:
				
				self.passed = self.passed and line.passed
				
				if line.passed:
					self.number_passed +=1
				else:
					self.number_failed +=1

		return self

	def print(self):
		for line in self.lines:
			if line.passed is None:
				output = "Note"
			elif line.passed is True:
				output = "Yaas"
			else:
				output = "Oops"
			output += '\t' + line.header + '\t' + line.desc + '\n'

		print output
		return self


