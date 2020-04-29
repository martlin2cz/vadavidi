"""
The datas util module. Apart from the datas module here are more advanced and
extra classes are specified.
"""

from typing import List, Mapping, Any

from common.datas import *
from builtins import staticmethod


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

	@staticmethod
	def column(table, field_name):
		""" Returns the list of values of given field over the whole table """
		
		return list(map(lambda e: e[field_name], table))
	
	@staticmethod
	def extract(entry, field_names):
		""" Extracts the specified fields from the entry, returns as map """
		
		return dict(map(lambda fn: (fn, entry[fn]), field_names))

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

	def add_field(self, field_name, field_type, value_computer=None):
		""" Adds given field with given initial value """
		
		self.schema = DatasUtil.add_to_schema(self.schema, field_name, field_type)
		
		self.entries = \
			list((self.add_to_entry(i, e, field_name, value_computer))
					for i,e in enumerate(self.entries))

	def add_field_with_values(self, field_name, field_type, values):
		""" Adds given field with given values """
		
		if len(values) != len(self.entries):
			raise ValueError("Lists length mismatch: " + str(len(values))
							 + " and " + str(len(self.entries)))
		
		value_computer = lambda ordernum, e: values[ordernum]
		
		return self.add_field(field_name, field_type, value_computer)
		
				
	def add_to_entry(self, ordernum, entry, field_name, value_computer):
		""" Replaces given entry with entry with the new field """
		
		if value_computer:
			value = value_computer(ordernum, entry)
		else:
			value = None
			
		values = { **entry.values, **{field_name: value} }
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
	cmt.add_field("name", "str", lambda o, e: e["foo"] * 10)
	cmt.add_field("gender", "enum", None)
	
	twc = cmt.to_table()
	twc.printit()
	print("=========")
	
	print(DatasUtil.column(twc, "foo"))
	