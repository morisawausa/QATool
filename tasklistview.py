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
		self.master_ids = []
		self.master_queue = {}
		self.render()
		# Test()

	def render(self):
		"""draw entire application"""
		padding = 15
		self.w = Window((600, 800), "Occupant QA", minSize=(450, 700), maxSize=None,)

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

		detail_height = 120
		# set up detail view
		self.w.details = Box((padding, list_height+padding, -padding, detail_height), u"Details")
		self.w.details.text = TextBox((5, 5, -5, -5), "Test Details Placeholder")

		box_height = 100
		# set up parameter placeholders (maximum 3)
		self.w.params = Box((padding, list_height+detail_height+padding*2, -padding, box_height), u"Parameters")

		self.w.params.param0 = Group((5,10,-5,25))
		self.w.params.param0.input = EditText((0, 0, 100, -0), callback=self.create_param_callback(0))
		self.w.params.param0.label = TextBox((102, 3, -0, -0), "Parameter")

		self.w.params.param1 = Group((5,45,-5,25))
		self.w.params.param1.input = EditText((0, 0, 100, -0), callback=self.create_param_callback(1))
		self.w.params.param1.label = TextBox((102, 3, -0, -0), "Parameter")

		# self.w.params.param2 = Group((5,65,-5,25))
		# self.w.params.param2.input = EditText((0, 0, 100, -0), callback=self.create_param_callback(2))
		# self.w.params.param2.label = TextBox((102, 3, -0, -0), "Parameter")

		master_height = 230
		# set up masters to display in list
		self.master_rows = list()

		for i, master in enumerate(Glyphs.font.masters):
			self.master_ids.append(master.id) #append to list of master ids
			self.master_queue[master.id] = 0  #store id in master queue that feeds into profile

			self.master_rows.append({'Active': False, 'Master': master.name, 'Id': master.id})

		masterListHeader = [
			{"title": "Active", "cell": CheckBoxListCell(title=None), "width": 40},
			{"title": "Master", "editable": False, "resizable": False},
			{"title": "Id", "editable": False, "width": 0},
		] #Id is a hidden column

		self.w.masterSelection = List( (padding, list_height+detail_height+box_height+padding*3, -padding, master_height), 
			items=self.master_rows, 
			columnDescriptions=masterListHeader, 
			editCallback=self.activate_master,
			allowsMultipleSelection=True)

		# self.w.masters = Box((padding, list_height+detail_height+box_height+padding*3, -padding, box_height), "Masters")
		# self.w.masters.checkbox = CheckBox((5, 10, 120, 20), 

		# set up note clearing buttons	
		self.w.clearNotesButton = Button((padding, -90, 280, 20), u"Clear all notes", callback=self.clear_notes)
		self.w.clearNoteButton = Button((305, -90, 280, 20), u"Clear notes on current layer", callback=self.clear_note)

		# set up Run button
		self.w.runAllButton = SquareButton((padding, -55, -padding, 40), u"👉 Run Selected Tests 👈", callback=self.run_profile)

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
		

	def activate_master(self, sender):
		"""given a checkbox selection within list of masters,
		 activates master to load into QA profile queue"""
		updatedList = self.w.masterSelection.get()

		for item in updatedList:
			if item['Active'] == True:
				#checkbox selected
				self.master_queue[item['Id']] = 1 #activate master id
			else:
				#checkbox not selected
				self.master_queue[item['Id']] = 0 #activate master id


	def clear_note(self, sender):
		"""clears notes on selected glyph"""
		layer = Glyphs.font.selectedLayers[0]
		layer.annotations = None
		print u"Notes on %s[%s] removed ✨" %(layer.parent.name, layer.name)


	def clear_notes(self, sender):
		"""clears all notes"""
		for g in Glyphs.font.glyphs:
			for layer in g.layers:
				layer.annotations = None
		print u"All notes removed ✨✨✨"

		

	def run_profile(self, sender):
		"""looks at current profile and runs all tasks"""
		# self.clear_notes()
		self.profile.load_masters(self.master_queue)
		self.profile.run()
		pass

