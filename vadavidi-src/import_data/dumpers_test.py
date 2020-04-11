# the test module for the dumpers

import unittest
from datas import Schema, Entry, Table
from datas_util import MutableTable
from dumpers_impls import SimpleCSVDumper, SQLiteDumper, DeletingHandler, SimplyBackupingHandler

########################################################################
# tests the parsers
class TestDumpers(unittest.TestCase):
	schema = Schema({"first": "str", "number": "int", "second": "bool", "gender": "enum", "fraction": "decimal"})

	def test_SimpleCSVDumper(self):
		table = self.createTable()
		
		dumper = SimpleCSVDumper()
		dumper.existingFileHandler = DeletingHandler()
		
		self.runDumper(table, dumper)
		
		
	def test_SQLiteDumper(self):
		table = self.createTable()
		
		dumper = SQLiteDumper()
		dumper.existingFileHandler = SimplyBackupingHandler()
		
		self.runDumper(table, dumper)
		
	# creates testing table
	def createTable(self):
		mutable = MutableTable(self.schema)
		mutable.add(Entry.create(self.schema, 0, {"first": "hello", "number": 42, "second": "world", "gender": "BOTH", "fraction": 0.99}))
		mutable.add(Entry.create(self.schema, 1, {"first": "world", "number": 99, "second": "HELLO", "gender": "ANY", "fraction": 3.14}))
		return mutable.toTable()

	# runs the dumper itself
	def runDumper(self, table, dumper):
		print("=======================================================")
		print("Running dumper " + str(dumper))
		datasetName = "/tmp/testing data set"
		
		filename = dumper.dump(datasetName, table)
		print("Runned: Created file: " + filename)

########################################################################
if __name__ == '__main__':
    unittest.main()
	
		
