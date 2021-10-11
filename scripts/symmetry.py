# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *

from abstracts.task import QATask

class Script(QATask):
	"""Checks for symmetric sidebearings for certain glyphs.
	"""

	def details(self):
		return {
			"name": u"Symmetric sidebearings",
			"version": "1.0.0",
			"description": u"Checks whether left and right sidebearings are equivalent for the glyphs that are usually symmetric"
			}


	def parameters(self):
		return [
			("List", "Default"),
			("Threshold", 1)
		]

	
	def run(self, parameters, report):

		report.note("\n\n[SYMMETRIC SIDEBEARINGS]\n")
		
		symmetric_list = parameters[0][1]
		if symmetric_list == "Default":
			symmetric_list = ['A', 'Aacute', 'Abreve', 'Acircumflex', 'Adieresis', 'Agrave', 'Amacron', 'Aogonek', 'Aring', 'Aringacute', 'Atilde', 'H', 'Hbar', 'Hcircumflex', 'I', 'Ibreve', 'Icircumflex', 'Idieresis', 'Idotaccent', 'Imacron', 'Itilde', 'M', 'N', 'Nacute', 'Ncaron', 'Ncommaaccent', 'Eng', 'Ntilde', 'O', 'Oacute', 'Obreve', 'Ocircumflex', 'Odieresis', 'Ograve', 'Omacron', 'Oslash', 'Oslashacute', 'Otilde', 'T', 'Tbar', 'Tcaron', 'Tcedilla', 'Tcommaaccent', 'U', 'Uacute', 'Ubreve', 'Ucircumflex', 'Udieresis', 'Ugrave', 'Umacron', 'Uring', 'Utilde', 'V', 'W', 'Wacute', 'Wcircumflex', 'Wdieresis', 'Wgrave', 'X', 'Y', 'Yacute', 'Ycircumflex', 'Ydieresis', 'Ygrave', 'i', 'idotaccent', 'ij', 'l', 'lslash', 'o', 'oacute', 'obreve', 'ocircumflex', 'odieresis', 'ograve', 'omacron', 'oslash', 'oslashacute', 'otilde', 'v', 'w', 'wacute', 'wcircumflex', 'wdieresis', 'wgrave', 'x', 'z', 'zacute', 'zcaron', 'zdotaccent', 'u.salt_simple', 'uacute.salt_simple', 'ubreve.salt_simple', 'ucircumflex.salt_simple', 'udieresis.salt_simple', 'ugrave.salt_simple', 'umacron.salt_simple', 'uogonek.salt_simple', 'uring.salt_simple', 'utilde.salt_simple', 'oslash.NO_BAR', 'ordmasculine', 'A-cy', 'Zhe-cy', 'Ii-cy', 'Iishort-cy', 'Iigrave-cy', 'Em-cy', 'En-cy', 'O-cy', 'Pe-cy', 'Te-cy', 'Ef-cy', 'Ha-cy', 'Sha-cy', 'Dzhe-cy', 'Yeru-cy', 'I-cy', 'Yi-cy', 'Ustraight-cy', 'Ustraightstroke-cy', 'Palochka-cy', 'Zhebreve-cy', 'Abreve-cy', 'Imacron-cy', 'Odieresis-cy', 'Obarred-cy', 'De-cy.loclBGR', 'El-cy.loclBGR', 'zhe-cy', 'ii-cy', 'iishort-cy', 'iigrave-cy', 'em-cy', 'en-cy', 'o-cy', 'pe-cy', 'te-cy', 'ef-cy', 'ha-cy', 'sha-cy', 'dzhe-cy', 'yeru-cy', 'i-cy', 'ustraight-cy', 'ustraightstroke-cy', 'palochka-cy', 'zhebreve-cy', 'imacron-cy', 'odieresis-cy', 'obarred-cy', 'zhe-cy.loclBGR', 'el-cy.loclBGR', 'Alpha', 'Delta', 'Eta', 'Theta', 'Iota', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega', 'Iotadieresis', 'Upsilondieresis', 'gamma', 'theta', 'lambda', 'nu', 'omicron', 'pi', 'upsilon', 'phi', 'chi', 'psi', 'omega', 'upsilontonos', 'upsilondieresis', 'upsilondieresistonos', 'omicrontonos', 'omegatonos', 'zero', 'eight', 'zero.tf', 'eight.tf', 'zeroinferior', 'eightinferior', 'zero.dnom', 'eight.dnom', 'zero.numr', 'eight.numr', 'zerosuperior', 'eightsuperior', 'fraction', 'period', 'colon', 'ellipsis', 'exclam', 'exclamdown', 'periodcentered', 'bullet', 'asterisk', 'numbersign', 'overline', 'slash', 'backslash', 'periodcentered.loclCAT', 'hyphen', 'endash', 'emdash', 'figuredash', 'horizontalbar', 'underscore', 'underscoredbl', 'anoteleia', 'emquad', 'emspace', 'enquad', 'enspace', 'figurespace', 'fourperemspace', 'hairspace', 'sixperemspace', 'space', 'nbspace', 'thinspace', 'threeperemspace', 'zerowidthspace', 'space.frac', '.notdef', 'nonbreakingzerowidthspace', 'currency', 'dollar', 'manat', 'tenge', 'yen', 'bulletoperator', 'divisionslash', 'multiply', 'equal', 'notequal', 'approxequal', 'asciitilde', 'infinity', 'Ohm', 'increment', 'summation', 'percent', 'perthousand', 'lozenge', 'apple', 'at', 'copyright', 'registered', 'published', 'careof', 'degree', 'bar', 'brokenbar', 'dagger', 'daggerdbl', 'dieresiscomb', 'dotaccentcomb', 'circumflexcomb', 'caroncomb', 'brevecomb', 'ringcomb', 'tildecomb', 'macroncomb', 'dotbelowcomb', 'dieresis', 'dotaccent', 'circumflex', 'caron', 'breve', 'ring', 'tilde', 'macron', 'cedilla', 'ogonek', 'tonos', 'dieresistonos', 'breve-cy', 'brevecomb-cy', 'descender-cy', 'zeroslash', 'zeroslash.tf']
		diff = parameters[1][1]

		for m in self.masters:
			for g in self.glyphs:
				if g.name in symmetric_list:
					layer =  g.layers[m.id]
					if abs(layer.LSB - layer.RSB) > diff:
						report.add(m.name, g.name, 'Symmetry', u"⚠️ [ %s ] has a left SB of %i and right SB of %i" % (g.name, layer.LSB, layer.RSB), passed=False)

