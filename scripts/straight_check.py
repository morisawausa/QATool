# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from abstracts.task import QATask


class Script(QATask):
	"""Checks if there are any path endpoints that are 1pt off."
	"""

	def details(self):
		return {
			"name": "Straight but not straight",
			"version": "1.0.0",
			"description": "For all masters of selected font, checks if any consecutive points are 1pt off."
			}


	def parameters(self):
		return {
		}


	def run(self, parameters, report):
		for m in self.font.masters:
			report.add( "\n\n"+m.name, "\n---------------------------------------------", passed=None )
			previous_glyph=""
			for g in self.font.glyphs:
				layer =  g.layers[m.id]
				points = []

				for path in layer.paths:
					points = []
					for node in path.nodes:
						if node.type == 'line' or node.type == 'curve':
							points.append(node)
				
					for i, val in enumerate(points):
						point = points[i]
						if (i==0):
							prev_point = points[0]
						else:
							prev_point = points[i-1]

						diffX = abs(point.x - prev_point.x)
						diffY = abs(point.y - prev_point.y)
					
						if(diffX==1 or diffY==1):
							if (g != previous_glyph): # avoid repeating glyph name for each point
								report.add( "\n*", g.name, passed=None )
								previous_glyph = g
							if (diffX==1):
								report.add( "x\t", "check horizontal alignment between " + report.node(point) + " and " + report.node(prev_point), passed=False )
							if (diffY==1):
								report.add( "y\t", "check vertical alignment between " + report.node(point) + " and " + report.node(prev_point), passed=False )

							


							# difference = node.y - nearest
							# if (abs(difference) < padding):
							# 	if (g != previous_glyph):
							# 		report.add( "\n*", g.name, passed=None )
							# 		previous_glyph = g

							# 	shift = ""
							# 	point = "[" + str(node.x) + "," + str(node.y) + "]"
								
							# 	def render(shift):
							# 		return "".join([" is ", shift, " the ", metrics[nearest], " by ", str(abs(difference))])
								
							# 	if difference < 0:
							# 		report.add(point, render('below'), passed=False)
							# 	else:
							# 		report.add(point, render('above'), passed=False)
								

