# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *


class QAProfile():
	"""The QAProfile class manages which tasks are activated 
	and which are inactive, as well as defining custom 
	parameters for the typeface."""

	def __init__(self, pool):
		"""Set up our dictionary of task parameters and our 
		task ordering later use. """

		self.profile_tasks = dict()

		for task in pool.tasks:
			self.profile_tasks[task] = {
				'Script' : pool.tasks[task],
				'State' : False,
				'Parameters' : dict()
			}

		print self.profile_tasks


	def run(self, pool):
		"""Given a pool of available tasks, run the tasks 
		specified in pool and report the result. """
		# print pool

		

		# render_task_report(self):
		# return list(), list(), list()


	def save(self):
		"""Save the currently specified QATask parameters to 
		the current font's customParameters fields."""
		return self


	def load(self):
		"""Load the parameters for the specified QATasks to 
		from the current font's customParameters fields."""
		return self

	def toggle(self, task_name):
		
		self.profile_tasks[ task_name ]['State'] = not self.profile_tasks[ task_name ]['State']

		print self.profile_tasks
		return self

