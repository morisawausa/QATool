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
			"name": "QA QA",
			"version": "1.0.0",
			"description": "QA description goes here"
		}

	def run( self, parameters, report ):
		report.add( "Blah", "Passed the Sample Test (desc)", passed=True )
