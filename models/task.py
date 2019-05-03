# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *

class QATask():
	
	def __init__(self):
		print "QATask constructor called"
		self.report = None


	def details(self):
		"""returns default task details. Implementers should override
		this with specifics of the test"""
		return {
			"name": "Default Taks Name",
			"version": "1.0.0",
			"description": "This is the default description"
		}


	def parameters(self):
		"""returns default task parameters."""
		return dict()


	def start(self):
		"""calls run method and stores results in QAReport. 
		Returns QAReport for rendering."""
		pass


	def run(self, parameters, report):
		"""Implementers should override this method to run test"""
		pass


	def finalize(self):
		"""Update QAReport after running test and return QAReport"""
		pass

