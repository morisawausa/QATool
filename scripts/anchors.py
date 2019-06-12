# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from abstracts.task import QATask


class Script(QATask):
	"""
	Checks the consistency of top anchors for floating accents
	"""

	def details(self):
		return {
			"name": "Top anchor alignment",
			"version": "1.3.0",
			"description": "Checks the consistency of top anchors for floating accents"
			}


	def parameters(self):
		parameters = [
			("Reference", "macron"),
		]

		return parameters


	def setup_lists(self):
		"""Collect and categorize diacritic marks"""

		self.marks = { }
		self.marks["Legacy"] = []

		self.mark_categories = { 
			"comb" : "Lowercase", 
			"comb.case" : "Uppercase",
			"comb.sc" : "Smallcaps",
			"comb.narrow" : "Lowercase",
			"comb.narrow.case" : "Uppercase",
			"comb.sc.narrow" : "Smallcaps"
		}

		non_floating = ["cedilla", "commaaccent", "ogonek", "caronvert", "horn"]
		self.ignore = []
		
		for g in self.glyphs:
			layer = g.layers[self.font.selectedFontMaster.id]
			name = g.name.encode('utf-8')

			# collect all non-floating marks to ignore
			if g.name.startswith(tuple(non_floating)):
				self.ignore.append(g.name.encode('utf-8'))

			# collect all marks by category
			if "comb" in name:					
				for extension in self.mark_categories:
					if g.name.endswith(extension):
						if self.mark_categories[extension] not in self.marks:
							self.marks[self.mark_categories[extension]] = [name]
						else:
							self.marks[self.mark_categories[extension]].append(name)
			elif g.category == "Mark" and g.subCategory == "Spacing":
				self.marks["Legacy"].append(name)


	def get_metrics(self, master, parameters):
		"""Given reference accent, stores the '_top' anchor points of the accent and
		its case (.case, .sc) counterparts for reference. If .case accents do not exist,
		uses top accent position of A + reference accent"""
		reference = { }
		
		# get reference glyphs
		ref_accent_name = parameters[0][1] # i.e. macron

		if ref_accent_name in self.glyphs:
			# for mark in self.marks["Legacy"]:
			# 	if ref_glyph_name.endswith(mark):
			# 		reference_mark = mark # i.e. macron, accent name

			for extension in self.mark_categories:
				mark_name = "%s%s" %(ref_accent_name, extension) #i.e. macroncomb

				if mark_name in self.glyphs:
					# get _top anchor of mark
					anchor = self.glyphs[mark_name].layers[master.id].anchors['_top']
					if anchor:
						reference[self.mark_categories[extension]] = anchor.position
					else:
						self.report.note("* %s does not have a _top anchor" % mark_name)


		else:
			self.report.note("* Reference glyph does not exist in the font")

		return reference


	def check_anchors(self, master, all_marks, points, report):
		for category in points:
			# list of marks
			marks = all_marks[category]
			ref_point = points[category]				

			for mark in marks:

				if mark not in self.ignore: #ignore non-floating marks
					layer = self.glyphs[mark].layers[master.id]
					anchor = layer.anchors['_top']

					if anchor:
						diffX = anchor.x - ref_point.x
						diffY = anchor.y - ref_point.y

						if diffX != 0 or diffY != 0:
							report.add(master.name, mark, "Component Anchors", "_top anchor is off of the %s anchor point by (%.1f, %.1f)" % (category, diffX, diffY), passed=False )
					else:
						report.add(master.name, mark, "Component Anchors", "_top anchor does not exist", passed=False )
	


	def run(self, parameters, report):
		
		report.note("\n\n[ANCHOR ALIGNMENT]\n")

		self.setup_lists()
		
		report.note("* %s accent is %s" % (parameters[0][0], parameters[0][1]) )

		for master in self.masters:

			report.note("\n* MASTER %s :" % master.name)

			alignment_points = self.get_metrics(master, parameters)

			for a in alignment_points:
				report.note( "%s top anchors should be at %s" % (a, report.node(alignment_points[a]) ) )

			# check top anchor consistency within each mark category
			self.check_anchors(master, self.marks, alignment_points, report)

