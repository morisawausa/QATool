#MenuTitle: Occupant QA
# -*- coding: utf-8 -*-
__doc__="""
Occupant QA Tool
"""
# import sys
# print(sys.version_info[0])
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import *
import traceback

from tasklistview import OCC_QATaskListView

class OCC_QATool():
	def __init__(self):
		print "constructor called"
		self.application = OCC_QATaskListView()

if __name__ == '__main__':
	tool = OCC_QATool()
