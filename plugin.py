#MenuTitle: Occupant QA
# -*- coding: utf-8 -*-
__doc__="""
Occupant QA Tool
"""

from GlyphsApp import *
from vanilla import *
from vanilla.test.testAll import Test
import traceback

from tasklistview import OCC_QATaskListView

class OCC_QATool():

	def __init__(self):
		print "\n\nWelcome to the Occupant QA Tool :)\n\n"
		# Test()
		self.application = OCC_QATaskListView()

if __name__ == '__main__':
	tool = OCC_QATool()
