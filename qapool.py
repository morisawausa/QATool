# -*- coding: utf-8 -*-
import os
from pydoc import locate

import objc
import os
import importlib
from GlyphsApp import *
from vanilla import *

class QAPool():

	def __init__(self):
		print "QAPool constructor called"
		self.tasks = dict()

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
				self.tasks[task_name] = task

		print "QA Pool, self.tasks", self.tasks

		return self

		# self.scripts_module = 'scripts'
		# self.script_class_name = 'Script'
		# self.scripts_dir = os.path.abspath('./' + self.scripts_module )


	# def update_tasks(self):
	# 	"""reads filelist of QATasks and loades the contents of the
	# 	scripts directory as a series of QATasks. Records an err
	# 	or if any of the QATasks are missing a name"""

	# 	def get_running_script_for_file( script_name ):
	# 		"""Given the name of a python file containing a Script class
	# 		that subclasses QATask, read that file into a working python
	# 		module that we can execute.
	# 		"""
	# 		script_name = script_name.split('.py')[0]
	# 		module_to_load = self.scripts_module + '.' + script_name + '.' + self.script_class_name
	# 		return locate( module_to_load )()

	# 	scripts = [f for f in os.listdir(self.scripts_dir) if f.endswith('.py') and '__init__' not in f]

	# 	for script_instance in map(get_running_script_for_file, scripts ):
	# 		script_details = script_instance.details()
	# 		script_name = script_details['name'] + ' v' + script_details['version'] # NOTE: if this isn't defined, problem
	# 		self.tasks[ script_name ] = script_instance

	# 	print( self.tasks )

		# return self

		# TODO: Add checks to prevent weird script names from crashing the program!
