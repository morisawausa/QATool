# _OccQATool
This repository holds the Occupant Fonts QA Tool for the Glyphs application. It checks the agreed upon by the team.
> Note: The QA Tool only reports. For scripts to assist in , access the [_GlyphsSCripts](https://github.com/morisawausa/_GlyphsScripts) repository.

## Getting Started

### Installation
Clone this repository into the Scripts folder of your Glyphs application.

Usually, the path to your Glyphs scripts folder is:
`/Users/*yourusername*/Library/Application\ Support/Glyphs/Scripts`

## Usage
Access the QA Tool in Glyphs via `Script > OccQATool > Occupant QA`
> For now, relaunch your tool when running for a different font (in order to load the correct default parameters)

## How it works
1. Select a test or multiple tests
2. Use the default parameters or enter in your own
3. Hit *Run Selected Tests*

# The Report 

## Notes
All notes will be displayed first under REFERENCE.
```
REFERENCE
++++++++++++++++++++++++
.
.
.
```

## Results
All results are consolidated under TEST RESULTS.
They are organized first by master, then by glyph name.
If multiple tests are run, results are consolidated together under each glyph.
```
TEST RESULTS
++++++++++++++++++++++++
.
.
--------------------------------------------------
Master Name
--------------------------------------------------
.
.
Glyph Name
------------
[Result Header] Result description
.
.
```

# The Tests

## Structure
All tests takes the constructor `abstract > task.py`:
```python
# -*- coding: utf-8 -*-
from GlyphsApp import *
from vanilla import *
from abstracts.task import QATask


class Script(QATask):
	"""Test description goes here"""

	def details(self):
		return {
			"name": "Test name",
			"version": "1.0.0",
			"description": "This description will display in the detail view"
			}


	def parameters(self):
		return [
			{"Parameter Name": "Default value"}
		]

	def run(self, parameters, report):

		default = parameters[0]['Parameter Name']
		report.note("\n* Parameter Description: " + default + "\n" )

		for m in self.masters:
			for g in self.glyphs:
				report.add(m.name, g.name, 'Heading', 'Description', passed=False)

```


## Test Objects

For convenience, a few objects set up to be available for any test:
`self.font` Glyphs font object
`self.masters` All masters within the font
`self.glyphs` All glyphs within the font

Access the [Glyphs API](https://docu.glyphsapp.com/index.html) for the Glyphs object model.

## Report Outputs
There are 2 types of outputs from the test.

### Add a Note
Notes do not inherently have a pass/fail status. They are good for noting parameters and reference points for a test.
> **report.note**(string)

#### Parameters
`string` any text


Example
```
report.note("Parameter")
```

### Add a Test result
Use this method when reporting a test result. This logs a line item for the final report output.
> **report.add**(master, glyph, header, desc, passed)

#### Parameters
`master` the name of the master
`glyph` the name of the glyph 
`header` the test label
`desc` the test result description \* integers must be a converted to string values for concatenation
`passed` whether the test passes or fails. Set it to `False` for failed tests, `True` for passed tests.
 
Example
```
report.add(m.name, g.name, 'Overkerns', 'Positive kerning above' + str(kern), passed=False)
```

# Maintenance

## Test Updates
Additional tests can be added by:
1. Writing a test in the predefined format noted in Structure above.
2. Adding the test to the **scripts** folder within the respository.
3. Add the exact test name defined in the test details in the **test_order.txt** file. You can rearrange the order of the tests here.


## Tool Updates
All feature requests and issues of the tool itself are handled in [Github issues](https://github.com/morisawausa/OccQATool/issues).
The Project [QA Tool Updates](https://github.com/morisawausa/OccQATool/projects/1) provides tracking into each.





