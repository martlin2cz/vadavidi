"""
The datas module. Contains the basic data structures.
"""

from dataclasses import dataclass
from typing import List, Mapping, Any

########################################################################

""" The ID field_name. Such field may contain order number or some other 
numeric unique identifier of the entry. """
ID = "vadavi_id"

""" The source field_name. Such field may contain information where the 
particular entry have been obtained from, typically the input file name. """
SOURCE = "vadavi_source"

########################################################################
@dataclass(frozen = True)
class Schema:
	""" The schema of the Table, list of fields. Immutable. """
	
	# The list of typed fields. Maps field_names to the types.
	fields: Mapping[str, str]
	
	def __init__(self, fields: Mapping[str, str]):
		object.__setattr__(self, "fields", \
						{**{ID: "integer", SOURCE: "string"}, **fields}) 

	def type_of(self, field_name):
		""" Returns the type of given field. """
			
		return self.fields[field_name]
	
	def list_field_names(self):
		""" Returns the list of all field's (their names). """
		
		return self.fields.keys()
		
	def list_raw(self):
		""" Returns the list of raw (without ID and SOURCE) field's (names) """ 
		
		return [f for f in self.list_field_names() if f not in [ID, SOURCE]]
	
	def __getitem__(self, key):
		return self.type_of(key)
	
	def __iter__(self):
		return self.list_field_names().__iter__()
	
	def __str__(self):
		return "Schema:(" + ", ".join(map(
			lambda fn: (fn + " of " + self[fn]),
			self)) + ")"
	

########################################################################
@dataclass(frozen = True)
class Entry:
	""" The entry, the one row of the Table. Contains list of fields values. 
	Immutable. """
	
	# Values, maps field_names to actual values
	values: Mapping[str, Any]

	def value(self, field_name):
		""" Returns the value of the given field """
		
		return self.values[field_name]
	
	def __getitem__(self, key):
		return self.value(key)
		
	# just the __str__
	def __str__(self):
		return "Entry:" + str(self.values)
	
	@staticmethod
	def create_new(schema, id, source, values):
		""" Creates (new) Entry with given id, source and values """
		
		values = { **{ID: id, SOURCE: source}, **values }
		return Entry.create(schema, values)
	
	
	@staticmethod
	def create(schema, values):
		""" Creates Entry with given values (already containing id and 
		source) """
		
		missing = schema.list_field_names() - values.keys()
		if missing == [ID, SOURCE]:
			raise ValueError("Missing ID and SOURCE.")
		
		if len(missing) > 0:
			raise ValueError("Missing following fields: " + ", ".join(missing))
		
		return Entry(values) 

	
########################################################################
@dataclass(frozen = True)
class Table:
	""" The whole datatable, a list of Entries. Imutable too. """
	
	# the schema (the fields specification)
	schema: Schema
	# list of Entries
	entries: List[Entry]
	
	def count(self):
		""" Returns the count of the entries """

		return len(self.entries)
	
	def list(self):
		""" Lists (all) the entries """
		
		return self.entries

	def __int__(self):
		return self.count()

	def __list__(self):
		return self.list()

	def __iter__(self):
		return self.list().__iter__()

	# just the __str__
	def __str__(self):
		return "Table:" + "; ".join(list(map(\
			lambda entry: ("[{0}]".format(", ".join(list(map(\
				lambda fieldName: ("({0}={1})".format(fieldName, str(entry[fieldName]))), \
				self.schema))))), \
			self.entries)))
			

	def printit(self):
		""" Simply prints the table to stdout """
		
		print("\t| ".join(map(\
				lambda fieldName: (fieldName + ":" + self.schema[fieldName]), \
				self.schema)))
			
		for entry in self.entries:
			print("\t\t| ".join(map(
					lambda fieldName: str(entry[fieldName]),
					self.schema)))


########################################################################
if __name__ == "__main__":
	print("Testing the datas module")
	schema = Schema({'foo': 'str', 'bar': 'int', 'baz': 'date', 'aux': 'enum'})
	print(schema)
	print((f + ";") for f in schema)
	
	entry1 = Entry({ID: 1, SOURCE: 'src', 'foo': 'Karel', 'bar': 42, 'baz': 'TODO', 'aux': 'FIXED'})
	print(entry1)
	
	entry2 = Entry.create_new(schema, 2, "unknown", {'foo': 'Jirka', 'bar': 99, 'baz': 'FILLME', 'aux': 'DYNAMIC'})
	print(entry2)
	
	try:
		Entry.create(schema, {'foo': 'Franta', 'baz': 'FIXME'})
	except ValueError as ex:
		print("Expected error: " + str(ex));
	
	table = Table(schema, [entry1, entry2])
	print(table)
	table.printit()
	
	print(str(int(table)) + "->" + str(list(table)))
	print((e + ";") for e in table)
