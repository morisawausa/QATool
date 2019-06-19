# -*- coding: utf-8 -*-

from GlyphsApp import *
from vanilla import *
# from vanilla.test.testAll import Test

from qaprofile import QAProfile
from taskview import OCC_QATaskView



class OCC_QATaskListView():

	def __init__(self):		
		self.profile = QAProfile()
		self.task_view = OCC_QATaskView()
		self.selected_task_name = None
		self.selected_task = None
		self.master_queue = {}
		self.render()
		# Test()

	def render(self):
		"""draw entire application"""
		padding = 15
		self.w = Window((600, 700), "Occupant QA", minSize=(450, 700), maxSize=None,)

		# setup tasks to display in the list view per the task order
		self.items = list()
		
		for test in self.profile.task_order:
			self.items.append({'Test': test, 'Select': False})

		columnDescriptions = [
			{"title": "Select", "cell": CheckBoxListCell(title=None), "width": 40},
			{"title": "Test", "editable": False},
		]

		list_height = 200
		self.w.list = List((0, 0, -0, list_height), 
			items=self.items, 
			columnDescriptions=columnDescriptions, 
			selectionCallback=self.select_task, 
			editCallback=self.toggle,
			allowsMultipleSelection=False)

		detail_height = 150
		# set up detail view
		self.w.details = Box((padding, list_height+padding, -padding, detail_height), "Details")
		self.w.details.text = TextBox((5, 5, -5, -5), "Test Details Placeholder")

		box_height = 100
		# set up parameter placeholders (maximum 3)
		self.w.params = Box((padding, list_height+detail_height+padding*2, -padding, box_height), "Parameters")

		self.w.params.param0 = Group((5,10,-5,25))
		self.w.params.param0.input = EditText((0, 0, 100, -0), callback=self.create_param_callback(0))
		self.w.params.param0.label = TextBox((102, 3, -0, -0), "Parameter")

		self.w.params.param1 = Group((5,45,-5,25))
		self.w.params.param1.input = EditText((0, 0, 100, -0), callback=self.create_param_callback(1))
		self.w.params.param1.label = TextBox((102, 3, -0, -0), "Parameter")

		# self.w.params.param2 = Group((5,65,-5,25))
		# self.w.params.param2.input = EditText((0, 0, 100, -0), callback=self.create_param_callback(2))
		# self.w.params.param2.label = TextBox((102, 3, -0, -0), "Parameter")


		# set up master (maximum 9)
		self.w.masters = Box((padding, list_height+detail_height+box_height+padding*3, -padding, box_height), "Masters")
		self.w.masters.checkbox = CheckBox((5, 10, 120, 20), "All Masters", callback=self.master_all_callback, value=True)

		columns = (140, 280, 420)
		rows = (10,30,50)
		x = 0

		for i, master in enumerate(Glyphs.font.masters):
			self.master_queue[master.id] = 1;

			# assign columns
			if i<3:
				x = 0
			elif i<6:
				x = 1
			else:
				x = 2

			attrName = "checkbox%s" %i 
			checkbox = CheckBox((columns[x], rows[i%3], -10, 20), master.name, callback=self.create_master_callback(master.id), value=True)			
			setattr(self.w.masters, attrName, checkbox)


		# set up note clearing buttons
		self.w.clearNotesButton = Button((padding, -90, 140, 20), "Clear all test notes", callback=self.clear_notes)
		self.w.clearNoteButton = Button((160, -90, 275, 20), "Clear notes on current layer", callback=self.clear_note)

		# set up Run button
		self.w.runAllButton = SquareButton((padding, -55, -padding, 40), "Run Selected Tests", callback=self.run_profile)

		# select the first task
		self.select_task(self.w.list) 

		self.w.open()


	def create_param_callback(self, index):
		"""given an index into the set of parameter text inputs,
		return a callback that that text input can use to update
		its state.

		:param index: an integer that identifies the parameter input that this callback operates on.
		:return: a callback that set a parameter in the QAProfile for the selected script.
		"""
		param_index = index
		profile = self.profile

		def param_callback(sender):
			# get input value
			param_input = sender.get()

			# format parameter to appropriate type
			try:
				param_input = int(param_input)
			except ValueError:
				param_input = param_input.encode('utf-8')

			# save entered params to profile
			profile.load_params(self.selected_task_name, param_index, param_input)

		return param_callback



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

			# reset parameter view then show relevant parameters
			self.w.params.param0.show(False)
			self.w.params.param1.show(False)
			# self.w.params.param2.show(False)
			self.show_params()
			pass


	def toggle(self, sender):
		"""when clicking checkbox, toggle active state of selected task"""
		self.select_task(sender)
		self.profile.toggle(self.selected_task_name) # toggle task activation in profile


	def show_params(self):
		"""given a selected task, add each parameter to parameter view"""
		self.param_list = self.profile.tasks[self.selected_task_name]['Parameters']

		for p in self.param_list:
			group = 'param' + str(self.param_list.index(p))
			param = getattr(self.w.params, group)
			param.show(True)
			param.input.set(p[1])
			param.label.set(p[0])


	def create_master_callback(self, key):
		"""given a master id, stores whether it is active
		in self.master_queue."""
		master_id = key
		def master_callback(sender):
			self.master_queue[master_id] = sender.get()
			if sender.get()==0:
				self.w.masters.checkbox.set(False)
		return master_callback


	def master_all_callback(self, sender):
		#toggle all masters
		# print sender.get()
		if sender.get()==1:
			for i, master in enumerate(Glyphs.font.masters):
				checkbox_id = "checkbox%s" %i
				checkbox = getattr(self.w.masters, checkbox_id)
				checkbox.set(True)
				self.master_queue[master.id] = 1
		else:
			for i, master in enumerate(Glyphs.font.masters):
				checkbox_id = "checkbox%s" %i
				checkbox = getattr(self.w.masters, checkbox_id)
				checkbox.set(False)
				self.master_queue[master.id] = 0
		pass


	def clear_note(self, sender):
		"""clears notes on selected glyph"""
		layer = Glyphs.font.selectedLayers[0]
		layer.annotations = None


	def clear_notes(self, sender):
		"""clears all notes"""
		for g in Glyphs.font.glyphs:
			for layer in g.layers:
				layer.annotations = None

		

	def run_profile(self, sender):
		"""looks at current profile and runs all tasks"""
		# self.clear_notes()
		self.profile.load_masters(self.master_queue)
		self.profile.run()
		pass

