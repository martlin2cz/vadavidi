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
        
        builder = DefaultObjectBuilder()
        builder.new_object("LoremSimply")
        
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
        
        builder.end_object()
        builder.printit()
        
    def _test_collect_with_collections(self):
        print(" === test_collect_with_collections")
        
        builder = DefaultObjectBuilder()
        builder.new_object("LoremCollections")
        
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
        
        builder.end_object()
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

    def test_first_object_prompter(self):
        print(" === test_first_object_prompter")
        self.run_object_prompter("first-model.yaml", "BaseCalc",
         ["LoremCalc", \
            11, "SitMath", \
                    "ok, here are the pis", \
                    3.14, 3.15, 3.16, \
                    None, \
            "Lorem ipsum" \
            ])
        
    def test_second_object_prompter(self):
        print(" === test_second_object_prompter")
        self.run_object_prompter("second-model.yaml", "BaseOperation",
         ["NaryOperation", \
          "+", "okay, go on the list of operands", \
            "AtomicValueOperation", \
                "VariableAtom", \
                    "x_0", \
            "continue, want add more operands", \
            "BinaryOperation", \
                "*",\
                    "AtomicValueOperation", \
                        "ComplexNumberAtom", \
                            0.9, \
                            1.1, \
                            None,#XXX
                    "AtomicValueOperation", \
                        "IntNumberAtom", \
                            42, \
            "and one more", \
            "UnaryOperation", \
                "~", \
                    "AtomicValueOperation", \
                        "IntNumberAtom", \
                            1010, \
            None \
             ])
        
        
    def run_object_prompter(self, schema_file_name, clazz, answers):
        file_name = TestUtils.test_file_name(schema_file_name)
        schemater = DefaultObjectSchemater.load(file_name)
        
        builder = DefaultObjectBuilder()
        prompter = ObjectPrompter(schemater, builder, clazz)
        
        for answer in answers:
            prompt = prompter.to_next()
            
            print("Prompting: " + str(prompt) + ", getting: " + str(answer)) #prompt.prompt_text
            
            prompter.set_value(answer)
        
        builder.printit()
################################################################################
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()