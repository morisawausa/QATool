# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from abstracts.task import QATask

import numpy as np

class Script(QATask):
	"""Checks vertical alignment of key points across masters.
	Scans for points within the zone threshold around each vertical metric.
	"""

	def details(self):
		return {
			"name": "Vertical metrics",
			"version": "1.2.0",
			"description": "For all masters of selected font, checks if any point falls within the {Zone threshold} (3pts by default.) Uses the following glyphs as reference points for alignment: baseline (H), baseline overshoot (O), ascender (h), descender (p), capheight (H), capheight overshoot (O), xheight (u), xheight overshoot (o). If small caps exists, also checks small cap capheight (H.sc)"
			}


	def parameters(self):
		return [
			("Zone threshold", 3)
		]

	def find_nearest(self, array, value):
		array = np.asarray(array)
		idx = (np.abs(array - value)).argmin()
		return array[idx]
	
	def set_metrics(self):

		def ref_bounds(ref):
			glyph = self.glyphs[ref].layers[self.font.selectedFontMaster.id]
			bounds = []

			bounds.append(glyph.bounds.origin.y) #minimum point
			bounds.append(glyph.bounds.origin.y + glyph.bounds.size.height) #max point

			return bounds

		metrics_dict = {
		 "baseline" : min(ref_bounds('H')), 
		 "baseline undershoot" : min(ref_bounds('O')),
		 "ascender" : max(ref_bounds('h')),
		 "descender" : min(ref_bounds('p')), 
		 "capheight" : max(ref_bounds('H')),
		 "capheight overshoot" : max(ref_bounds('O')),
		 "xheight" : max(ref_bounds('u')),
		 "xheight overshoot" : max(ref_bounds('o')),
		}

		if self.glyphs["h.sc"] in self.glyphs:
			metrics_dict["smallcapheight"] =  max(ref_bounds('h.sc'))
			metrics_dict["smallcapheight overshoot"] = max(ref_bounds('o.sc'))
		
		return metrics_dict

	def run(self, parameters, report):

		report.note("\n\n[VERTICAL METRICS]\n")

		metrics = self.set_metrics()

		metrics_output = "\n".join(["%s = %s" % (key, value) for (key, value) in metrics.items()])
		report.note("\n* Alignments:\n%s" % metrics_output )

		padding = parameters[0][1]
		report.note("\n* Buffer: %i\n" % padding)

		for m in self.masters:
			for g in self.glyphs:
				layer =  g.layers[m.id]
				for path in layer.paths:
					for node in path.nodes:
						if node.type == 'line' or node.type == 'curve':
							if node.y in metrics.values(): # matches metrics line
								break
							else:
								nearest = self.find_nearest(metrics.values(), node.y) # returns metrics nearest to node
								diff = node.y - nearest
								if (abs(diff) < padding):
									report.add(m.name, g.name, 'Vertical metrics', "%s is off of the %s by %.1f" %( report.node(node), metrics.keys()[metrics.values().index(nearest)], diff), passed=False)

