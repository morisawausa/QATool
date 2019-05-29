#MenuTitle: Occupant QA
# -*- coding: utf-8 -*-
__doc__="""
Occupant QA Tool
"""
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import *
from vanilla.test.testAll import Test
import traceback

from tasklistview import OCC_QATaskListView

class OCC_QATool():

	def __init__(self):
		print "Welcome to the Occupant QA Tool :)"

		self.application = OCC_QATaskListView()

if __name__ == '__main__':
	tool = OCC_QATool()
