# the datas_util module

from typing import List, Mapping, Any
from datas import *

########################################################################
# The utilities class for the datas module
class DatasUtil:
	
	# Creates the schema of given schema, but for the raw table
	@staticmethod
	def schemaOfRaw(schema):
		newFields = dict(map(
					lambda fn: (fn, "str"),
					schema.listFieldNames()))
					
		return  Schema(newFields)
	
	# Creates empty table of given schema
	@staticmethod
	def emptyTable(schema):
		return Table(schema, [])

	# Creates empty table of given schema
	@staticmethod
	def joinTables(first, second):
		schema = first.schema
		entries = (first.list()) + (second.list())
		
		return Table(schema, entries)


	# adds the given field to given schema
	@staticmethod
	def addToSchema(schema, fieldName, fieldType):
		print("addToSchema")
		pass #TODO mutable or unmutable?


########################################################################
# The "mutable" variant of the table. 
# Someone may call it "Table builder".
class MutableTable:
	# maps field names to types
	schema: Schema
	# list of Entries
	entries: List[Entry]
	
	def __init__(self, schema):
		self.schema = schema
		self.entries = []
	
	def add(self, entry):
		self.entries.append(entry)
		
	def toTable(self):
		return Table(self.schema, self.entries)

	def __str__(self):
		return "MutableTable " + str(len(self.entries)) + "";
########################################################################
if __name__== "__main__":
	print("Testing the datas_util module")
	schema = Schema({"foo": "int", "bar": "str", "baz": "date", "aux": "enum"})
	print(schema)
	ofRaw = DatasUtil.schemaOfRaw(schema)
	print(ofRaw)
	emptyTable = DatasUtil.emptyTable(schema)
	print(emptyTable)
	
	mt = MutableTable(schema)
	mt.add(Entry(0, {"foo": 42, "bar": "lorem", "baz": "today", "aux": "MAYBE"}))
	mt.add(Entry(1, {"foo": 43, "bar": "ipsum", "baz": "yesterday", "aux": "NO"}))
	mtt = mt.toTable()
	mtt.printit()
