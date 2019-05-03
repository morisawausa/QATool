# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *

class QAPool():
	def __init__(self):
		print "QAPool constructor called"
		self.tasks = dict()

	def update_tasks(self):
		"""reads filelist of QATasks and loades the contents of the scripts directory as a series of QATasks. Records an error if any of the QATasks are missing a name"""
		return self