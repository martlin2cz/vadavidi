"""
The test module for the objecter.
"""
import unittest

from common.test_utils import TestUtils
from config.object_builder_impl import DefaultObjectBuilder
from config.object_schemater_impl import DefaultObjectSchemater, \
    SchematerObjectModel, SchematerModel, \
    IMPORTER_SCHEMATER_FILE
from config.object_schemater_producer import DefaultSchematerProducer
from config.value_obtainers_impls import SimpleValuePrompter,\
    ClassChoosePrompter
from config.object_prompter import ObjectPrompter


################################################################################
class TestObjecter(unittest.TestCase):

################################################################################

    def _test_simple_builder_collect(self):
        print(" === test_simple_builder_collect")
        
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
        
    def _test_collect_with_collections(self):
        print(" === test_collect_with_collections")
        
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
    def _test_object_schemater(self):
        print(" === test_object_schemater")
        
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
        
    def _test_object_schemater_load(self):
        print(" === test_object_schemater_load")
        
        file_name = TestUtils.test_file_name("first-model.yaml")
        schemater = DefaultObjectSchemater.load(file_name)
        print(schemater)

    def _test_common_schematers(self):
        print(" === test_common_schematers")

        print(DefaultObjectSchemater.load(IMPORTER_SCHEMATER_FILE))

################################################################################
    def _test_schemater_producer(self):
        print(" === test_schemater_producer")
        
        producer = DefaultSchematerProducer()
        producer.lookup_package_names = ["import_data"]

        #print("\n PKG:".join(map(str, producer.list_packages())))
        #print("\n MOD:".join(map(str, producer.list_modules())))
        #print("\n CLS:".join(list(map(str, producer.list_classes()))[slice(1, 10)]))

        base_class = "BaseParser"
        model = producer.generate_model(base_class)
        print(model)
        
        DefaultSchematerProducer.save(model, "/tmp/model-of-parser.yaml")

################################################################################

    def test_object_prompter(self):
        file_name = TestUtils.test_file_name("first-model.yaml")
        schemater = DefaultObjectSchemater.load(file_name)
        
        clazz = "BaseCalc"
        builder = DefaultObjectBuilder(clazz)
        
        prompter = ObjectPrompter(schemater, builder, clazz)
        
        num = 0;
        while True:
            prompt = prompter.to_next()
            print("WILL PROMPT: " + str(prompt))
            if prompt is None:
                break
            
            if (isinstance(prompt, ClassChoosePrompter)):
                impls = schemater.list_impls(prompt.clazz)
                prompter.set_value(impls[-1])
            else:
                prompter.set_value(num)
            
            num += 1
        

################################################################################
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()