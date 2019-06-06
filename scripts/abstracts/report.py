# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *

from line import QALine

class QAReport( ):

	def __init__(self, task):
		self.passed = None
		self.number_passed = 0
		self.number_failed = 0
		self.task = task
		self.task_name = task.details()['name']
		self.notes = []	
		self.results = dict()


	def add(self, master, glyph, header, desc, passed):
		"""Adds line of a single test result to report.
		"""
		glyphName = glyph.encode('utf-8')
		masterName = master.encode('utf-8')

		result = {'glyph': glyphName, 'header': header, 'desc': desc, 'pass': passed }
		
		# collect results by master
		if masterName in self.results:
			self.results[masterName].append(result)
		else:
			self.results[masterName] = list()
			self.results[masterName].append(result)
		return self


	def note(self, message):
		"""Adds explanatory descriptors to report.
		"""
		self.notes.append(message)
		return self


	def node(self, GSnode):
		"""Formats GS Node into human-readable point coordinates"""
		return "(" + str(GSnode.x) + "," + str(GSnode.y) + ")"


	def finalize(self):
		"""Update QAReport after running test and return QAReport.
		"""
		return self.results, self.notes

