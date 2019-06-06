# _OccQATool
This repository holds the Occupant Fonts QA Tool for the Glyphs application. It serves as a way to manage the QA items agreed upon by the team as well as as an interface to run the scripts.
> Note: The QA Tool only reports on items — it will never change anything in your font file. For scripts to assist in glyphs manipulation, access the [_GlyphsScripts](https://github.com/morisawausa/_GlyphsScripts) repository.

## Getting Started

### Installation
Clone this repository into the Scripts folder of your Glyphs application.

Usually, the path to your Glyphs scripts folder is:
`/Users/*yourusername*/Library/Application\ Support/Glyphs/Scripts`

## Usage
Access the QA Tool in Glyphs via `Script > OccQATool > Occupant QA`
> You should have a font file open before launching the tool. For now, relaunch your tool when running for a different font (in order to load the correct default parameters)

## How it works
1. Select a test or multiple tests
2. Use the default parameters or enter in your own
3. Hit *Run Selected Tests*

## The Report 
There are two types of outputs for the QA Report: a) Notes and b) Results.

### Notes
All notes will be displayed first under REFERENCE.
```
REFERENCE
++++++++++++++++++++++++

Notes
...
```

### Results
All results are consolidated under TEST RESULTS.
They are organized first by master, then by glyph name.
If multiple tests are run, results are consolidated together under each glyph.
```
TEST RESULTS
++++++++++++++++++++++++

------------------------------------------------------------------------------------------
Master Name
------------------------------------------------------------------------------------------

Glyph Name
------------
[Test Label] Test description

...
```

## The Tests

### Structure
All tests inherits the constructor `abstract > task.py`. The test *must* follow this template to execute properly from the tool.
If no parameters exist for the test, simply return nothing.

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



### Test Objects

For convenience, a few objects set up to be available for any test:
- `self.font` Glyphs font object
- `self.masters` All masters within the font
- `self.glyphs` All glyphs within the font

Access the [Glyphs API](https://docu.glyphsapp.com/index.html) for the Glyphs object model.


### Log a Note
**report.note**(string)

Notes do not inherently have a pass/fail status. They are good for noting parameters and reference points for a test and will appear under `REFERENCE` on the final report output.


- `string` (string) any text

```python
report.note("Parameter Message")
```

### Log a Test Result
**report.add**(master, glyph, header, desc, passed)

Use this method when reporting a test result. This logs a line item under `TEST RESULTS` on the final report output.

- `master` (string) The name of the master
- `glyph` (string) The name of the glyph 
- `header` (string) The test label. Appears on the report within brackets `[header]`
- `desc` (string) The test result description. \* Integers must be a converted to string values for concatenation
- `passed` (Boolean) Whether the test passes or fails. Set it to `False` for failed tests, `True` for passed tests.
 
```python
report.add(m.name, g.name, 'Overkerns', 'Positive kerning above' + str(kern), passed=False)
```

## Maintenance

### Test Updates
Additional tests can be added by:
1. Writing a test in the predefined format noted in Structure above.
2. Adding the test to the **scripts** folder within the respository.
3. Add the exact test name defined in the test details in the **test_order.txt** file. You can rearrange the order of the tests here.


### Tool Updates
All feature requests and issues of the tool itself are handled in [Github issues](https://github.com/morisawausa/OccQATool/issues).
The Project [QA Tool Updates](https://github.com/morisawausa/OccQATool/projects/1) provides tracking into each.





