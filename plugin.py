#MenuTitle: Test Suite
# -*- coding: utf-8 -*-
__doc__="""
Loads user-defined script files for testing purposes.
"""

from GlyphsApp import *
from vanilla import *
import traceback

from tasklistview import OCC_QATaskListView

class QAToolSuite():

	def __init__(self):
		Glyphs.showMacroWindow()
		if Glyphs.font:
			print("\n🙌 Welcome to the Test Suite 🙌\n\n")
			self.application = OCC_QATaskListView()
		else:
			print("There are no fonts open 😥 Please open a file and run the tool again.")

if __name__ == '__main__':
	tool = QAToolSuite()