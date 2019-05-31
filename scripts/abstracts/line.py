# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *


class QALine():

	def __init__(self, passed, desc):
		self.passed = passed
		self.desc = desc