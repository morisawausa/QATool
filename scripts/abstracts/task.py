# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *

from .report import QAReport

class QATask():

	def __init__(self):
		self.report = QAReport(self)
		self.font = Glyphs.font
		self.glyphs = self.font.glyphs


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
		return list()


	def start(self, parameters, master_list):
		"""Calls run method and stores results in QAReport.
		Returns QAReport for rendering."""
		self.masters = master_list
		self.report = QAReport(self)
		self.run(parameters, self.report)
		return self.report.finalize()


	def run(self, parameters, report):
		"""Implementers should override this method to run test"""
		pass

