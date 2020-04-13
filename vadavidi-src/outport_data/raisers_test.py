import unittest

from common.datas import Schema
from outport_data.raisers_impls import SimpleCSVRaiser


################################################################################
class RaisersTest(unittest.TestCase):
    schema = Schema({"ordernum":"int","first": "str", "number": "int", "second": "bool", "gender": "enum", "fraction": "decimal"})

    def test_SimpleCSVRaiser(self):
        raiser = SimpleCSVRaiser()
        raiser.csv.separator = ';'
        
        self.runRaiser(raiser)
        
        
    def runRaiser(self, raiser):
        print("Running raiser " + str(raiser))
        
        table = raiser.run("/tmp/testing data set 2", self.schema)
        
        table.printit()

################################################################################

if __name__ == "__main__":
    unittest.main()
