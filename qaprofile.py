# -*- coding: utf-8 -*-

from GlyphsApp import *
from vanilla import *
import os
import importlib
import re
from Foundation import NSPoint

from taskview import OCC_QATaskView

class QAProfile():
	"""The QAProfile class manages
	- which tasks are activated
	- parameter values for each task
	- which masters to run QA."""

	def __init__(self):
		"""Set up our dictionary of tasks that stores the tasks, its states, and parameters"""
		self.tasks = dict()
		self.task_order = list()
		self.load_scripts()
		self.task_view = OCC_QATaskView()

		self.testCount = 0
		self.font = Glyphs.font
		self.glyphs = self.font.glyphs


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


	def load_params(self, task_name, param_index, param_value):
		"""Load the parameters for the specified QATasks to 
		from the current font's customParameters fields."""

		# given param index, get name of parameter
		param_name = self.tasks[task_name]['Parameters'][param_index][0]

		# assign task new parameter in profile
		self.tasks[task_name]['Parameters'][param_index] = (param_name, param_value)

		return self


	def load_masters(self, masters):
		"""Load activated masters to run QA"""
		self.master_list = list(Glyphs.font.masters)

		for master_id in masters:
			if masters[master_id] == 0: #if marked inactive, remove from self.master_list
				self.master_list.remove(Glyphs.font.masters[master_id])

		return self


	def toggle(self, task_name):
		"""Toggle the active state of a given task"""
		self.tasks[ task_name ]['State'] = not self.tasks[ task_name ]['State']
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

				# execute test and get return, list of results and notes
				run = task_info['Script'].start(task_info['Parameters'], self.master_list)
				
				# store test results on task profile
				results = run[0]
				task_info['Results'] = results

				# collect notes
				self.all_notes.append( run[1] )

				# collect all results by master for output
				for master in results:
					if master in self.all_errors:
						self.all_errors[master].append(results[master])
					else:
						self.all_errors[master] = list()
						self.all_errors[master].append(results[master])

		
		if self.testCount == 0:
			print "\n\n⚠️ No tests selected"
		if len(self.master_list) == 0:
			print "\n\n⚠️ No masters selected"
		else:
			# output results
			self.report_all()


	def report_all(self):
		"""generate final report"""
		master_list =[]
		for GS_master in self.font.masters:
			master_list.append(GS_master.name)

		print "%s tests run\n" %self.testCount

		output = u""

		if self.all_notes or self.all_errors:

			output += u"\n\n⚙️ REFERENCE ⚙️\n++++++++++++++++++++++++\n\n"

			# output all notes
			for n in self.all_notes:
				for line in n:
					output += line + "\n"

			if self.all_errors:
				output += u"\n\n👉 TEST RESULTS 👈\n++++++++++++++++++++++++\n\n"	

				# output all errors by master
				for master in self.all_errors:
					#get index of master
					master_index = master_list.index(master)

					output += u"\n\n\n\n\n------------------------------------------------------------------------------------------\n📌 %s 📌\n------------------------------------------------------------------------------------------" %master
					errorGlyphs = {}

					# group all errors by glyph
					for errors in self.all_errors[master]:
			
						for line in errors:
							key = line['glyph']
							if key in errorGlyphs:				
								errorGlyphs[key].append(line)
							else:
								errorGlyphs[key] = list()
								errorGlyphs[key].append(line)

					for e in errorGlyphs:
						output += '\n\n%s\n------------\n' %e
						x = 0
						for line in errorGlyphs[e]:
							error = "[%s] %s\n" %(line['header'], line['desc'])
							output += error

							layer = self.glyphs[e].layers[self.font.masters[master_index].id]

							#add notes to glyphs if they have relevant points
							node = re.search('\((-?\d*), (-?\d*)\)', line['desc'])
							if node:
								x = int(node.group(1))
								y = int(node.group(2))

								circle = GSAnnotation()
								circle.position = NSPoint(x,y)
								circle.type = CIRCLE
								circle.width = 30

								layer.annotations.append(circle)
							else:
								y = 1200

							note = GSAnnotation()
							note.position = NSPoint(x,y)
							note.type = TEXT
							note.text = error
							layer.annotations.append(note)
							x += 600
							
					
					# output error glyphs in new tab
					tab_text = "/" + "/".join(errorGlyphs.keys()).decode('utf-8')
					
					# open new tab with master selected
					if tab_text != "/":
						self.font.newTab( tab_text ).masterIndex = master_index
			elif not self.all_notes:
				output += u"👏 ALL GOOD 👏"
		
		print output
		



