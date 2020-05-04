"""
The test module for the objecter.
"""
import unittest

from common.test_utils import TestUtils
from config.object_builder_impl import DefaultObjectBuilder
from config.object_schemater_impl import DefaultObjectSchemater, \
    SchematerObjectModel, SchematerModel
from config.value_obtainers_impls import SimpleValuePrompter


################################################################################
class TestObjecter(unittest.TestCase):

################################################################################

    def test_simple_builder_collect(self):
        builder = DefaultObjectBuilder("LoremSimply")
        builder.add_field("foo").set_value(42)
        builder.add_field("bar").set_value(99)
        
        builder.add_field("foo").new_object("IpsumSimply")
        builder.add_field("karel").set_value(True)
        
        builder.add_field("jirka").new_object("DolorSimply")
        builder.end_object()
        
        builder.add_field("franta").set_value(False)
        builder.end_object()
        
        builder.add_field("baz").set_value(111)
        
        builder.add_field("aux").new_object("Sit")
        builder.add_field("jitka").set_value("MAYBE")
        builder.end_object()
        
        builder.end_object()
        
        builder.printit()
        
    def test_collect_with_collections(self):
        builder = DefaultObjectBuilder("LoremCollections")
        builder.add_field("foo").set_value(42)
        
        builder.add_field("bar").new_list()
        builder.add_list_item().set_value(420)
        
        builder.new_object("IpsumCollections")
        builder.add_field("nope").set_value(None)
        builder.end_object()

        builder.add_list_item().new_list()
        builder.add_list_item().set_value(False)
        builder.end_list()
        
        builder.end_list()
        
        builder.add_field("baz").new_dict()
        builder.add_dict_key().set_value("lorem")
        builder.add_dict_value().set_value("LOREM")
        
        builder.add_dict_key().set_value("ipsum")
        builder.add_dict_value().set_value("IPSUM")
        
        builder.add_dict_key().new_object("DolorKey")
        builder.end_object()
        builder.add_dict_value().new_list()
        builder.add_list_item().set_value("Not empty list")
        builder.end_list()
        
        builder.end_dict()
        
        builder.printit()

################################################################################
    def test_object_schemater(self):
        schemater = DefaultObjectSchemater()
        
        lorem = SchematerObjectModel("BaseCalc", { \
                "lorem": SimpleValuePrompter("The lorem value", "str"), \
                "length": SimpleValuePrompter("Length of that", "int") \
            })
        
        ipsum = SchematerObjectModel("BaseCalc", { })
        dolor = SchematerObjectModel("BaseMath", { })
        
        objects = {"LoremCalc": lorem, "IpsumCalc": ipsum, "DolorMath": dolor}
        schemater.model = SchematerModel(objects)
        
        print(schemater.list_impls("BaseCalc"))
        print(schemater.list_impls("BaseMath"))
        print(schemater.list_fields("LoremCalc"))

################################################################################
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()