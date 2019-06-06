# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from abstracts.task import QATask


class Script(QATask):
	"""
	Scope: All masters of selected font
	For each glyph, checks:
	- [Name] whether the components correspond with the glyph name (Latin only)
	- [Order] order of components
	- [Width] whether component glyphs have the same width as its base
	- [Alignment] vertical consistency of floating accents (Latin only)	
	"""

	def details(self):
		return {
			"name": "Components checker",
			"version": "1.0.0",
			"description": "For all masters of selected font, checks:\n - [Component] whether the components correspond with the glyph name \n - [Component Order] order of components \n - [Component Width] whether component glyphs have the same width as its base \n - [Component Alignment] vertical consistency of floating accents (uses accent baseline from reference glyphs defined in parameters below)"
			}


	def parameters(self):
		parameters = [
			{"Uppercase": 'Agrave'},
			{"Lowercase": 'agrave'}
		]

		if self.glyphs["A.sc"] in self.glyphs:
			parameters.append({"Smallcaps": 'Agrave.sc'})
		
		return parameters

	def setup_lists(self):
		"""Sets up list of a)diacritic marks and b)glyphs with components"""

		self.diacritics = []
		self.componentGlyphs = []
		
		for g in self.glyphs:
			layer = g.layers[self.font.selectedFontMaster.id]
			
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
		for component in glyph.layers[master.id].components:
			
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
				self.report.add(master.name, glyph.name, 'Component order', "base glyph is not first", passed=False)
		

	def get_components(self, glyph, master):
		"""Given a glyph with components, returns the base glyph and accent components as a dictionary."""

		componentDict = {}

		for component in glyph.layers[master.id].components:

			# build dictionary of component and base glyphs
			if component.name in self.diacritics:
				# define accent glyph
				componentDict['accent'] = component
			else:
				# define base glyph from non-diacritic component
				componentDict['baseComp'] = component

				# define base glyph from glyph name (in the case that base glyphs are decomposed)
				componentDict['base'] = component.name.encode('utf-8')

		return componentDict

	
	def check_widths(self, glyph, master, comps):
		"""Given a component glyph (i.e. ã), compares its width to the width of its base glyph (i.e. a) """

		# get width of glyph
		width = glyph.layers[master.id].width
		baseGlyph = ""
		
		if 'baseComp' in comps:
			baseGlyph = comps['baseComp'].componentName
		elif 'base' in comps:
			baseGlyph = comps['base']
			self.report.add(master.name, glyph.name, "Component", "base glyph is decomposed", passed=False)
		else:
			self.report.add(master.name, glyph.name, "Component", "unknown base glyph", passed=False)
		
		if baseGlyph != "":
			# get width of base glyph
			baseWidth = self.glyphs[baseGlyph].layers[master.id].width
						
			# check if the composed glyph width matches the width of its base glyph
			diff = baseWidth - width
			if diff != 0:
				self.report.add(master.name, glyph.name, "Component width", 'Width of ' + glyph.name + ' is off from ' + baseGlyph + " by " + str(diff), passed=False)


	def get_metrics(self, master, parameters):
		"""Given reference glyphs, stores the bottom-most point of the accent component in reference_metrics.TODO: read in params for ref glyphs"""
		reference = { }
		
		for p in parameters:
			ref_glyph = p.values()[0]
			ref_category = p.keys()[0]

			if ref_glyph in self.glyphs:
				glyph = self.glyphs[ ref_glyph ]
				ref_components = self.get_components(glyph, master)

				if 'accent' in ref_components:
					reference[ ref_category ] = ref_components['accent'].bounds.origin.y
				else:
					self.report.note("Reference glyph does not contain a diacritic component")

		return reference


	def check_alignment(self, glyph, master, comps, metrics):
		"""Given a component glyph, checks the bottom alignment of its accent to a given reference glyph"""

		# check only latin accents
		if glyph.script == "latin":

			# if component is an accent
			if 'accent' in comps:

				# if there is a reference metric for the glyph category
				if glyph.subCategory in metrics:

					diff = comps['accent'].bounds.origin.y - metrics[ glyph.subCategory ]
					if diff != 0:
						self.report.add(master.name, glyph.name, "Component alignment", comps['accent'].name + " is off of the accent line by " + str(diff), passed=False)
				else:
					self.report.note("Reference point for " + glyph.name + " in category [" + glyph.subCategory + "] is missing")
			else:
				self.report.add(master.name, glyph.name, "Component", "Note: accent component is missing or decomposed", passed=False)



	def run(self, parameters, report):
		
		self.setup_lists()
		
		for p in parameters:
			self.report.note("* ALIGN ACCENTS for " + p.keys()[0] + " to " + p.values()[0])

		for m in self.font.masters:
			alignment_points = self.get_metrics(m, parameters)
			self.report.note("\n* MASTER " + m.name + ":")

			for a in alignment_points:
				self.report.note( a.encode('utf-8') + " accent line = " + str(alignment_points[a]))

			for g in self.componentGlyphs:

				# check glyph name consistency and component order
				self.check_names(g, m)

				# get components
				comps = self.get_components(g, m)

				# check width consistency
				self.check_widths(g, m, comps)

				# check accent alignment consistency
				self.check_alignment(g, m, comps, alignment_points)
