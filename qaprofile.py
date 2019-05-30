# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *
import os
import importlib

from taskview import OCC_QATaskView

class QAProfile():
	"""The QAProfile class manages which tasks are activated 
	and which are inactive, as well as defining custom 
	parameters for the typeface."""

	def __init__(self):
		"""Set up our dictionary of tasks that stores the tasks, its states, and parameters"""
		self.tasks = dict()
		self.load_scripts()
		self.task_view = OCC_QATaskView()


	def load_scripts(self):
		"""Load .py files in the 'scripts' directory as a series of QATasks. TODO: Records an error 
		if any of the QATasks are missing a name"""
		files = os.listdir('scripts')

		for file in files:
			if file.endswith(".py") and "__init__" not in file:
				mod = importlib.import_module( 'scripts.' + file.split('.')[0] )
				class_name = getattr(mod, 'Script')
				test = class_name()
				task_name = test.details()['name']
				self.tasks[task_name] = dict([('Script',test), ('State', False), ('Parameters', dict())])
				# append script to list of tasks
		return self


	def run(self):
		"""Given a pool of available tasks, run the tasks 
		specified in pool and report the result. """	
		for task in self.tasks:
			task_obj = self.tasks[task]
			if task_obj['State'] is True:
				self.task_view.render_task_report(self.tasks[task]['Script'])


	def save(self):
		"""Save the currently specified QATask parameters to 
		the current font's customParameters fields."""
		return self


	def load(self):
		"""Load the parameters for the specified QATasks to 
		from the current font's customParameters fields."""
		return self


	def toggle(self, task_name):
		"""Toggle the active state of a given task"""
		self.tasks[ task_name ]['State'] = not self.tasks[ task_name ]['State']
		print 'toggle state', task_name
		return self

