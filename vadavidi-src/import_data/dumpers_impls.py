# The impl modules with dumpers

import os
import re
import sqlite3

from common.simple_csv import SimpleCSV
from import_data.base_dumpers import CommonFileDumper, BaseExistingFileHandler, \
	FileDumper


########################################################################
########################################################################
# Just the simple testing dumper dumping to primitive CSV
class SimpleCSVDumper(FileDumper):
	csv = SimpleCSV()
	
	# constructor
	def __init__(self):
		self.namer.extension = 'csv'


	def dumpToFile(self, datasetName, fileName, table):
		schema = table.schema
		lines = [self.csv.schemaToLine(schema)] \
			+ list(map(lambda e: self.csv.entryToLine(schema, e),
					table.list()))
			
		self.csv.saveLines(lines, fileName)
		
########################################################################
# The dumper dumping to the sqlite database
class SQLiteDumper(CommonFileDumper):

	# constructor
	def __init__(self):
		self.namer.extension = 'db'
	
	# opens the file, returns the handle
	def openTheFile(self, datasetName, fileName):
		return sqlite3.connect(fileName)
		
	# dumps some header (the schema, i guess)
	def dumpHeader(self, datasetName, fileName, conHandle, schema):
		self.createTable(conHandle, datasetName, schema)
		
	# dumps the body (entries)
	def dumpBody(self, datasetName, fileName, conHandle, schema, entries):
		for entry in entries:
			self.insertEntry(conHandle, datasetName, schema, entry)
	
	# creates the table
	def createTable(self, conn, datasetName, schema):
		tableName = self.tableName(datasetName)
		fieldsDecl = ", ".join(list(map(
			lambda fn: self.columnName(fn) + " " + self.sqlTypeOfField(schema, fn),
			schema.listFieldNames())))
		
		sql = "CREATE TABLE {0} (ordnum INT PRIMARY KEY, {1})".format(tableName, fieldsDecl)
		#print(sql)
		
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
	
	# inserts the entry into the table
	def insertEntry(self, conn, datasetName, schema, entry):
		
		tableName = self.tableName(datasetName)
		fieldsDecl = ", ".join(list(map(
			lambda fn: self.columnName(fn),
			schema.listFieldNames())))
		
		ordnum = entry.ordernum()
		valuesDecl = ", ".join(list(map(
			lambda fn: "?",
			schema.listFieldNames())))
		
		sql = "INSERT INTO {0} (ordnum, {1}) VALUES (?, {3})" \
				.format(tableName, fieldsDecl, ordnum, valuesDecl)
		#print(sql)
		
		values = [ordnum] + list(map(
			lambda fn: entry.value(fn),
			schema.listFieldNames()))
		
		c = conn.cursor()
		c.execute(sql, values)
		conn.commit()
		
	# creates name of the table
	def tableName(self, datasetName):
		return re.sub("[\W]", "_", datasetName)
	
	# creates name of column	
	def columnName(self, fieldName):
		return re.sub("[\W]", "_", fieldName)
		
	# obtains sql type of the field
	def sqlTypeOfField(self, schema, fieldName):
		fieldType = schema.typeOf(fieldName)
		
		if fieldType in ("int", "integer"):
			return "INT"
			
		if fieldType in ("decimal", "float"):
			return "REAL"
		
		if fieldType in ("bool", "boolean"):
			return "BOOL"
			
		return "TEXT"

########################################################################
########################################################################
# The handler which simply the existing files deletes.
class DeletingHandler(BaseExistingFileHandler):
	
	# handles the existing file
	def handle(self, datasetName, fileName):
		os.remove(fileName)

########################################################################
# The handler which simply moves the simple backup file.
class SimplyBackupingHandler(BaseExistingFileHandler):
	
	# handles the existing file
	def handle(self, datasetName, fileName):
		backupFileName = fileName + "_backup"
		os.rename(fileName, backupFileName)
	
########################################################################
if __name__== "__main__":
	print("Run dumpers_test.TestDumpers to test")

