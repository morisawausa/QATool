# _OccQATool
This repository holds the Occupant Fonts QA Tool for the Glyphs application. It serves as a way to manage the QA items agreed upon by the team and as an interface to run the relevant scripts.
> Note: The QA Tool only reports on items — it will never change anything in your font file. For scripts to assist in glyphs manipulation, access the [_GlyphsScripts](https://github.com/morisawausa/_GlyphsScripts) repository.

## Getting Started

### Installation
Clone this repository into the Scripts folder of your Glyphs application.

Usually, the path to your Glyphs scripts folder is:
`/Users/*yourusername*/Library/Application\ Support/Glyphs/Scripts`

## Usage
![Screenshot of QA Tool](QATool_screenshot.png)
> You should have a font file open before launching the tool. For now, relaunch your tool when running for a different font (in order to load the correct default parameters)

1. Select the font to run QA. It will only run on the selected font.
2. Launch the QA Tool via `Script > OccQATool > Occupant QA`
3. Select a test or multiple tests from the list
4. Verify the default parameters or enter in your own
5. Hit *Run Selected Tests*

## The Report 
There are two types of outputs for the QA Report: **Notes** and **Results**.

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
[Test Label] Result description

...
```

## The Tests

### Structure
All tests inherits the constructor `scripts > abstracts > task.py`. The test *must* follow this template to execute properly from the tool.
If no parameters exist for the test, return an empty list `[]`.

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
			("Parameter Name": "Default value")
		]

	def run(self, parameters, report):

		default = parameters[0][1]
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


#### Code
```python
report.note("* Some message for reference")
```

#### Output
```
* Some message for reference
```


### Log a Test Result
**report.add**(master, glyph, header, desc, passed)

Use this method when reporting a test result. This does 2 things: 
1. Logs a line item under `TEST RESULTS` on the final report output.
2. Adds the description text as an annotation onto the glyph. If there is a specific point included in the description, it will attach the annotation to that point; if not, it will attach the annotation at the top left corner of the glyph.

- `master` (string) The name of the master
- `glyph` (string) The name of the glyph 
- `header` (string) The test label. Appears on the report within brackets `[header]`
- `desc` (string) The test result description. \* Integers must be a converted to string values for concatenation
- `passed` (Boolean) Whether the test passes or fails. Set it to `False` for failed tests, `True` for passed tests.
 

#### Code
```python
report.add(m.name, g.name, 'Overkerns', 'Positive kerning', passed=False)
```

#### Output
```
[Overkerns] Positive kerning
```



### Helper: Format a Point
**report.node**(GSnode)

Use this method to format Glyphs NSPoint Objects such as points, nodes, anchors, or other objects with x and y values. This should be used within the above Log methods.

- `GSnode` (Glyphs point object) Any NSPoint object


#### Code
```python
report.add(m.name, g.name, 'Not straight', "/ %s and %s is off on the X by %i pts" % (report.node(point), report.node(prev_point), skew), passed=False )
```

#### Output
```
[Not straight] / (438.0, 240.0) and (439.0, 288.0) is off on the X by 1 pts
```


## Maintenance

### Test Updates
Additional tests can be added by:
1. Writing a test in the predefined format noted in Structure above.
2. Adding the test to the **scripts** folder within the respository.
3. Add the exact test name defined in the test details in the **test_order.txt** file. You can rearrange the order of the tests here.


### Tool Updates
All feature requests and issues of the tool itself are handled in [Github issues](https://github.com/morisawausa/OccQATool/issues).
Please tag each issue with relevant labels and with the [QA Tool Updates](https://github.com/morisawausa/OccQATool/projects/1) project. This is where issues will be tracked for futher versions of the tool.



