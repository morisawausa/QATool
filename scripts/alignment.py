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
			"name": "Vertical metrics checker",
			"version": "1.2.0",
			"description": "For all masters of selected font, checks if any point falls within the {Zone threshold} (3pts by default.) Uses the following glyphs as reference points for alignment: baseline (H), baseline overshoot (O), ascender (h), descender (p), capheight (H), capheight overshoot (O), xheight (u), xheight overshoot (o). If small caps exists, also checks small cap capheight (H.sc)"
			}


	def parameters(self):
		return [
			{"Zone threshold": 3}
		]

	def find_nearest(self, array, value):
		array = np.asarray(array)
		idx = (np.abs(array - value)).argmin()
		return array[idx]
	
	def set_metrics(self):

		def ref_nodes(ref):
			glyph = self.glyphs[ref].layers[self.font.selectedFontMaster.id]
			nodes = []
			for path in glyph.paths:
				for node in path.nodes:
					nodes.append(node.y)
			return nodes

		metrics_dict = {
		 min(ref_nodes('H')): "baseline", 
		 min(ref_nodes('O')): "baseline overshoot",
		 max(ref_nodes('h')): "ascender",
		 min(ref_nodes('p')): "descender", 
		 max(ref_nodes('H')): "capheight",
		 max(ref_nodes('O')): "capheight overshoot",
		 max(ref_nodes('u')): "xheight",
		 max(ref_nodes('o')): "xheight overshoot",
		}

		if self.glyphs["H.sc"] in self.glyphs:
			metrics_dict[max(ref_nodes('H.sc'))] = "smallcapheight"
			metrics_dict[max(ref_nodes('O.sc'))] = "smallcapheight overshoot"
		
		return metrics_dict

	def run(self, parameters, report):

		metrics = self.set_metrics()

		metrics_output = '\n'.join(['%s = %s' % (value, key) for (key, value) in metrics.items()])
		report.note("\n* Alignment metrics:\n" + metrics_output )

		padding = parameters[0]['Zone threshold']
		report.note("\n* Alignment buffer: " + str(padding) + 
		"\n" )

		for m in self.masters:
			for g in self.glyphs:
				layer =  g.layers[m.id]
				for path in layer.paths:
					for node in path.nodes:
						if node.type == 'line' or node.type == 'curve':
							if node.y in metrics.keys():
								break
							else:
								nearest = self.find_nearest(metrics.keys(), node.y)
								diff = node.y - nearest
								if (abs(diff) < padding):
									report.add(m.name, g.name, 'Vertical metrics', report.node(node) + " is off of the " + metrics[nearest] + " by " + str(diff), passed=False)

