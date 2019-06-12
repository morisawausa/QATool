# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from abstracts.task import QATask


class Script(QATask):
	"""Checks for paths or handles that are supposed to be straight."""

	def details(self):
		return {
			"name": "Almost straights",
			"version": "1.0.0",
			"description": "For all masters of selected font, checks if any consecutive points are off by the {Skew threshold} (1pt by default.)"
			}


	def parameters(self):
		return [
			("Skew threshold", 1)
		]


	def run(self, parameters, report):

		report.note("\n\n[ALMOST STRAIGHTS]\n")

		skew = parameters[0][1]
		
		report.note("* Skewed by: %i pts \n" % skew)

		for m in self.masters:
			for g in self.glyphs:
				layer =  g.layers[m.id]
				points = []
				for path in layer.paths:
					points = []
					for node in path.nodes:
						points.append(node)
				
					for i, val in enumerate(points):
						point = points[i]
						if i == 0:
							prev_point = points[0]
						else:
							prev_point = points[i-1]

						if not (point.type == 'offcurve' and prev_point.type == 'offcurve'):
							# ignore offcurve to offcurve 
							diffX = abs(point.x - prev_point.x)
							diffY = abs(point.y - prev_point.y)
						
							if diffX == skew or diffY == skew:
								if diffX == skew:
									report.add(m.name, g.name, 'Not straight', "/ %s and %s is off on the X by %i pts" % (report.node(point), report.node(prev_point), skew), passed=False )
								if diffY == skew:
									report.add(m.name, g.name, 'Not straight', "/ %s and %s is off on the Y by %i pts" % (report.node(point), report.node(prev_point), skew), passed=False )
