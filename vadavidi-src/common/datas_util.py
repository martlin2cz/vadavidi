"""
The datas util module. Apart from the datas module here are more advanced and
extra classes are specified.
"""

from typing import List, Mapping, Any

from common.datas import *


########################################################################
class DatasUtil:
	"""
	The utilities for datas.
	"""
	
	@staticmethod
	def add_to_schema(schema, field_name, field_type):
		""" Creates new schema with given field appended to it. """
		
		fields = {**schema.fields, **{field_name: field_type}}
		return Schema(fields)
		

	@staticmethod
	def empty_table(schema):
		""" Creates empty table of given schema """
		
		return Table(schema, [])

	@staticmethod
	def join_tables(first, second):
		""" Creates empty table of given schema """
		
		schema = first.schema
		entries = (first.list()) + (second.list())
		
		return Table(schema, entries)

########################################################################
class RowsMutableTable:
	"""
	The rows mutable (allowing to add new rows) table. Someone may call it
	"Table builder".
	""" 
	
	# the schema of the table
	schema: Schema
	# list of Entries
	entries: List[Entry]
	
	def __init__(self, schema):
		self.schema = schema
		self.entries = []
	
	def add(self, entry):
		""" Adds (appends) given entry """
		
		self.entries.append(entry)
		return self
		
	def to_table(self):
		""" Converts to table """
		
		return Table(self.schema, self.entries)

	def __iadd__(self, entry):
		return self.add(entry)

	def __str__(self):
		return "RowsMutableTable:" + str(len(self.entries)) + "";

	
########################################################################
class ColsMutableTable:
	"""
	The columns mutable table (allowing to add new columns). It allows to extend
	the entries of the table by adding new fields to it.
	"""
	
	# the schema (gets updated)
	schema: Schema
	# list of Entries
	entries: List[Entry]

	def __init__(self, table):
		self.schema = table.schema
		self.entries = table.entries

	# TODO make the initial_value to be function entry -> value
	def add_field(self, field_name, field_type, initial_value=None):
		""" Adds given field with given initial value """
		
		self.schema = DatasUtil.add_to_schema(self.schema, field_name, field_type)
		
		self.entries = list(map(lambda e: self.add_to_entry(
				e, field_name, initial_value), self.entries))
				
	def add_to_entry(self, entry, field_name, initial_value):
		""" Replaces given entry with entry with the new field """
		
		values = { **entry.values, **{field_name: initial_value} }
		return Entry.create(self.schema, values)
	
	def to_table(self):
		""" Converts back to table """
		
		return Table(self.schema, self.entries)
	
	def __str__(self):
		return "ColsMutableTable:" + str(schema)
	
########################################################################
if __name__ == "__main__":
	print("Testing the datas_util module")
	schema = Schema({"foo": "int", "bar": "str", "baz": "date", "aux": "enum"})
	print(schema)
	
	rmt = RowsMutableTable(schema)
	rmt.add(Entry.create_new(schema, 0, "idk", {"foo": 42, "bar": "lorem", "baz": "today", "aux": "MAYBE"}))
	rmt.add(Entry.create_new(schema, 1, "maybe", {"foo": 43, "bar": "ipsum", "baz": "yesterday", "aux": "NO"}))
	twr = rmt.to_table()
	twr.printit()
	print("=========")

	cmt = ColsMutableTable(twr)
	cmt.add_field("name", "str", None)
	cmt.add_field("gender", "enum", "UNSPECIFIED")
	
	twc = cmt.to_table()
	twc.printit()