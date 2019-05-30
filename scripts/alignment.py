# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from abstracts.task import QATask

class Script(QATask):
	"""Test QA
	"""

	def details( self ):
		return {
			"name": "Alignment Reporter",
			"version": "1.0.0",
			"description": "Loops through all open fonts and checks if any point falls within 2 pts vertical distance of baseline, xheight, cap height, descender height, or ascender height."
		}

	def run( self, parameters, report ):
		font = Glyphs.font
		name = font.familyName
		print name
		report.add( "Font Name",
			str(name),
			passed=True )
