# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *

from qaprofile import QAProfile
from taskview import OCC_QATaskView

class OCC_QATaskListView():

	def __init__(self):
		print "QA Task List View constructor called"
		
		self.profile = QAProfile()
		self.task_view = OCC_QATaskView()
		self.selected_task_name = None
		self.selected_task = None
		self.render()


	def render(self):
		"""draw entire application"""
		self.w = Window((500, 500), "Occupant QA")
		self.w.runAllButton = Button((0, -20, -0, 20), "Run All Tests", callback=self.run_profile)

		self.items = list() # setup task list for display
		for key in self.profile.tasks.keys():
			self.items.append({'Test': key})

		columnDescriptions = [
			{"title": "Select", "cell": CheckBoxListCell(title=None), "width": 40},
			{"title": "Test"},
			# {"title": "Run", "width": 40}, #TODO: set up individual runs per line
		]

		self.w.list = List((0, 0, -0, 300), 
			items=self.items, 
			columnDescriptions=columnDescriptions, 
			selectionCallback=self.select_task, 
			editCallback=self.toggle)
		self.w.details = TextBox((10, 300, -10, 100), "Test Details") #TODO: first line selected by default
		self.w.open()


	def select_task(self, sender):
		"""given a QATask, render that information to OCC_QATaskView"""
		self.selection(sender) # get task info of selected line item
		self.task_view.set_task(self.selected_task) # sets selected task
		self.w.details.set(self.task_view.render()) # add task details into textbox
		pass


	def toggle(self, sender):
		"""when clicking checkbox, toggle active state of selected task"""
		self.selection(sender)
		self.profile.toggle(self.selected_task_name)


	def selection(self, sender):
		"""gives corresponding task from a list selection on the window"""
		selected = sender.getSelection()[0] # gets index of line item in list. only deal with single selection for now.
		self.selected_task_name = self.items[selected]['Test'] # gets name of task
		self.selected_task = self.profile.tasks[self.selected_task_name]['Script'] # gets task script


	def run_profile(self, sender):
		"""looks at current profile and runs all tasks"""
		print "run all tests"
		for task in self.profile.tasks:
			task_obj = self.profile.tasks[task]
			if task_obj['State'] is True:
				self.task_view.render_task_report(self.profile.tasks[task]['Script'])
		pass


	def run_single_task(self, task):
		"""given a QATask, execute that task"""
		pass
