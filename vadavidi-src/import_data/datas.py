# The datas module

from dataclasses import dataclass
from typing import List, Mapping, Any

########################################################################
# The schema of the table. The table heading, the list of the fields
# the list of the fields names with associated type specifier
@dataclass
class Schema:
	# the mapping fieldName -> typeName, or list of fields
	fields: Mapping[str, str]
	
	# returns the typeName of the given fieldName
	def typeOf(self, fieldName):
		return self.fields[fieldName]
	
	# lists all the typeNames
	def listFieldNames(self):
		return self.fields.keys()
	
	# just __str__
	def __str__(self):
		return "Schema(" + ", ".join(map(
			lambda fn: (fn + " of " + self.typeOf(fn)),
			self.listFieldNames())) + ")"
	

########################################################################
# The one row of the data table, the one data entry
@dataclass
class Entry:
	# the order number
	ordnum: int
	# maps field names to values
	values: Mapping[str, Any]

	# returns the value of the given fieldName
	def value(self, fieldName):
		return self.values[fieldName]
		
	# just the __str__
	def __str__(self):
		return "Entry " + str(self.ordnum) + ":" + str(self.values)
	
########################################################################
# The whole datatable, list of entries with schema
@dataclass
class Table:
	# maps field names to types
	schema: Schema
	# list of Entries
	entries: List[Entry]
	
	# just the __str__
	def __str__(self):
		return "Table" + "; ".join(list(map( \
			lambda entry: ("[" + ", ".join(list(map( \
				lambda fieldName: ("(" + fieldName + "=" + str(entry.value(fieldName)) + ")"), \
				self.schema.listFieldNames()))) + "]"), \
			self.entries)))
			
	# prints the table simply
	def printit(self):
		print("\t| ".join(map(
			lambda fieldName: (fieldName + ":" + self.schema.typeOf(fieldName)), \
			self.schema.listFieldNames())))
			
		for entry in self.entries:
			print("\t\t| ".join(map(
				lambda fieldName: str(entry.value(fieldName)), 
				self.schema.listFieldNames())))


########################################################################
if __name__== "__main__":
	print("Testing the datas module")
	schema = Schema({'foo': 'str', 'bar': 'int', 'baz': 'date', 'aux': 'enum'})
	print(schema)
	
	entry1 = Entry(1, {'foo': 'Karel', 'bar': 42, 'baz': 'TODO', 'aux': 'FIXED'})
	print(entry1)
	
	table = Table(schema, [entry1])
	print(table)
	table.printit()
