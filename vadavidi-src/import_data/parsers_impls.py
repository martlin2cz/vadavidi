# The base module for parsers

from datas import Schema, Entry, Table
from base_parsers import LinesSplittingParser
from datas_util import MutableTable


########################################################################
# The simple CSV parser.
# Assumes values on lines separated with one simple separator,
# no quotes, no multilines, no escaped separators.
class SimpleCSVParser(LinesSplittingParser):
	# the fields separator
	separator = "\t"
	
	# converts given line to entry
	def parseLine(self, ordnum, line, schema):
		parts = line.split(self.separator)
		values = dict(map(lambda part,field: (field, part), parts, schema.listFieldNames()))
		
		return Entry(ordnum, values)	

########################################################################
if __name__== "__main__":
	print("Runining simple CSV parser")
	parser = SimpleCSVParser()
	input_file = "../testdata/first.csv"
	schema = Schema({"first": "str", "number": "int", "second": "str"})
	
	table = parser.parse(schema, input_file)
	print(table)
	table.printit()

