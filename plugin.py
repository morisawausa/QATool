#MenuTitle: Occupant QA
# -*- coding: utf-8 -*-
__doc__="""
Occupant QA Tool
"""

from views.tasklistview import OCC_QATaskListView

class OCC_QATool():
	def __init__(self):
		print "constructor called"
		self.application = OCC_QATaskListView()

if __name__ == '__main__':
	tool = OCC_QATool()
