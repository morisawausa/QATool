# -*- coding: utf-8 -*-

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
		self.task_order = list()
		self.load_scripts()

		self.task_view = OCC_QATaskView()

		self.testCount = 0


	def load_scripts(self):
		"""Load .py files in the 'scripts' directory as a series of QATasks.
		Uses the test_order.txt file to determine the task order. TODO: Records an error 
		if any of the QATasks are missing a name or does not match"""
		files = os.listdir('scripts')

		# load all .py files
		for file in files:
			if file.endswith(".py") and "__init__" not in file:
				mod = importlib.import_module( 'scripts.' + file.split('.')[0] )
				class_name = getattr(mod, 'Script')
				test = class_name()
				task_name = test.details()['name']
				self.tasks[task_name] = dict([('Script',test), ('State', False), ('Parameters', test.parameters()), ('Results', list())])
				# append script to list of tasks
		
		# read in script order file
		f = open('scripts/test_order.txt', 'r')
		order = f.read().splitlines()
		f.close()
		self.task_order = order

		return self


	def run(self):
		"""Given a pool of available tasks, runs a selection of tasks and reports the result. """
		Glyphs.clearLog()
		
		self.all_errors = {}
		self.all_notes = []

		self.testCount = 0

		for task in self.tasks:

			task_info = self.tasks[task]

			# run test if task is activated
			if task_info['State'] is True:

				self.testCount += 1

				# execute test and get return (results, notes)
				results = task_info['Script'].start(task_info['Parameters'])[0]
				
				# store test results
				task_info['Results'] = results

				# collect notes
				self.all_notes.append( task_info['Script'].start(task_info['Parameters'])[1] )

				# collect all results for output
				for m in results:
					if m in self.all_errors:
						self.all_errors[m].append(results[m])
					else:
						self.all_errors[m] = list()
						self.all_errors[m].append(results[m])

		
		if self.testCount == 0:
			print "\n\n* No tests selected"
		else:
			# output results
			self.report_all()


	def save(self):
		"""Save the currently specified QATask parameters to 
		the current font's customParameters fields."""

		return self


	def load_params(self, task_name, param_index, param_value):
		"""Load the parameters for the specified QATasks to 
		from the current font's customParameters fields."""

		# given param index, get name of parameter
		param_name = self.tasks[task_name]['Parameters'][param_index][0]

		# assign task new parameter in profile
		self.tasks[task_name]['Parameters'][param_index] = (param_name, param_value)

		return self


	def toggle(self, task_name):
		"""Toggle the active state of a given task"""
		self.tasks[ task_name ]['State'] = not self.tasks[ task_name ]['State']
		return self


	def report_all(self):
		"""generate final report"""
		
		print str(self.testCount) + " tests run\n"

		output = ""

		output += "\n\nREFERENCE\n++++++++++++++++++++++++\n\n"

		# output all notes
		for n in self.all_notes:
			for line in n:
				output += line + "\n"


		output += "\n\nTEST RESULTS\n++++++++++++++++++++++++\n\n"		

		# output all errors by master
		for master in self.all_errors:
			output += "\n\n\n\n\n------------------------------------------------------------------------------------------\n" + master + "\n------------------------------------------------------------------------------------------"
			errorGlyphs = {}

			# group all errors by glyph
			for errors in self.all_errors[master]:
				# key = e['glyph']
				for line in errors:
					key = line['glyph']
					if key in errorGlyphs:				
						errorGlyphs[key].append(line)
					else:
						errorGlyphs[key] = list()
						errorGlyphs[key].append(line)

			for e in errorGlyphs:
				output += "\n\n" + e + "\n------------\n"
				for line in errorGlyphs[e]:
					output += "[" + line['header'] + "] " 
					output += line['desc'] +'\n'

		print output



