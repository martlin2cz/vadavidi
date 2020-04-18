# The impl modules with dumpers

import os
import re
import sqlite3

from common.simple_csv import SimpleCSV
from import_data.base_dumpers import CommonFileDumper, BaseExistingFileHandler, \
	FileDumper


########################################################################
class SimpleCSVDumper(FileDumper):
	""" Just the simple testing dumper dumping to primitive CSV. """

	# the CSV impl	
	csv = SimpleCSV(True, True)
	
	def __init__(self):
		self.namer.extension = 'csv'

	def dump_to_file(self, dataset_name, file_name, table):
		self.csv.save_table(table, file_name)
		
########################################################################
class SQLiteDumper(CommonFileDumper):
	""" The dumper dumping to the sqlite database. """
	
	def __init__(self):
		self.namer.extension = 'db'
	
	def open_the_file(self, dataset_name, file_name):
		return sqlite3.connect(file_name)
		
	def dump_header(self, dataset_name, file_name, con_handle, schema):
		self.create_table(con_handle, dataset_name, schema)
		
	# dumps the body (entries)
	def dump_body(self, dataset_name, file_name, con_handle, schema, entries):
		for entry in entries:
			self.insert_entry(con_handle, dataset_name, schema, entry)
	
	# creates the table
	def create_table(self, conn, dataset_name, schema):
		table_name = self.table_name(dataset_name)
		fields_decl = ", ".join(list(map(
			lambda fn: self.column_name(fn) + " " + self.sql_type_of_field(schema, fn),
			schema)))
		
		sql = "CREATE TABLE {0} (ordnum INT PRIMARY KEY, {1})" \
				.format(table_name, fields_decl)
		#print(sql)
		
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
	
	# inserts the entry into the table
	def insert_entry(self, conn, dataset_name, schema, entry):
		
		table_name = self.table_name(dataset_name)
		fields_decl = ", ".join(list(map(
			lambda fn: self.column_name(fn),
			schema)))
		
		values_decl = ", ".join(list(map(
			lambda fn: "?",
			schema)))
		
		sql = "INSERT INTO {0} ({1}) VALUES ({2})" \
				.format(table_name, fields_decl, values_decl)
		#print(sql)
		
		values = list(map(
			lambda fn: entry.value(fn),
			schema))
		
		c = conn.cursor()
		c.execute(sql, values)
		conn.commit()
		
	# creates name of the table
	def table_name(self, dataset_name):
		return re.sub("[\W]", "_", dataset_name)
	
	# creates name of column	
	def column_name(self, field_name):
		return re.sub("[\W]", "_", field_name)
		
	# obtains sql type of the field
	def sql_type_of_field(self, schema, field_name):
		field_type = schema[field_name]
		
		if field_type in ("int", "integer"):
			return "INT"
			
		if field_type in ("decimal", "float"):
			return "REAL"
		
		if field_type in ("bool", "boolean"):
			return "BOOL"
			
		return "TEXT"

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

