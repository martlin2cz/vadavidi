"""
The test module for the objecter.
"""
import unittest

from config.objecter import AutomatedObjectBuilder


################################################################################
class TestObjecter(unittest.TestCase):

    def test_simple_builder_collect(self):
        builder = AutomatedObjectBuilder("Lorem")
        builder.set("foo", 42)
        builder.set("bar", 99)
        
        builder.set_object("foo", "Ipsum")
        builder.set("karel", True)
        
        builder.set_object("jirka", "Dolor")
        builder.end_object()
        
        builder.set("franta", False)
        builder.end_object()
        
        builder.set("baz", 111)
        
        builder.set_object("aux", "Sit")
        builder.set("jitka", "MAYBE")
        builder.end_object()
        
        builder.end_object()
        
        builder.printit()

################################################################################

################################################################################
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()