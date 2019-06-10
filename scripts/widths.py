# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from abstracts.task import QATask


class Script(QATask):
	"""
	Scope: All masters of selected font
	Checks the widths of
	- Combining accents
	- Non-Combining legacy accents
	- Spacing glyphs 
	- Tabular glyphs
	"""

	def details(self):
		return {
			"name": "Fixed width checker",
			"version": "1.0.0",
			"description": "Checks glyphs that have fixed widths: combining accents, legacy accents, tabular glyphs, and spacing glyphs."
			}


	def parameters(self):
		return []


	def run(self, parameters, report):

		report.note("\n\n[TABULAR WIDTH]\n")

		# get units per em
		upm = self.font.upm

		spaces = {
			"enquad" : .5,
			"emquad" : 1,
			"enspace" : .5,
			"emspace" : 1,
			"threeperemspace" : .333,
			"fourperemspace" : .25,
			"sixperemspace" : .166,
			"thinspace" : .166,
			"hairspace" : .1,
			"zerowidthspace" : 0,
			"zerowidthnobreakspace" : 0,
		}


		for m in self.masters:

			if "zero.tf" in self.glyphs:
				tab_width = self.glyphs["zero.tf"].layers[m.id].width
				report.note("* MASTER %s tabular width = %i\n" %(m.name, tab_width) )
			else:
				tab_width = False
				report.note("Tabular glyphs or zero.tf does not exist")

			for g in self.glyphs:

				width = g.layers[m.id].width

				if g.subCategory=="Nonspacing":
					if width != 0:
						report.add(m.name, g.name, "Zero width", g.name + " has a non-zero width", passed=False)
				if g.name.endswith(".tf") or g.subCategory=="Spacing" or g.name == "figurespace":
					if tab_width:
						if width != tab_width:
							report.add(m.name, g.name, "Tabular width", g.name + " is off of the tab width by " + str(tab_width-width), passed=False)
				if g.name in spaces:
					space_width = upm * spaces[g.name]
					if width != space_width:
						report.add(m.name, g.name, "Space width", g.name + " is off of the space width by " + str(tab_width-width), passed=False)


