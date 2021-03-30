# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from abstracts.task import QATask

from math import atan2, sqrt, degrees, pi
from AppKit import NSPoint

def round_point(pt, gridLength=1):
	if gridLength == 1:
		return (int(round(pt[0])), int(round(pt[1])))
	elif gridLength == 0:
		return pt
	else:
		x = round(pt[0] / gridLength) * gridLength
		y = round(pt[1] / gridLength) * gridLength
		return (x, y)

def angle_between_points(p0, p1):
	return atan2(p1.position.y - p0.position.y, p1.position.x - p0.position.x)

def distance_between_points(p0, p1):
	return sqrt((p1.position.y - p0.position.y) ** 2 + (p1.position.x - p0.position.x) ** 2)

def distance_between_points_tuple(p0, p1):
	return sqrt((p1[1] - p0[1]) ** 2 + (p1[0] - p0[0]) ** 2)

def difference_vector(p0, p1):
	return (
		p1.position.x - p0.position.x,
		p1.position.y - p0.position.y
	)

def normalize_vector(v0):
	length = sqrt(v0[0] * v0[0] + v0[1] * v0[1])

	if length == 0: return (0.0, 0.0), 0.0

	return (v0[0] / length, v0[1] / length), length

def inner_product(v0, v1):
	return v0[0] * v1[0] + v0[1] * v1[1]


max_incorrect_dot_product_short = 0.2
min_incorrect_dot_product_short = 0.002 # 0.0001 is roughly equivalent to one unit in 1000upm
max_incorrect_dot_product_long = 0.2
min_incorrect_dot_product_long = 0.0002 # 0.0001 is roughly equivalent to one unit in 1000upm



def get_triplets(layer):

	triplets = []

	for contour in layer.paths:
		for index in range(len(contour.nodes)):
			# compute the indices, wrapping around the contour
			prev_index = (index - 1)
			curr_index = index
			next_index = (index + 1) % len(contour)

			# Look up the nodes
			prev = contour.nodes[prev_index]
			curr = contour.nodes[index]
			next = contour.nodes[next_index] # assuming this is a closed contour...


			if (
				prev.type == OFFCURVE and
				curr.type == CURVE and
				next.type == OFFCURVE
			):
				triplets.append([prev, curr, next])

			elif (
				(prev.type == LINE or prev.type == CURVE) and
				(curr.type == LINE or curr.type == CURVE) and
				next.type == OFFCURVE
			):
				triplets.append([prev, curr, next])


			elif (
				prev.type == OFFCURVE and
				(curr.type == LINE or curr.type == CURVE) and
				(next.type == LINE or next.type == CURVE)
			):
		 		triplets.append([prev, curr, next])

	return triplets


def get_tolerances(length_one, length_two):
	l = min(length_one, length_two)

	if l < 10.0:
		return min_incorrect_dot_product_short, max_incorrect_dot_product_short

	else:
		return min_incorrect_dot_product_long, max_incorrect_dot_product_long



def is_triplet_misaligned_RA(triplet):
	prev, curr, next = triplet

	phi1 = angle_between_points(prev, curr)
	phi2 = angle_between_points(curr, next)

	# distance of pt to next reference point
	dist1 = distance_between_points(prev,curr)
	dist2 = distance_between_points(curr, next)

	# print("Checking:")
	# print("  ", self._prev_ref, pt, degrees(phi1), dist1)
	# print("  ", pt, next_ref, degrees(phi2), dist2)

	if dist1 >= dist2:
		# distance 1 is longer, check dist2 for correct angle
		dist = dist2
		phi = phi1
		ref = next
	else:
		# distance 2 is longer, check dist1 for correct angle
		dist = dist1
		phi = phi2 - pi
		ref = prev

	smooth_connection_max_dist = 4.0

	if dist > 2 * smooth_connection_max_dist: # this is smooth_connection_max_distance from red arrow, it's ... something that needs to be upm-normalized
		projected_pt = (
			curr.position.x + dist * cos(phi),
			curr.position.y + dist * sin(phi),
		)

		p = round_point(projected_pt, 1)

		badness = distance_between_points_tuple(
			p, (ref.position.x, ref.position.y) # 1 is self.grid_length in red arrow (by default)
		)

		d = 0.75

		return d < badness

	return False

def is_triplet_misaligned_CN(triplet):
	prev, curr, next = triplet

	diff_one = difference_vector(prev, curr)
	diff_two = difference_vector(curr, next)

	diff_one_norm, length_one = normalize_vector(diff_one)
	diff_two_norm, length_two = normalize_vector(diff_two)

	tolerance_low, tolerance_high = get_tolerances(length_one, length_two)

	similarity = inner_product(diff_one_norm, diff_two_norm)

	return not (
		1.0 - similarity <= tolerance_low or
		1.0 - similarity >= tolerance_high)


def report_errors(report, layer, triplets):
	misaligned = False
	for triplet in triplets:
		bad_triplet = is_triplet_misaligned_CN(triplet)
		misaligned = misaligned or bad_triplet
		if bad_triplet:
			middle_point = triplet[1]
			report.add(layer.name, layer.parent.name, "kink", "node %i at (%i, %i)" % (middle_point.index, middle_point.position.x, middle_point.position.y), passed=False)

	return misaligned


class Script(QATask):
	"""
	Scope: All masters of selected font
	Checks for kinks across all relevant node triplets
	of the selected master.
	"""

	def details(self):
		return {
			"name": u"Kinks",
			"version": "1.0.0",
			"description": u"Checks whether glyphs have kinked points. Can take a long time if run on many masters."
			}

	def parameters(self):
		return []

	def run(self, parameters, report):

		report.note("\n\n[KINKS]\n")

		for m in self.masters:
			layers = map(lambda g: filter(lambda l: l.associatedMasterId == m.id, g.layers)[0], Glyphs.font.glyphs)

			for layer in layers:
				triplets = get_triplets(layer)
				error = report_errors(report, layer, triplets)
