# The impl modules with dumpers

import os
import re
import sqlite3

from common.simple_csv import SimpleCSV
from import_data.base_dumpers import CommonFileDumper, BaseExistingFileHandler, \
	FileDumper
from common.sqlite_db import SQL_LITE_POOL


########################################################################
class SimpleCSVDumper(FileDumper):
	""" Just the simple testing dumper dumping to primitive CSV. """

	# the CSV impl	
	csv = SimpleCSV(True, True)
	
	def __init__(self):
		super().__init__("csv")

	def dump_to_file(self, dataset_name, file_name, table):
		self.csv.save_table(table, file_name)
		
########################################################################
class SQLiteDumper(CommonFileDumper):
	""" The dumper dumping to the sqlite database. """
	
	def __init__(self):
		super().__init__("db")
	
	def open_the_file(self, dataset_name, file_name):
		return SQL_LITE_POOL.get(dataset_name)
		
	def dump_header(self, dataset_name, file_name, sqll_handle, schema):
		sqll_handle.create_table(schema)
		
	def dump_body(self, dataset_name, file_name, sqll_handle, schema, entries):
		for entry in entries:
			sqll_handle.insert_entry(schema, entry)
	
	
	def close_the_file(self, dataset_name, file_name, handle):
		# nothing to do in here
		pass
	
# TODO batch insert sqllite dumper
########################################################################
########################################################################
class DeletingHandler(BaseExistingFileHandler):
	""" The handler which simply the existing files deletes. """
	
	def handle(self, dataset_name, file_name):
		os.remove(file_name)

########################################################################
class SimplyBackupingHandler(BaseExistingFileHandler):
	""" The handler which simply moves the simple backup file. """
	
	def handle(self, dataset_name, file_name):
		backup_file_name = file_name + "_backup"
		os.rename(file_name, backup_file_name)
	
########################################################################
if __name__== "__main__":
	print("Run dumpers_test.TestDumpers to test")

