"""
The test module for the dumpers.
"""

import unittest

from common.datas import Schema, Entry
from common.datas_util import RowsMutableTable
from import_data.dumpers_impls import SimpleCSVDumper, DeletingHandler, \
	SQLiteDumper, SimplyBackupingHandler


###############################################################################
class TestDumpers(unittest.TestCase):
	schema = Schema({"first": "str", "number": "int", "second": "bool", "gender": "enum", "fraction": "decimal"})

	def test_SimpleCSVDumper(self):
		table = self.create_table()
		
		dumper = SimpleCSVDumper()
		dumper.existing_file_handler = DeletingHandler()
		dumper.csv.separator = ';'
		
		self.run_dumper(table, dumper)
		
		
	def test_SQLiteDumper(self):
		table = self.create_table()
		
		dumper = SQLiteDumper()
		dumper.existing_file_handler = SimplyBackupingHandler()
		
		self.run_dumper(table, dumper)
		
###############################################################################	
	
	# creates testing table
	def create_table(self):
		mutable = RowsMutableTable(self.schema)
		mutable.add(Entry.create_new(self.schema, 0, "devnul", {"first": "hello", "number": 42, "second": "world", "gender": "BOTH", "fraction": 0.99}))
		mutable.add(Entry.create_new(self.schema, 1, "devzero", {"first": "world", "number": 99, "second": "HELLO", "gender": "ANY", "fraction": 3.14}))
		return mutable.to_table()

	# runs the dumper itself
	def run_dumper(self, table, dumper):
		print("=======================================================")
		print("Running dumper " + str(dumper))
		dataset_name = "/tmp/testing data set"
		
		file_name = dumper.dump(dataset_name, table)
		print("Runned: Created file: " + file_name)

########################################################################
if __name__ == '__main__':
    unittest.main()
	
		
