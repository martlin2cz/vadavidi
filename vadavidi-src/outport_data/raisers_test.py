"""
The test for the raisers.
"""
import unittest

from common.datas import Schema
from outport_data.raisers_impls import SimpleCSVRaiser, SQLLiteRaiser


################################################################################
class RaisersTest(unittest.TestCase):
    schema = Schema({"first": "str", "number": "int", "second": "bool", "gender": "enum", "fraction": "decimal"})

    def test_SimpleCSVRaiser(self):
        raiser = SimpleCSVRaiser()
        raiser.csv.separator = ';'
        
        self.run_raiser(raiser)
    
    def test_SQLLiteRaiser(self):
        raiser = SQLLiteRaiser()
        
        self.run_raiser(raiser)
    
        
################################################################################       
    def run_raiser(self, raiser):
        print("Running raiser " + str(raiser))
        
        table = raiser.run("/tmp/testing data set", self.schema)
        
        table.printit()

################################################################################
if __name__ == "__main__":
    unittest.main()
