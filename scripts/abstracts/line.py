# -*- coding: utf-8 -*-
import objc
from GlyphsApp import *
from vanilla import *


class QALine():

	def __init__(self, passed, header, desc):
		self.passed = passed
		self.header = header
		self.desc = desc