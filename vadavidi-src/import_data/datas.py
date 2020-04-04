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
		return "Schema:(" + ", ".join(map(
			lambda fn: (fn + " of " + self.typeOf(fn)),
			self.listFieldNames())) + ")"
	

########################################################################
# The one row of the data table, the one data entry
@dataclass
class Entry:
	# the order number
	ordnum: int
	# maps fieldNames to values
	values: Mapping[str, Any]

	# returns the value of the given fieldName
	def value(self, fieldName):
		return self.values[fieldName]
	
	# returns the order number of this entry
	def ordernum(self):
		return self.ordnum;
		
	# just the __str__
	def __str__(self):
		return "Entry:" + str(self.ordnum) + ":" + str(self.values)
	
	# validates the values agains the schema (only field names) 
	# and constructs entry
	@staticmethod
	def create(schema, ordnum, values):
		missing = schema.listFieldNames() - values.keys()
		if len(missing) > 0:
			raise ValueError("Missing following fields: " + ", ".join(missing))
		
		return Entry(ordnum, values) 
	
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
		return "Table:" + "; ".join(list(map( \
			lambda entry: ("{0} [{1}]".format(entry.ordernum(), ", ".join(list(map( \
				lambda fieldName: ("({0}={1})".format(fieldName, str(entry.value(fieldName)))), \
				self.schema.listFieldNames()))))), \
			self.entries)))
			
	# prints the table simply
	def printit(self):
		print("NO \t| " \
			+ "\t| ".join(map( \
				lambda fieldName: (fieldName + ":" + self.schema.typeOf(fieldName)), \
				self.schema.listFieldNames())))
			
		for entry in self.entries:
			print(str(entry.ordernum()) + "\t| " \
				+ "\t\t| ".join(map(
					lambda fieldName: str(entry.value(fieldName)), 
					self.schema.listFieldNames())))


########################################################################
if __name__== "__main__":
	print("Testing the datas module")
	schema = Schema({'foo': 'str', 'bar': 'int', 'baz': 'date', 'aux': 'enum'})
	print(schema)
	
	entry1 = Entry(1, {'foo': 'Karel', 'bar': 42, 'baz': 'TODO', 'aux': 'FIXED'})
	print(entry1)
	
	entry1 = Entry.create(schema, 2, {'foo': 'Jirka', 'bar': 99, 'baz': 'FILLME', 'aux': 'DYNAMIC'})
	print(entry1)
	
	try:
		Entry.create(schema, 2, {'foo': 'Franta',  'baz': 'FIXME'})
	except Exception as ex:
		print("Expected error: " + str(ex));
	
	table = Table(schema, [entry1])
	print(table)
	table.printit()
