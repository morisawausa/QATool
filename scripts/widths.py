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
			"description": "Checks glyphs that have fixed widths: combining accents, legacy accents, spacing glyphs, and tabular glyphs"
			}


	def parameters(self):
		return []


	def run(self, parameters, report):

		unicode_space = {  '2000': (.5, "enquad"),
		               '2001': (1, "emquad"),
		               '2002': (.5,  "enspace"),
		               '2003': (1,  "emspace"),
		               '2004': (.333, "threeperemspace"),
		               '2005': (.25,  "fourperemspace"),
		               '2006': (.166, "sixperemspace"),
		               '2009': (.166,  "thinspace"),
		               '200A': (.1,  "hairspace"),
		               '200B': (0, "zerowidthspace"),
		               'FEFF': (0, "nonbreakingzerowidthspace"),
		               }


		for m in self.masters:

			if "zero.tf" in self.glyphs:
				tab_width = self.glyphs["zero.tf"].layers[m.id].width
				report.note("\n* MASTER " + m.name + " tab_width = " + str(tab_width))
			else:
				report.note("zero.tf does not exist")

			for g in self.glyphs:
				width = g.layers[m.id].width

				if g.subCategory=="Nonspacing":
					if width != 0:
						report.add(m.name, g.name, "Zero width", g.name + " has a non-zero width", passed=False)
				if g.name.endswith(".tf") or g.subCategory=="Spacing":
					if width != tab_width:
						report.add(m.name, g.name, "Tabular width", g.name + " is off of the tab width by " + str(tab_width-width), passed=False)

