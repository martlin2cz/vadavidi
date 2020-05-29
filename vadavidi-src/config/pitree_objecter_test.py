"""
The test module for the pitree based objecter.
"""
import unittest
from common.test_utils import TestUtils
from config.object_schemater_impl import DefaultObjectSchemater
from config.pitree_objecter import PiTreeObjectPrompter
from config.value_obtainers_impls import ClassChoosePrompter



################################################################################
class TestPiTreeObjecter(unittest.TestCase):

################################################################################

   
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
            #"continue, want add more operands", \
            "BinaryOperation", \
                "*",\
                    "AtomicValueOperation", \
                        "ComplexNumberAtom", \
                            0.9, \
                            1.1, \
                    "AtomicValueOperation", \
                        "IntNumberAtom", \
                            42, \
            #"and one more", \
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
        
        root_prompter = ClassChoosePrompter(clazz, "Specify the whole object") 
        prompter = PiTreeObjectPrompter(schemater, root_prompter)
        
        for answer in answers:
            prompt = prompter.to_next()
                
            print("Prompting: " + str(prompt.prompt_text) + ", getting: " + str(answer)) #prompt.prompt_text
            
            prompter.specify_value(answer)
            
        prompter.tree.printit()
################################################################################
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()