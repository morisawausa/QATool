# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from .abstracts.task import QATask


class Script(QATask):
	"""Checks for paths or handles that are supposed to be straight."""

	def details(self):
		return {
			"name": u"Global metrics",
			"version": "1.0.0",
			"description": u"Checks consistency of font dimensions metrics values, using the first master as a reference."
			}


	def parameters(self):
		return []


	def run(self, parameters, report):
		metrics = {
			"ascender": [],
			"cap_height": [],
			"x_height": [],
			"descender": [],
			"italic_angle": []
		}
		report.note("\n\n[GLOBAL METRICS]\n")

		# collect metrics info for each master
		for m in self.masters:
			metrics["ascender"].append(m.ascender)
			metrics["cap_height"].append(m.capHeight)
			metrics["x_height"].append(m.xHeight)
			metrics["descender"].append(m.descender)
			metrics["italic_angle"].append(m.italicAngle)

		# compare metrics for each category
		reference = "* Reference Master: %s\n" %self.masters[0].name
		reference += "* Masters Checked: %s\n\n" %', '.join(m.name for m in self.masters)
		errors = ""
		for category in metrics:
			reference += "%s = %s\n\n" %(category, ', '.join(map(str, metrics[category])) )
			if category != "x_height":
				for i, metric in enumerate(metrics[category]):
					if metric != metrics[category][0]:
						master = self.masters[i]
						report.add(master.name, "", "Global Metrics", u"⚠️ %s = %i" %(category, metric), passed=False)
		
		# check absolute sum of ascender and descender
		sum_check = abs(metrics["ascender"][0])+abs(metrics["descender"][0])
		if sum_check == 1000:
			reference += u"|ascender| + |descender| = 1000 👍\n"
		else:
			reference += u"⚠️ |ascender| and |descender| does not add up to 1000\n"

		# output
		report.note(reference)
		

			