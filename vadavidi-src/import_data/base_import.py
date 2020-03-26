# The base importers module

from datas import Table, Entry
from abc import ABC, abstractmethod

# The general importer
class BaseImporter(ABC):
	# the file we are inputing from
	input_file = ""
	
	# runs the import itself
	def run(self, schema):
		print("running");
		raw = self.parse(schema)
		print("parsed");
		analysed = self.analyse(schema, raw)
		print("analyed");
		return analysed
	
	# parses the input to the raw tokens
	@abstractmethod
	def parse(self, schema):
		yield Exception("Implement me!");

	# extracts the atoms from the raw tokens
	@abstractmethod
	def analyse(self, schema, raw):
		yield Exception("Implement me!");

class CommonImporter(BaseImporter):
	
	def analyse(self, schema, raw):
		print("common")
		new_entries = []
		for entry in raw.entries:
			
			analysed = dict(map(lambda field: (field, self.analyse_val(field, schema[field], entry.value(field))), \
							entry.atoms))
							
			new_entry = Entry(analysed)
			new_entries.append(new_entry)
			
		return Table(schema, new_entries)

	def analyse_val(self, field_name, field_type, value):
		if field_type == "str":
			return value
			
		if field_type == "int":
			return int(value)
			
		return None
