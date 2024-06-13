	# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from .abstracts.task import QATask

class Script(QATask):
	""" Checks vertical alignment of key points across masters.
		Scans for points within the zone threshold around each vertical metric.
	"""

	def details(self):
		return {
			"name": u"Vertical alignment",
			"version": "1.2.0",
			"description": u"Checks if any point falls within the ⚙️Zone threshold. Uses the following references: baseline (H), baseline overshoot (O), ascender (h), descender (p), capheight (H), capheight overshoot (O), xheight (u), xheight overshoot (o). Also checks smallcap height (H.sc) if applicable."
			}


	def parameters(self):
		return [
			("Zone threshold", 3)
		]

	def find_nearest(self, array, value):
		"""Returns the item nearest to the given value within the array"""
		return array[ min( range(len(array)), key = lambda i: abs(array[i]-value) ) ]

	def set_metrics(self, master):
		"""Defines reference points from control glyphs, such as H, O, h, p, u."""

		def ref_bounds(ref):
			reference_glyph = self.glyphs[ref]
			bounds = []
			if reference_glyph:
				glyph = reference_glyph.layers[master.id]
				bounds.append(glyph.bounds.origin.y) #minimum point
				bounds.append(glyph.bounds.origin.y + glyph.bounds.size.height) #max point
			else:
				print("\n⚠️ Reference glyph %s does not exist\n" %ref)
				bounds = [0,0]
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

		padding = parameters[0][1]
		report.note("\n* Buffer: %i\n" % padding)

		for m in self.masters:
			metrics = self.set_metrics(m)
			metrics_output = "\n".join(["%s = %s" % (key, value) for (key, value) in sorted(metrics.items())])
			report.note("\n* %s alignment points:\n%s" % (m.name, metrics_output) )

			for g in self.glyphs:
				layer =  g.layers[m.id]
				for path in layer.paths:
					for node in path.nodes:
						if node.type == 'line' or node.type == 'curve':
							if node.y not in metrics.values():
								nearest = self.find_nearest(list(metrics.values()), node.y) # returns metrics nearest to node
								diff = node.y - nearest
								metric_name = [k for k,v in metrics.items() if v == nearest]
								if (abs(diff) < padding):
									report.add(m.name, g.name, 'Vertical metrics', "%s is off of the %s by %i" %( report.node(node), metric_name, diff), passed=False)

