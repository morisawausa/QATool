# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *

class OCC_QATaskView():

	def __init__(self):
		print "QATaskView constructor called"
		self.task = None
		self.report = list()
		self.updating = False


	def set_task(self, task):
		"""Set the selected task in taskview"""
		self.task = task
		return self

	def render(self):
		return "\n".join(['%s : %s' % (key, value) for (key, value) in self.task.details().items()])


	def render_task_report(self, task):
		self.report = task.start(dict())
		print "-------------------------------------------------------","\n", self.report
		return self

	def render_task_parameters(self):
		return self