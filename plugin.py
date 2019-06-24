#MenuTitle: Occupant QA
# -*- coding: utf-8 -*-
__doc__="""
Occupant QA Tool
"""

from GlyphsApp import *
from vanilla import *
import traceback

from tasklistview import OCC_QATaskListView

class OCC_QATool():

	def __init__(self):
		Glyphs.showMacroWindow()
		if Glyphs.font:
			print u"\n\n🙌 Welcome to the Occupant QA Tool 🙌\n\n"
			self.application = OCC_QATaskListView()
		else:
			print u"There are no fonts open 😥 Please open a file and run the tool again."

if __name__ == '__main__':
	tool = OCC_QATool()
