import objc
from GlyphsApp import *
from vanilla import *

class QAProfile():
    """The QAProfile class manages which tasks are activated
    and which are inactive, as well as defining custom parameters
    for the typeface.
    """


    def __init__(self):
        """Set up our dictionary of task parameters
        and our task ordering later use.
        """
        self.tasks = dict()
        self.task_order = list()


    def run(self, pool):
        """Given a pool of available tasks,
        run the tasks specified in self.tasks and report
        the result.
        """
        return list(), list(), list()


    def save(self):
        """Save the currently specified QATask parameters to
        the current font's customParameters fields."""
        return self


    def load(self):
        """Load the parameters for the specified QATasks to
        from the current font's custom oaraneters fields."""
        return self


    def activate(self, task_name):
        """Mark the given task as active"""
        return self


    def deactivate(self, task_name):
        """Mark the given task as inactive"""
        return self
