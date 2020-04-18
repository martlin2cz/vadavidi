'''
The test for the simple_csv
'''
import unittest

from common.datas import Schema, Table, Entry, ID, SOURCE
from common.simple_csv import SimpleCSV

###############################################################################
class SimpleCSVTest(unittest.TestCase):
    schema = Schema({"foo": "int", "bar": "str"})
    table = Table(schema, [ \
        Entry({ID: 11, SOURCE: "f.txt", "foo": 42, "bar": "lorem"}), \
        Entry({ID: 12, SOURCE: "f.txt", "foo": 99, "bar": "ipsum"}) \
    ])


    def testNoHeadNoMetas(self):
        self.runit(False, False)
    
    def testHeadNoMetas(self):
        self.runit(True, False)
        
    def testNoHeadMetas(self):
        self.runit(False, True)
        
    def testHeadMetas(self):
        self.runit(True, True)
        
        
###############################################################################        
    def runit(self, with_header, with_metas):
        """ Saves and loads back the table with header and metas as 
        specified """
        
        csv = SimpleCSV(with_header, with_metas)
        
        file_name = "/tmp/test-header-{0}-metas-{1}.csv".format(
            with_header, with_metas)
        
        print("Saving to " + file_name)
        csv.save_table(self.table, file_name)
        
        print("Loading from: " + file_name)
        loaded = csv.load_table(self.schema, file_name)
        loaded.printit()
        print("Done " + file_name)
        print()

###############################################################################
if __name__ == "__main__":
    unittest.main()