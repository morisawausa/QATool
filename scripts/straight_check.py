# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from abstracts.task import QATask


class Script(QATask):
	"""Checks if there are any path endpoints that are 1pt off."
	"""

	def details(self):
		return {
			"name": "Almost straight checker",
			"version": "1.0.0",
			"description": "For all masters of selected font, checks if any consecutive points are 1pt off."
			}


	def parameters(self):
		return {
		}


	def run(self, parameters, report):
		for m in self.font.masters:
			report.add( "\n\n\n---------------------------------------------\n" + m.name + "\n---------------------------------------------", passed=None )
			previous_glyph=""

			for g in self.font.glyphs:
				layer =  g.layers[m.id]
				points = []

				for path in layer.paths:
					points = []
					for node in path.nodes:
						points.append(node)
				
					for i, val in enumerate(points):
						point = points[i]
						if i==0:
							prev_point = points[0]
						else:
							prev_point = points[i-1]

						if not (point.type == 'offcurve' and prev_point.type == 'offcurve'):
							# ignore offcurve to offcurve 
							diffX = abs(point.x - prev_point.x)
							diffY = abs(point.y - prev_point.y)
						
							if diffX==1 or diffY==1:
								if g != previous_glyph: # avoid repeating glyph name for each point
									report.add( "\n*" + g.name, passed=None )
									previous_glyph = g
								if diffX==1:
									report.add( report.node(point) + " and " + report.node(prev_point) + " is off on x ", passed=False )
								if diffY==1:
									report.add( report.node(point) + " and " + report.node(prev_point) + " is off on y ", passed=False )

								

