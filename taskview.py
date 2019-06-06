# -*- coding: utf-8 -*-

from GlyphsApp import *
from vanilla import *

class OCC_QATaskView():

	def __init__(self):
		self.task = None
		self.report = list()


	def set_task(self, task):
		"""Set the selected task in taskview"""
		self.task = task
		return self


	def render(self):
		"""Populates the task details in taskview"""
		return self.task.details()['name'] + " (v" + self.task.details()['version'] + ")\n" + self.task.details()['description']


	def render_task_parameters(self):
		"""Populates the task parameters in parameterview"""
		return self.task.parameters()


	# def render_task_report(self, task):
	# 	self.errors = {}
	# 	#set up placeholder list of errors for each glyph
	# 	for g in Glyphs.font.glyphs:
	# 		key = g.name.encode('utf-8')
	# 		self.errors[key] = list()

	# 	self.report = task.start(task.parameters())
	# 	print "\n\n\n", name, "\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n", self.report
	# 	print self.report
	# 	return self


