# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *

from qaprofile import QAProfile
from taskview import OCC_QATaskView

class OCC_QATaskListView():

	def __init__(self):		
		self.profile = QAProfile()
		self.task_view = OCC_QATaskView()
		self.selected_task_name = None
		self.selected_task = None
		self.render()


	def render(self):
		"""draw entire application"""
		self.w = Window((500, 640), "Occupant QA")
		self.w.runAllButton = SquareButton((10, -50, -10, 40), "Run Selected Tests", callback=self.run_profile)

		# setup tasks to display in the list view per the task order
		self.items = list()
		
		for test in self.profile.task_order:
			self.items.append({'Test': test})

		columnDescriptions = [
			{"title": "Select", "cell": CheckBoxListCell(title=None), "width": 40,},
			{"title": "Test", "editable": False},
		]

		self.w.list = List((0, 0, -0, 300), 
			items=self.items, 
			columnDescriptions=columnDescriptions, 
			selectionCallback=self.select_task, 
			editCallback=self.toggle,
			allowsMultipleSelection=False)
		self.w.details = Box((10, 310, -10, 150), "Details")
		self.w.details.text = TextBox((5, 5, -5, -5), "Test Details Placeholder")


		# set up parameter placeholders (maximum 3)
		self.w.params = Box((10, 470, -10, 110), "Parameters")

		self.w.params.param0 = Group((5,5,-5,25))
		self.w.params.param0.input = EditText((0, 0, 100, -0), "pts", callback=self.param_callback)
		self.w.params.param0.label = TextBox((102, 3, -0, -0), "Parameter")

		self.w.params.param1 = Group((5,35,-5,25))
		self.w.params.param1.input = EditText((0, 0, 100, -0), "pts", callback=self.param_callback)
		self.w.params.param1.label = TextBox((102, 3, -0, -0), "Parameter")

		self.w.params.param2 = Group((5,65,-5,25))
		self.w.params.param2.input = EditText((0, 0, 100, -0), "pts", callback=self.param_callback)
		self.w.params.param2.label = TextBox((102, 3, -0, -0), "Parameter")

		self.select_task(self.w.list) # select the first task

		self.w.open()


	def select_task(self, sender):
		"""given a QATask, render that information to OCC_QATaskView"""

		selected = sender.getSelection() # gets index of line item in list.
		if not selected:
			return
		else:
			self.selected_index = selected[0] # only deal with single selection for now.

			self.selected_task_name = self.items[self.selected_index]['Test'] # get name of selected task
			self.selected_task = self.profile.tasks[self.selected_task_name]['Script'] # get selected task script

			self.task_view.set_task(self.selected_task) # sets selected task
			# add task details into detail view
			self.w.details.text.set(self.task_view.render()) 


			# reset parameter view
			self.w.params.param0.show(False)
			self.w.params.param1.show(False)
			self.w.params.param2.show(False)

			# add each parameter to parameter view
			param_list = self.task_view.render_task_parameters()
			for i, p in enumerate(param_list):
				group = 'param' + str(i)
				param = getattr(self.w.params, group)
				param.show(True)
				param.input.set(param_list[p])
				param.label.set(p)
			pass


	def toggle(self, sender):
		"""when clicking checkbox, toggle active state of selected task"""
		self.select_task(sender)
		self.profile.toggle(self.selected_task_name) # toggle task activation in profile


	def param_callback(self, sender):
		print "text entry!", sender.get()


	def run_profile(self, sender):
		"""looks at current profile and runs all tasks"""
		self.profile.run()
		pass


	def run_single_task(self, task):
		"""TODO: given a QATask, execute that task"""
		pass
