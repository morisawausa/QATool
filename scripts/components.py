# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from abstracts.task import QATask


class Script(QATask):
	"""
	Scope: All masters of selected font
	For each glyph, checks:
	- [Name]: whether the components correspond with the glyph name (Latin only)
	- [Order]: order of components
	- [Width]: whether component glyphs have the same width as its base
	- [Alignment]: vertical consistency of floating accents (Latin only)
			
	"""

	def details(self):
		return {
			"name": "Components checker",
			"version": "1.0.0",
			"description": "For all masters of selected font, checks:\n - [Name] whether the components correspond with the glyph name \n - [Order] order of components \n - [Width] whether component glyphs have the same width as its base \n - [Alignment] vertical consistency of floating accents *uses accent baseline from reference glyphs defined in parameters below"
			}


	def parameters(self):
		return {
			"Uppercase": 'Agrave',
			"Lowercase": 'agrave',
			"Smallcaps": 'Agrave.sc'
		}

	def setup_lists(self):
		"""Sets up list of a)diacritic marks and b)glyphs with components"""

		self.diacritics = []
		self.componentGlyphs = []
		
		for g in self.glyphs:
			layer = g.layers[self.thisMaster]		
			
			# collect diacritic marks
			if g.category == "Mark":
				self.diacritics.append(g.name.encode('utf-8'))
			
			# collect glyphs with components
			if layer.components and g.category == "Letter":
				self.componentGlyphs.append(g)


	def check_names(self, glyph, master):
		"""Given a glyph with components, tracks the component order by concatenating the detected components together"""

		# placeholder for detected components
		composedName = ""

		# process suffixed glyphs such as .sc and .salt_tail
		name = ""
		suffix = ""
		if "." in glyph.name:
			name = glyph.name.split(".", 1)[0]
			suffix = "." + glyph.name.split(".", 1)[1]

		# string together component names for comparison
		for component in glyph.layers[master].components:
			
			# compose component names
			if component.name == "idotless":
				composedName += "i"
			elif "comb.case" in component.name:
				composedName += component.name.replace("comb.case","")
			elif "comb" in component.name:
				composedName += component.name.replace("comb","")
			elif suffix in component.name:
				composedName += component.name.replace(suffix,"")
			else:
				composedName += component.name

		# add suffix back onto the name	
		composedName += suffix

		# check if it has the right components according to its name
		if glyph.script == "latin": # only check Latin glyphs
			if glyph.name != composedName:
				return "[Order] check component order"
		

	def get_components(self, glyph, master):
		"""Given a glyph with components, returns the base glyph and accent components as a dictionary."""

		# placeholder for base / accent dict
		components = {}

		for component in glyph.layers[master].components:

			# build dictionary of component and base glyphs
			if component.name in self.diacritics:
				# define accent glyph
				components['accent'] = component
			else:
				# define base glyph from non-diacritic component
				components['baseComp'] = component

				# define base glyph from glyph name (in the case that base glyphs are decomposed)
				components['base'] = component.name.encode('utf-8')

		return components

	
	def check_widths(self, glyph, comps, master):
		"""Given a component glyph (i.e. ã), compares its width to the width of its base glyph (i.e. a) """

		# get width of glyph
		width = glyph.layers[master].width
		
		if 'baseComp' in comps:
			baseGlyph = comps['baseComp'].componentName
		elif 'base' in comps:
			baseGlyph = comps['base']
			return "[Name] base glyph is decomposed"
		else:
			return "[Name] unknown base glyph"
		
		if baseGlyph:
			# get width of base glyph
			baseWidth = self.glyphs[baseGlyph].layers[master].width
						
			# check if the composed glyph width matches the width of its base glyph
			diff = baseWidth - width
			if diff != 0:
				return '[Width] Width of ' + glyph.name + ' is off from ' + baseGlyph + " by " + str(diff)


	def get_metrics(self, master):
		"""Given reference glyphs, stores the bottom-most point of the accent component in reference_metrics.TODO: read in params for ref glyphs"""
		reference = dict()
		
		smallCaps = True

		def get_accent_bounds(glyphName):
			glyph = self.glyphs[ glyphName ]
			reference[ glyph.subCategory ] = self.get_components(glyph, master)['accent'].bounds.origin.y
		# reference['Uppercase'] = self.get_components('Agrave', master)['accent'].bounds.origin.y
		# reference['Lowercase'] = self.get_components('agrave', master)['accent'].bounds.origin.y

		get_accent_bounds('Agrave')
		get_accent_bounds('agrave')
		
		if smallCaps:
			get_accent_bounds('Agrave.sc')

		return reference


	def check_alignment(self, g, comps, metrics):
		"""Given a component glyph, checks the bottom alignment of its accent to a given reference glyph"""

		# check only latin accents
		if g.script == "latin":
			if 'accent' in comps:
				diff = comps['accent'].bounds.origin.y - metrics[ g.subCategory ]
				if diff != 0:
					return "[Alignment] " + comps['accent'].name + " is off of the accent baseline by " + str(diff)
			else:
				return "Note: accent component is missing or decomposed"



	def run(self, parameters, report):
		self.thisMaster = self.font.selectedFontMaster.id
		self.setup_lists()
		
		alignment_points = self.get_metrics(self.thisMaster)

		for a in alignment_points:
			self.report.add( "* " + a.encode('utf-8') + " accents should be aligned at " + str(alignment_points[a]), passed=None )


		for g in self.componentGlyphs:

			# check glyph name consistency and component order
			n = self.check_names(g, self.thisMaster)

			# get components
			comps = self.get_components(g, self.thisMaster)

			# check width consistency
			w = self.check_widths(g, comps, self.thisMaster)

			# check accent alignment consistency
			a = self.check_alignment(g, comps, alignment_points)

			if n or w or a:
				report.add( report.glyph(g), passed=None )
				if n:
					report.add(str(n), passed=False)
				if w:
					report.add(str(w), passed=False)
				if a: 
					report.add(str(a), passed=False)


		# 		
		# 

		# for g in componentGlyphs:
		# 	print "\n\n", g.name
		# 	components = getComponents(g.name)
		# 	print components
		# 	compare_widths(g, components)
		# 	check_alignment(g, components)
