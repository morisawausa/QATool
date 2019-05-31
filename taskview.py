# -*- coding: utf-8 -*-
import objc
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
		return self.task.details()['name'] + " (v" + self.task.details()['version'] + ")\n" + self.task.details()['description']


	def render_task_parameters(self):
		return self.task.parameters()


	def render_task_report(self, task):
		font = Glyphs.font
		name = font.familyName
		self.report = task.start(task.parameters())
		print "\n\n\n", name, "\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n", self.report
		return self


