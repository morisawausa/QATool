# -*- coding: utf-8 -*-
import objc
import os
import importlib
from GlyphsApp import *
from vanilla import *

class QAPool():

	def __init__(self):
		print "QAPool constructor called"
		self.tasks = dict()
		self.update_tasks()

	def update_tasks(self):
		"""reads filelist of QATasks and loads the contents of the 
		scripts directory as a series of QATasks. TODO: Records an error 
		if any of the QATasks are missing a name"""
		files = os.listdir('scripts')

		for file in files:
			if file.endswith(".py") and "__init__" not in file:
				mod = importlib.import_module( 'scripts.' + file.split('.')[0] )
				class_name = getattr(mod, 'Script')
				task = class_name()
				task_name = task.details()['name']
				# add check if details includes name
				self.tasks[task_name] = task

		print "QA Pool, self.tasks", self.tasks

		return self