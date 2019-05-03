# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *

class QATask():
	
	def __init__(self):
		print "QATask constructor called"
		self.report = QAReport(self)


	def details(self):
		"""Returns default task details. Implementers should override
		this with specifics of the test"""
		return {
			"name": "Default Task Name",
			"version": "1.0.0",
			"description": "This is the default description"
		}


	def parameters(self):
		"""Returns default task parameters."""
		return dict()


	def start(self, parameters):
		"""Calls run method and stores results in QAReport. 
		Returns QAReport for rendering."""
		self.report = QAReport(self)
		self.run(parameters, self.report)
		self.report.finalize()
		return self.report


	def run(self, parameters, report):
		"""Implementers should override this method to run test"""
		pass

