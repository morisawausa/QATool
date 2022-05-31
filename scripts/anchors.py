# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from .abstracts.task import QATask


class Script(QATask):
	"""
	Checks the consistency of top anchors for floating accents
	"""

	def details(self):
		return {
			"name": u"Top anchor alignment",
			"version": "1.4",
			"description": u"Checks the consistency of top anchors for floating accents, for Latin Uppercase, Lowercase, and Smallcaps (if they exist) based off of the [_top] anchor of ⚙️ Reference accent. Uses the [top] anchor of capital 'A / a.sc' as reference point if case accents don't exist."
			}


	def parameters(self):
		parameters = [
			("Reference", "macron"),
		]

		return parameters


	def setup_lists(self):
		"""Collect and categorize diacritic marks and base glyphs"""

		self.marks = { }

		self.sc_key = "Smallcaps"

		if ( self.glyphs["a.sc"] is not None):
			self.sc_key = self.glyphs["a.sc"].subCategory
			print('sckey', self.sc_key)

		self.mark_categories = { 
			"comb" : "Lowercase", 
			"comb.case" : "Uppercase",
			"comb.sc" : self.sc_key,
			"comb.narrow" : "Lowercase",
			"comb.narrow.case" : "Uppercase",
			"comb.sc.narrow" : self.sc_key
		}

		non_floating = ["cedilla", "commaaccent", "ogonek", "caronvert", "horn"]
		self.ignore = []

		no_accents = ["Aogonek", "B", "Eng", "Eth", "Dcroat", "F", "Germandbls", "Hbar", "Iogonek", "K", "M", "OE", "P", "Q", "Schwa", "Thorn", "Uogonek", "V", "X", "aogonek", "b",  "eng", "eth", "dcroat", "f", "f.calt_nokern", "hbar", "iogonek", "k", "germandbls", "m", "oe", "p", "q", "schwa", "i", "j", "thorn", "longs", "t", "uogonek", "v", "x"]

		self.component_glyphs = []

		self.base_glyphs = []

		
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


			# collect glyphs with components and base glyphs
			if g.category == "Letter" and g.script == "latin":
				if layer.components:
					self.component_glyphs.append(g)
				elif g.name not in no_accents and g.subCategory in ("Lowercase", "Uppercase", self.sc_key):
					self.base_glyphs.append(g)


	def get_metrics(self, master, parameters):
		"""Given reference accent, stores the '_top' anchor points of the accent and
		its case (.case, .sc) counterparts for reference. If .case accent does not exist,
		uses 'top' anchor of letter A for Uppercase reference."""
		reference = { }
		
		# get reference accent
		ref_accent_name = parameters[0][1] # i.e. macron

		if ref_accent_name in self.glyphs:

			for extension in self.mark_categories:
				mark_name = "%s%s" %(ref_accent_name, extension) #i.e. macroncomb

				if mark_name in self.glyphs:
					# get _top anchor of mark
					anchor = self.glyphs[mark_name].layers[master.id].anchors['_top']
					if anchor:
						reference[self.mark_categories[extension]] = anchor.position
					else:
						self.report.note("* %s does not have a _top anchor" % mark_name)
				
			
			# if .case accents do not exist, use top anchor position for A for Uppercase
			# if .sc accents do not exist, use top anchor position for a.sc for Smallcaps
			case_accent = ref_accent_name + "comb.case"
			sc_accent = ref_accent_name + "comb.sc"

			if case_accent not in self.glyphs:
				self.report.note("(Reference for uppercase accent y position is the top anchor on A, since .case accents don't exist)")
				anchor = self.glyphs['A'].layers[master.id].anchors['top']
				if anchor:
					reference["Uppercase"] = anchor.position
				else:
					self.report.note("*'A' does not have a top anchor and cannot be used as an Uppercase reference")

			if ( self.glyphs["a.sc"] is not None):
				if sc_accent not in self.glyphs:
					self.report.note("(Reference for smallcaps accent y position is the top anchor on a.sc, since .sc accents don't exist)")
					scanchor = self.glyphs['a.sc'].layers[master.id].anchors['top']
					if scanchor:
						reference[self.sc_key] = scanchor.position
					else:
						self.report.note("*'a.sc' does not have a top anchor and cannot be used as a Smallcaps reference")

		else:
			self.report.note("* Reference glyph does not exist in the font")

		return reference


	def check_anchors(self, master, glyph_name, ref_point, anchor_type, category, report):
		"""gets the top anchor of a given glyph and compares it against a reference point
		of the relevant category

		:glyph_name: the name of the glyph to look at
		:ref_point: the alignment point to compare to
		:anchor_point: anchor_type, i.e. top or _top
		:category: type of glyph, i.e. Uppercase, Lowercase, or Smallcaps
		"""

		layer = self.glyphs[glyph_name].layers[master.id]
		anchor = layer.anchors[anchor_type]

		if anchor:
			diffY = anchor.y - ref_point.y
			if anchor_type == "_top":
				diffX = anchor.x - ref_point.x
				if diffX != 0 or diffY != 0:
					report.add(master.name, glyph_name, "Top Anchors", "_top anchor at %s is off of the %s anchor point by (%i, %i)" % (report.node(anchor), category, diffX, diffY), passed=False )
			elif diffY != 0:
				report.add(master.name, glyph_name, "Top Anchors", "top anchor at %s is vertically off of the %s anchor point by %i" % (report.node(anchor), category, diffY), passed=False )			
		else:
			report.add(master.name, glyph_name, "Top Anchors", "%s anchor does not exist" % anchor_type, passed=False )


	def run(self, parameters, report):
		
		report.note("\n\n[ANCHOR ALIGNMENT]\n")

		self.setup_lists()
		
		report.note("* %s accent is %s" % (parameters[0][0], parameters[0][1]) )

		for master in self.masters:

			report.note("\n* MASTER %s :" % master.name)

			# get alignment points for each mark category
			alignment_points = self.get_metrics(master, parameters)

			if alignment_points is not {}:

				for a in alignment_points:
					report.note( "%s top anchors should be at %s" % (a, report.node(alignment_points[a]) ) )

				# check _top anchor consistency within each mark category
				for category in self.marks:
					marks = self.marks[category]  # list of marks

					try: 
						ref_point = alignment_points[category] # corresponding accent alignment point	
					except:
						print ('error for', category) 
					else:
						for mark in marks:
							if mark not in self.ignore: #ignore non-floating marks
								self.check_anchors(master, mark, ref_point, "_top", category, report)

				# check top anchors of base glyphs
				for glyph in self.base_glyphs:
					self.check_anchors(master, glyph.name, alignment_points[glyph.subCategory], "top", glyph.subCategory, report)


			# check automatic alignment in component glyphs
			for glyph in self.component_glyphs:

				for component in glyph.layers[master.id].components:
					if not component.automaticAlignment:
						report.add(master.name, glyph.name, "Automatic Alignment", "%s is not automatically aligned" % component.name, passed=False )


