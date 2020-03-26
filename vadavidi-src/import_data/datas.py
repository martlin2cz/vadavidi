# The datas module

from dataclasses import dataclass
from typing import List, Mapping, Any

# The one row of the data table
@dataclass
class Entry:
	# maps field names to values
	atoms: Mapping[str, Any]

	def value(self, field):
		return self.atoms[field]
		
	def __str__(self):
		return "Entry" + str(self.atoms)
	
# The whole datatable
@dataclass
class Table:
	# maps field names to types
	schema: Mapping[str, str]
	# list of Entries
	entries: List[Entry]
	
	def __str__(self):
		return "Table" + "; ".join(list(map( \
			lambda entry: ("[" + ", ".join(list(map( \
				lambda field: ("(" + field + "=" + str(entry.value(field)) + ")"), \
				self.schema))) + "]"), \
			self.entries)))
			
	# prints the table simply
	def printit(self):
		print("\t".join(map(lambda field: (field + ":" + self.schema[field]), \
							self.schema.keys())))
		for entry in self.entries:
			print("\t\t".join(map(str, entry.atoms.values())))
