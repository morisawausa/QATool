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
		Glyphs.showMacroWindow()
		# Test()
		if Glyphs.font:
			print "\n\nWelcome to the Occupant QA Tool :)\n\n"
			self.application = OCC_QATaskListView()
		else:
			print "There are no fonts open :/."

if __name__ == '__main__':
	tool = OCC_QATool()
