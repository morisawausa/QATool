# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from abstracts.task import QATask

import numpy as np

class Script(QATask):
	"""Checks vertical alignment of key points across masters. Uses a threshold to scan for points within each vertical metric"
	"""

	def details(self):
		return {
			"name": "Vertical metrics checker",
			"version": "1.0.0",
			"description": "For all masters of selected font, checks if any point falls within the error threshold. Checks against metrics based off of reference glyphs as follows: baseline (H), baseline overshoot (O), ascender (h), descender(p), capheight(H), capheight overshoot (O), xheight (u), xheight overshoot (o)."
			}


	def parameters(self):
		return {
			"Zone Threshold": 3,
		}

	def findNearest(self, array, value):
		array = np.asarray(array)
		idx = (np.abs(array - value)).argmin()
		return array[idx]
	
	def setMetrics(self):
		self.master = self.font.selectedFontMaster.id

		def ref_nodes(ref):
			glyph = self.font.glyphs[ref].layers[self.master]
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
		
		return metrics_dict

	def run(self, parameters, report):
		metrics = self.setMetrics()
		metrics_output = '\n'.join(['%s = %s' % (value, key) for (key, value) in metrics.items()])

		report.add( "Alignment metrics:\n" + metrics_output, passed=None )

		padding = parameters['Zone Threshold']
		report.add( "\nAlignment buffer: " + str(padding), passed=None )

		for m in self.font.masters:
			report.add( "\n\n\n---------------------------------------------\n" + m.name + "\n---------------------------------------------", passed=None )
			previous_glyph=""
			for g in self.font.glyphs:
				layer =  g.layers[m.id]
				for path in layer.paths:
					for node in path.nodes:
						if node.type == 'line' or node.type == 'curve':
							if node.y in metrics.keys():
								break
							else:
								nearest = self.findNearest(metrics.keys(), node.y)
								difference = node.y - nearest
								if (abs(difference) < padding):
									if (g != previous_glyph): # avoid repeating glyph name for each point
										report.add( "\n*" + g.name, passed=None )
										previous_glyph = g

									shift = ""

									def note(shift):
										return "".join([" is ", shift, " the ", metrics[nearest], " by ", str(abs(difference))])
									
									if difference < 0:
										report.add(report.node(node) + note('below'), passed=False)
									else:
										report.add(report.node(node) + note('above'), passed=False)

