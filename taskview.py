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



