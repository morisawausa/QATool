# -*- coding: utf-8 -*-

from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import *

from abstracts.task import QATask

class Script(QATask):
	"""Test QA
	"""

	def details( self ):
		return {
			"name": "Test Test",
			"version": "1.0.0",
			"description": "Example Test Description"
		}

	def run( self, parameters, report ):
		report.add( "Line Title (header)", "Passed the Test Test (desc)", passed=True )
