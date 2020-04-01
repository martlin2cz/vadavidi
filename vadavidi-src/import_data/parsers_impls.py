# The base module for parsers

import csv

from datas import Schema, Entry, Table
from base_parsers import LinesSplittingParser, IteratingParser
from datas_util import MutableTable


########################################################################
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
########################################################################
# The (proper) CSV files parser. Allows to specify the format.
class CSVParser(IteratingParser):
	# the csv input format configuration
	delimiter = ','
	doublequote = 1
	escapechar = '\\'
	lineterminator = '\n'
	quotechar = '"'
	skipinitialspace = 1
	strict = 1
	
	# converts the input file to list of fractions
	def fracte(self, schema, file_name):
		with open(file_name, newline='') as csvfile:
			reader = csv.reader(csvfile, 
								delimiter = self.delimiter,
								doublequote = self.doublequote,
								escapechar = self.escapechar,
								lineterminator = self.lineterminator,
								quotechar = self.quotechar,
								skipinitialspace = self.skipinitialspace,
								strict = self.strict)
			return list(reader)
		
	# converts given fraction to entry
	def parseFraction(self, ordnum, fraction, schema):
		values = dict(list(map(
						lambda fn,val: (fn, val),
						schema.listFieldNames(), fraction)));		
		return Entry(ordnum, values)
	
########################################################################
########################################################################
# The Excel "CSV" files parser. Uses the default excel format.
class ExcelCSVParser(CSVParser):
	# the csv input format configuration
	delimiter = ','
	doublequote = 1
	escapechar = None
	lineterminator = '\r\n'
	quotechar = '"'
	skipinitialspace = 0
	strict = 0
		
########################################################################
########################################################################
if __name__== "__main__":
	schema = Schema({"first": "str", "number": "int", "second": "str"})
	
	print("Runining simple CSV parser")
	parser = SimpleCSVParser()
	input_file = "../testdata/first.csv"
	
	table = parser.parse(schema, input_file)
	print(table)
	table.printit()
	
	print("Runining CSV parser")
	parser = CSVParser()
	parser.delimiter = ';'
	input_file = "../testdata/second.csv"
	
	table = parser.parse(schema, input_file)
	print(table)
	table.printit()
	
	print("Runining Excel CSV parser")
	parser = ExcelCSVParser()
	input_file = "../testdata/third.csv"
	
	table = parser.parse(schema, input_file)
	print(table)
	table.printit()

