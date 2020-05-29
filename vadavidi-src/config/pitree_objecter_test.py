"""
The test module for the pitree based objecter.
"""
import unittest
from common.test_utils import TestUtils
from config.object_schemater_impl import DefaultObjectSchemater
from config.pitree_objecter import PiTreeObjectPrompter
from config.value_obtainers_impls import ClassChoosePrompter
from config.base_objecter import NO_VALUE



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
                    3.14, True, 3.15, True, 3.16, False, \
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
            True, #"continue, want add more operands", \
            "BinaryOperation", \
                "*",\
                    "AtomicValueOperation", \
                        "ComplexNumberAtom", \
                            0.9, \
                            1.1, \
                    "AtomicValueOperation", \
                        "IntNumberAtom", \
                            42, \
            True, #"and one more", \
            "UnaryOperation", \
                "~", \
                    "AtomicValueOperation", \
                        "IntNumberAtom", \
                            1010, \
            True, # okay, the last one
            "PolynomOperation", \
                "okay, telling the cooeficients", \
                "ok, will specify first coef", \
                    "VariableAtom", "x_0", \
                    3, \
                True, #next!
                "ok, will specify second coef", \
                    "IntNumberAtom", 4, \
                    2, \
                True, #next!
                "ok, will specify last coef", \
                "FloatNumberAtom", 0.9, \
                1, \
                False, #ok, done
            False, #and we are done
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