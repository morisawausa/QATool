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
			"description": "For all masters of selected font, checks:\n - [Component] whether the components correspond with the glyph name \n - [Component Order] order of components \n - [Component Width] whether component glyphs have the same width as its base \n - [Component Alignment] vertical consistency of floating accents measured against {reference glyphs}"
			}


	def parameters(self):
		parameters = [
			("Uppercase", 'Agrave'),
			("Lowercase", 'agrave')
		]

		# check for small caps
		if self.glyphs["a.sc"] in self.glyphs:
			parameters.append("Smallcaps", 'agrave.sc')
		
		return parameters

	def setup_lists(self):
		"""Sets up list of a)diacritic marks and b)glyphs with components"""

		self.diacritics = []
		self.component_glyphs = []
		
		for g in self.glyphs:
			layer = g.layers[self.font.selectedFontMaster.id]
			
			# collect diacritic marks
			if g.category == "Mark":
				self.diacritics.append(g.name.encode('utf-8'))
			
			# collect glyphs with components
			if layer.components and g.category == "Letter":
				self.component_glyphs.append(g)


	def check_names(self, glyph, master):
		"""Given a glyph with components, tracks the component order by concatenating the detected components together"""

		# placeholder for detected components
		composed_name = ""

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
				composed_name += "i"
			elif "comb.case" in component.name:
				composed_name += component.name.replace("comb.case","")
			elif "comb.sc" in component.name:
				composed_name += component.name.replace("comb.sc","")
			elif "comb" in component.name:
				composed_name += component.name.replace("comb","")
			elif suffix in component.name:
				composed_name += component.name.replace(suffix,"")
			else:
				composed_name += component.name

		# add suffix back onto the name	
		composed_name += suffix

		# check if it has the right components according to its name
		if glyph.script == "latin": # only check Latin glyphs
			if glyph.name != composed_name:
				self.report.add(master.name, glyph.name, 'Component order', "base glyph is not first", passed=False)
		

	def get_components(self, glyph, master):
		"""Given a glyph with components, returns the base glyph and accent components as a dictionary."""

		component_types = {}

		for component in glyph.layers[master.id].components:

			# build dictionary of component and base glyphs
			if component.name in self.diacritics:
				# define accent glyph
				component_types['accent'] = component
			else:
				# define base glyph from non-diacritic component
				component_types['baseComp'] = component

				# define base glyph from glyph name (in the case that base glyphs are decomposed)
				component_types['base'] = component.name.encode('utf-8')

		return component_types

	
	def check_widths(self, glyph, master, comps):
		"""Given a component glyph (i.e. ã), compares its width to the width of its base glyph (i.e. a) """

		# get width of glyph
		width = glyph.layers[master.id].width
		base_glyph = ""
		
		if 'baseComp' in comps:
			base_glyph = comps['baseComp'].componentName
		elif 'base' in comps:
			base_glyph = comps['base']
			self.report.add(master.name, glyph.name, "Component", "base glyph is decomposed", passed=False)
		else:
			self.report.add(master.name, glyph.name, "Component", "unknown base glyph", passed=False)
		
		if base_glyph != "":
			# get width of base glyph
			base_width = self.glyphs[base_glyph].layers[master.id].width
						
			# check if the composed glyph width matches the width of its base glyph
			diff = base_width - width
			if diff != 0:
				self.report.add(master.name, glyph.name, "Component width", 'Width of ' + glyph.name + ' is off from ' + base_glyph + " by " + str(diff), passed=False)


	def get_metrics(self, master, parameters):
		"""Given reference glyphs, stores the bottom-most point of the accent component in reference_metrics.TODO: read in params for ref glyphs"""
		reference = { }
		
		for p in parameters:
			ref_glyph = p[1]
			ref_category = p[0]

			if ref_glyph in self.glyphs:
				glyph = self.glyphs[ ref_glyph ]
				ref_components = self.get_components(glyph, master)

				if 'accent' in ref_components:
					reference[ ref_category ] = ref_components['accent'].bounds.origin.y
				else:
					self.report.note("Reference glyph does not contain a diacritic component")

		return reference


	def check_alignment(self, glyph, master, comps, metrics, report):
		"""Given a component glyph, checks the bottom alignment of its accent to a given reference glyph"""

		# check only latin accents
		if glyph.script == "latin":

			# if component is an accent
			if 'accent' in comps:

				# if there is a reference metric for the glyph category
				if glyph.subCategory in metrics:

					diff = comps['accent'].bounds.origin.y - metrics[ glyph.subCategory ]
					if diff != 0:
						report.add(master.name, glyph.name, "Component alignment", comps['accent'].name + " is off of the accent line by " + str(diff), passed=False)
				else:
					report.note("Reference point for " + glyph.name + " in category [" + glyph.subCategory + "] is missing")
			else:
				report.add(master.name, glyph.name, "Component", "Note: accent component is missing or decomposed", passed=False)



	def run(self, parameters, report):
		
		self.setup_lists()
		
		for p in parameters:
			report.note("*[COMPONENT ALIGNMENT] %s to %s" % (p[0], p[1]) )

		for m in self.masters:
			alignment_points = self.get_metrics(m, parameters)
			report.note("\n[COMPONENT ALIGNMENT] * MASTER %s :" % m.name)

			for a in alignment_points:
				report.note( "%s accent line = %i" % (a, alignment_points[a]) )

			for g in self.component_glyphs:

				# check glyph name consistency and component order
				self.check_names(g, m)

				# get components
				comps = self.get_components(g, m)

				# check width consistency
				self.check_widths(g, m, comps)

				# check accent alignment consistency
				self.check_alignment(g, m, comps, alignment_points, report)
