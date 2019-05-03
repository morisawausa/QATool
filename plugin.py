#MenuTitle: Occupant QA
# -*- coding: utf-8 -*-
__doc__="""
Occupant QA Tool
"""
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import *
import traceback

from tasklistview import OCC_QATaskListView
from scripts.compare_glyph_names import CompareGlyphNames

class OCC_QATool():

	def __init__(self):
		print "constructor called"
		self.application = OCC_QATaskListView()
		task = CompareGlyphNames()
		print(task.details())
		report = task.start(dict())

		print( report )


if __name__ == '__main__':
	tool = OCC_QATool()
