# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *

class OCC_QATaskListView():
	def __init__(self):
		print "QA Task List View constructor called"
		self.pool = Null
		self.profile = Null
		self.selected_task = Null

	def run_profile(self):
		"""looks at current profile and runs all tasks"""
		pass

	def run_single_task(self, task):
		"""given a QATask, execute that task"""
		pass

	def render(self):
		"""draw entire application"""
		pass

	def select_task(self, task):
		"""given a QATask, render that information to OCC_QATaskView"""
		pass

	def update_task_list(self):
		"""upon activation or deactivation of QATask, update tasklist"""
		pass

	def activate_task(self, task):
		pass

	def deactivate_atask(self, task):
		pass

