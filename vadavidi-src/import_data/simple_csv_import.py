# The CSV simple importer module

from base_import import BaseImporter
from datas import Table, Entry

# The simple line-breaking and lines-splitting importer
class SimpleCSVImporter(BaseImporter):
	# the fields separator
	separator = "\t"
	
	def run(self, schema):
		lines = self.load_lines()
		#print(lines)
		
		entries = list(map(lambda line: self.line2entry(schema, line), lines))
		
		#print(entries);
		return Table(schema, entries)
	
	# loads the lines as a array (from self.input_file)
	def load_lines(self):
		with open(self.input_file, "r") as f:
			lines = f.readlines()
			clean = list(map(lambda line: line.replace('\n', ''), lines)) 
			return clean

	# converts the line to the entry
	def line2entry(self, schema, line):
		parts = line.split(self.separator)
		atoms = dict(map(lambda part,field: (field, part), parts, schema.keys()))
		
		return Entry(atoms)	

########################################################################
if __name__== "__main__":
	print("Runining simple CSV import");
	importer = SimpleCSVImporter()
	importer.input_file = "../testdata/first.csv"
	schema = {"first": "str", "number": "num", "second": "str"}
	
	table = importer.run(schema)
	print(table)
	table.printit()
