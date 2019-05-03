# -*- coding: utf-8 -*-

from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import *

from ..models.task import QATask

class CompareGlyphNames(QATask):
    """Goes through all glyph names and checks against master list.
    Colors glyphs not present in the list orange, and outputs any missing glyph names in the macros panel.
    """

    def details():
        return {
            "name": "Compare Glyph Names",
            "version": "1.0.0",
            "description": "Goes through all glyph names and checks against master list. Colors glyphs not present in the list orange, and outputs any missing glyph names in the macros panel."
        }

    def run( self, parameters, report ):
    	masterList = ["A", "Aacute", "Abreve", "Acircumflex", "Adieresis", "Agrave", "Amacron", "Aogonek", "Aring", "Aringacute", "Atilde", "AE", "AEacute", "B", "C", "Cacute", "Ccaron", "Ccedilla", "Ccircumflex", "Cdotaccent", "D", "Eth", "Dcaron", "Dcroat", "E", "Eacute", "Ebreve", "Ecaron", "Ecircumflex", "Edieresis", "Edotaccent", "Egrave", "Emacron", "Eogonek", "F", "G", "Gbreve", "Gcircumflex", "Gcommaaccent", "Gdotaccent", "H", "Hbar", "Hcircumflex", "I", "IJ", "Iacute", "Ibreve", "Icircumflex", "Idieresis", "Idotaccent", "Igrave", "Imacron", "Iogonek", "Itilde", "J", "Jcircumflex", "K", "Kcommaaccent", "L", "Lacute", "Lcaron", "Lcommaaccent", "Ldot", "Lslash", "M", "N", "Nacute", "Ncaron", "Ncommaaccent", "Eng", "Ntilde", "O", "Oacute", "Obreve", "Ocircumflex", "Odieresis", "Ograve", "Ohungarumlaut", "Omacron", "Oslash", "Oslashacute", "Otilde", "OE", "P", "Thorn", "Q", "R", "Racute", "Rcaron", "Rcommaaccent", "S", "Sacute", "Scaron", "Scedilla", "Scircumflex", "Scommaaccent", "Germandbls", "Schwa", "T", "Tbar", "Tcaron", "Tcedilla", "Tcommaaccent", "U", "Uacute", "Ubreve", "Ucircumflex", "Udieresis", "Ugrave", "Uhungarumlaut", "Umacron", "Uogonek", "Uring", "Utilde", "V", "W", "Wacute", "Wcircumflex", "Wdieresis", "Wgrave", "X", "Y", "Yacute", "Ycircumflex", "Ydieresis", "Ygrave", "Z", "Zacute", "Zcaron", "Zdotaccent", "Iacute_J.loclNLD", "Jacute.loclNLD", "a", "aacute", "abreve", "acircumflex", "adieresis", "agrave", "amacron", "aogonek", "aring", "aringacute", "atilde", "ae", "aeacute", "b", "c", "cacute", "ccaron", "ccedilla", "ccircumflex", "cdotaccent", "d", "eth", "dcaron", "dcroat", "e", "eacute", "ebreve", "ecaron", "ecircumflex", "edieresis", "edotaccent", "egrave", "emacron", "eogonek", "schwa", "f", "g", "gbreve", "gcircumflex", "gcommaaccent", "gdotaccent", "h", "hbar", "hcircumflex", "i", "idotless", "iacute", "ibreve", "icircumflex", "idieresis", "igrave", "ij", "imacron", "iogonek", "itilde", "j", "jdotless", "jcircumflex", "k", "kcommaaccent", "kgreenlandic", "l", "lacute", "lcaron", "lcommaaccent", "ldot", "lslash", "m", "n", "nacute", "ncaron", "ncommaaccent", "eng", "ntilde", "o", "oacute", "obreve", "ocircumflex", "odieresis", "ograve", "ohungarumlaut", "omacron", "oslash", "oslashacute", "otilde", "oe", "p", "thorn", "q", "r", "racute", "rcaron", "rcommaaccent", "s", "sacute", "scaron", "scedilla", "scircumflex", "scommaaccent", "germandbls", "longs", "t", "tbar", "tcaron", "tcedilla", "tcommaaccent", "u", "uacute", "ubreve", "ucircumflex", "udieresis", "ugrave", "uhungarumlaut", "umacron", "uogonek", "uring", "utilde", "v", "w", "wacute", "wcircumflex", "wdieresis", "wgrave", "x", "y", "yacute", "ycircumflex", "ydieresis", "ygrave", "z", "zacute", "zcaron", "zdotaccent", "iacute_j.loclNLD", "jacute.loclNLD", "f_f", "f_f_i", "f_f_l", "f_i", "f_j", "f_l", "f_t", "ordfeminine", "ordmasculine", "A-cy", "Be-cy", "Ve-cy", "Ge-cy", "Gje-cy", "Gheupturn-cy", "De-cy", "Ie-cy", "Iegrave-cy", "Io-cy", "Zhe-cy", "Ze-cy", "Ii-cy", "Iishort-cy", "Iigrave-cy", "Ka-cy", "Kje-cy", "El-cy", "Em-cy", "En-cy", "O-cy", "Pe-cy", "Er-cy", "Es-cy", "Te-cy", "U-cy", "Ushort-cy", "Ef-cy", "Ha-cy", "Che-cy", "Tse-cy", "Sha-cy", "Shcha-cy", "Dzhe-cy", "Softsign-cy", "Hardsign-cy", "Yeru-cy", "Lje-cy", "Nje-cy", "Dze-cy", "E-cy", "Ereversed-cy", "I-cy", "Yi-cy", "Je-cy", "Tshe-cy", "Iu-cy", "Ia-cy", "Dje-cy", "Ghestroke-cy", "Zhedescender-cy", "Zedescender-cy", "Kadescender-cy", "Kabashkir-cy", "Endescender-cy", "Esdescender-cy", "Ustrait-cy", "Ustraitstroke-cy", "Hadescender-cy", "Chedescender-cy", "Shha-cy", "Palochka-cy", "Zhebreve-cy", "Abreve-cy", "Aie-cy", "Iebreve-cy", "Schwa-cy", "Imacron-cy", "Odieresis-cy", "Obarred-cy", "Umacron-cy", "Uhungarumlaut-cy", "De-cy.loclBGR", "El-cy.loclBGR", "Ef-cy.loclBGR", "Esdescender-cy.loclCHU", "a-cy", "be-cy", "ve-cy", "ge-cy", "gje-cy", "gheupturn-cy", "de-cy", "ie-cy", "iegrave-cy", "io-cy", "zhe-cy", "ze-cy", "ii-cy", "iishort-cy", "iigrave-cy", "ka-cy", "kje-cy", "el-cy", "em-cy", "en-cy", "o-cy", "pe-cy", "er-cy", "es-cy", "te-cy", "u-cy", "ushort-cy", "ef-cy", "ha-cy", "che-cy", "tse-cy", "sha-cy", "shcha-cy", "dzhe-cy", "softsign-cy", "hardsign-cy", "yeru-cy", "lje-cy", "nje-cy", "dze-cy", "e-cy", "ereversed-cy", "i-cy", "yi-cy", "je-cy", "tshe-cy", "iu-cy", "ia-cy", "dje-cy", "ghestroke-cy", "zhedescender-cy", "zedescender-cy", "kadescender-cy", "kabashkir-cy", "endescender-cy", "esdescender-cy", "ustrait-cy", "ustraitstroke-cy", "hadescender-cy", "chedescender-cy", "shha-cy", "palochka-cy", "zhebreve-cy", "abreve-cy", "aie-cy", "iebreve-cy", "schwa-cy", "imacron-cy", "odieresis-cy", "obarred-cy", "umacron-cy", "uhungarumlaut-cy", "ve-cy.loclBGR", "ge-cy.loclBGR", "de-cy.loclBGR", "zhe-cy.loclBGR", "ze-cy.loclBGR", "ii-cy.loclBGR", "iishort-cy.loclBGR", "iigrave-cy.loclBGR", "ka-cy.loclBGR", "el-cy.loclBGR", "pe-cy.loclBGR", "te-cy.loclBGR", "tse-cy.loclBGR", "sha-cy.loclBGR", "shcha-cy.loclBGR", "softsign-cy.loclBGR", "hardsign-cy.loclBGR", "iu-cy.loclBGR", "esdescender-cy.loclCHU", "be-cy.loclSRB", "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega", "Alphatonos", "Epsilontonos", "Etatonos", "Iotatonos", "Omicrontonos", "Upsilontonos", "Omegatonos", "Iotadieresis", "Upsilondieresis", "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", "sigmafinal", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega", "iotatonos", "iotadieresis", "iotadieresistonos", "upsilontonos", "upsilondieresis", "upsilondieresistonos", "omicrontonos", "omegatonos", "alphatonos", "epsilontonos", "etatonos", "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "zero.sinf", "one.sinf", "two.sinf", "three.sinf", "four.sinf", "five.sinf", "six.sinf", "seven.sinf", "eight.sinf", "nine.sinf", "zero.tnum", "one.tnum", "two.tnum", "three.tnum", "four.tnum", "five.tnum", "six.tnum", "seven.tnum", "eight.tnum", "nine.tnum", "zero.dnom", "one.dnom", "two.dnom", "three.dnom", "four.dnom", "five.dnom", "six.dnom", "seven.dnom", "eight.dnom", "nine.dnom", "zero.numr", "one.numr", "two.numr", "three.numr", "four.numr", "five.numr", "six.numr", "seven.numr", "eight.numr", "nine.numr", "zero.sups", "one.sups", "two.sups", "three.sups", "four.sups", "five.sups", "six.sups", "seven.sups", "eight.sups", "nine.sups", "fraction", "onehalf", "onequarter", "threequarters", "oneeighth", "threeeighths", "fiveeighths", "seveneighths", "period", "comma", "colon", "semicolon", "ellipsis", "exclam", "exclamdown", "question", "questiondown", "periodcentered", "bullet", "asterisk", "numbersign", "overline", "slash", "backslash", "periodcentered.case", "periodcentered.loclCAT.case", "periodcentered.loclCAT", "period.tnum", "comma.tnum", "colon.tnum", "semicolon.tnum", "numbersign.tnum", "parenleft", "parenright", "braceleft", "braceright", "bracketleft", "bracketright", "hyphen", "endash", "emdash", "figuredash", "horizontalbar", "underscore", "underscoredbl", "quotesinglbase", "quotedblbase", "quotedblleft", "quotedblright", "quoteleft", "quoteright", "guillemetleft", "guillemetright", "guilsinglleft", "guilsinglright", "quotedbl", "quotesingle", "anoteleia", "questiongreek", "emquad", "emspace", "enquad", "enspace", "figurespace", "fourperemspace", "hairspace", "sixperemspace", "space", "thinspace", "threeperemspace", "zerowidthspace", ".notdef", "nonbreakingzerowidthspace", "baht", "cedi", "cent", "colonsign", "currency", "dollar", "dong", "euro", "florin", "franc", "guarani", "hryvnia", "lira", "liraTurkish", "manat", "naira", "peseta", "peso", "ruble", "rupeeIndian", "sterling", "tenge", "tugrik", "won", "yen", "cent.tnum", "dollar.tnum", "euro.tnum", "florin.tnum", "sterling.tnum", "yen.tnum", "bulletoperator", "divisionslash", "plus", "minus", "multiply", "divide", "equal", "notequal", "greater", "less", "greaterequal", "lessequal", "plusminus", "approxequal", "logicalnot", "asciitilde", "asciicircum", "infinity", "integral", "Ohm", "increment", "product", "summation", "radical", "partialdiff", "micro", "percent", "perthousand", "plus.tnum", "minus.tnum", "multiply.tnum", "divide.tnum", "equal.tnum", "greater.tnum", "less.tnum", "lozenge", "apple", "at", "ampersand", "paragraph", "section", "copyright", "registered", "published", "trademark", "careof", "degree", "minute", "second", "bar", "brokenbar", "dagger", "literSign", "daggerdbl", "numero", "estimated", "servicemark", "apostrophemod", "dieresiscomb", "dotaccentcomb", "gravecomb", "acutecomb", "hungarumlautcomb", "circumflexcomb", "caroncomb", "brevecomb", "ringcomb", "tildecomb", "macroncomb", "commaturnedabovecomb", "dotbelowcomb", "commaaccent", "commaaccentcomb", "cedillacomb", "ogonekcomb", "acute", "breve", "caron", "cedilla", "circumflex", "dieresis", "dotaccent", "grave", "hungarumlaut", "macron", "ogonek", "ring", "tilde", "dieresiscomb.case", "dotaccentcomb.case", "gravecomb.case", "acutecomb.case", "hungarumlautcomb.case", "circumflexcomb.case", "caroncomb.case", "brevecomb.case", "ringcomb.case", "tildecomb.case", "macroncomb.case", "dotbelowcomb.case", "commaaccentcomb.case", "cedillacomb.case", "ogonekcomb.case", "tonos", "dieresistonos", "NUL", "zeroslash", "caronvert", "caronvertcomb.case", "caronvertcomb", "commaturnedabove", "Zeacute-cy", "esacute-cy", "breve-cy", "zeacute-cy", "Esacute-cy"]
    	missingList = masterList

    	allGlyphs = Glyphs.font.glyphs

    	for thisGlyph in allGlyphs:
    		name = thisGlyph.name
    		if name in masterList:
    			missingList.remove(name)
    		else:
    			thisGlyph.color = 1
    			print name, "is not a standard name"
    			# orange if glyph name is not on master list

    	print len(missingList), " missing glyphs:", missingList
