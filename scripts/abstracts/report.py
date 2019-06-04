# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *

from line import QALine

class QAReport():

	def __init__(self, task):
		self.passed = None
		self.number_passed = 0
		self.number_failed = 0
		self.task = task
		self.lines = list()
		

	def add(self, desc, passed=None):
		"""Adds line of the task test result to report.
		passed=None for general reporting, default value
		passed=True for successful tests
		passed=False for failed tests
		"""
		self.result = dict()
		self.result['passed'] = passed # test result
		self.result['desc'] = desc # description of result

		self.lines.append(self.result)
		return self


	def finalize(self):
		"""Update QAReport after running test and return QAReport
		If all tasks neither pass nor fail, returns a general report.
		If any task has failed, returns fail.
		If all tasks succeed, returns pass.
		"""
		# for line in self.lines:
		# 	if line.passed is not None:
		# 		self.passed = self.passed and line.passed

		# 		if line.passed:
		# 			self.number_passed +=1
		# 		else:
		# 			self.number_failed +=1

		return self


	def node(self, GSnode):
		"""outputs GS Node into human-readable point coordinates"""
		return "(" + str(GSnode.x) + "," + str(GSnode.y) + ")"


	def master(self, GSmaster):
		"""outputs and formats GS Master into human-readable name"""
		return "\n\n\n---------------------------------------------\n" + GSmaster.name + "\n---------------------------------------------"


	def glyph(self, GSglyph):
		"""formats glyph name for output"""
		return "\n\n" + GSglyph.name + "\n------------"


	def __repr__(self):
		output = self.task.details()['name'] +'\n\n'
		for line in self.lines:
			# if line.passed is None:
			# 	output += "* "
			# # elif line.passed is True:
			# # 	output += "YAS\t\t"
			# # else:
			# 	output += "OOPS\t\t"
			output += line['desc'] + '\n'

		return output
