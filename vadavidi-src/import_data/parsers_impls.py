# The base module for parsers

import csv
from lxml import etree
import re

from typing import Mapping
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
		
	# converts given fractionRecord to entry
	def parseFraction(self, ordnum, fractionRecord, schema):
		values = dict(list(map(
						lambda fn,val: (fn, val),
						schema.listFieldNames(), fractionRecord)));		
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
# The parser of XML files iterating over specified elements
class XMLElementParser(IteratingParser):
	# the xpaths for the values lookup
	# the xpath to list all the elements
	elemPath: str
	# the xpaths mapping to particular fieldNames
	fieldsPaths: Mapping[str, str]
	
	# converts the input file to list of fractions
	def fracte(self, schema, file_name):
		with open(file_name, newline='') as xmlfile:
			tree = etree.parse(xmlfile)
			elemXpath = etree.XPath(self.elemPath)
			return elemXpath(tree)

	# converts given fractionElem to entry
	def parseFraction(self, ordnum, fractionElem, schema):
		values = dict(list(map(lambda fn: self.parsePart(fractionElem, fn),
						schema.listFieldNames())));		
		return Entry(ordnum, values)

	# parses the given fieldName from given fractionElem
	def parsePart(self, fractionElem, fieldName):
		partPath = self.fieldsPaths.get(fieldName) 
		partXpath = etree.XPath(partPath) 
		partNodes = partXpath(fractionElem) 
		part = partNodes[0]
		return (fieldName, part) 
	
########################################################################
########################################################################
# The parser general files
class PatternBasedLinedParser(LinesSplittingParser):
	# the pattern of the line
	pattern: str
	# the mapping of the matches indexes to the fieldNames
	matchers: Mapping[str, int]
	# just the compiled pattern
	patternRe: None
	
	# runs the parsing itself
	def parse(self, schema, file_name):
		self.patternRe = re.compile(self.pattern)
		
		return super().parse(schema, file_name)
	
	# converts given line to entry
	def parseLine(self, ordnum, line, schema):
		matcher = self.patternRe.findall(line)
		matches = matcher[0]
		
		values = dict(map(
				lambda fieldName: (fieldName, matches[self.matchers[fieldName]]), 
				schema.listFieldNames()))
		
		return Entry(ordnum, values)	


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
	
	print("Runining XML parser 1")
	parser = XMLElementParser()
	parser.elemPath = "/records/record";
	parser.fieldsPaths = {"first": "@first", "number": "@number", "second": "@second"}
	input_file = "../testdata/fourth.xml"
	
	table = parser.parse(schema, input_file)
	print(table)
	table.printit()
	
	print("Runining XML parser 2")
	parser = XMLElementParser()
	parser.elemPath = "/records/record";
	parser.fieldsPaths = {"first": "first/text()", "number": "number/text()", "second": "second/text()"}
	input_file = "../testdata/fifth.xml"
	
	table = parser.parse(schema, input_file)
	print(table)
	table.printit()
	
	print("Runining Pattern based parser")
	parser = PatternBasedLinedParser()
	parser.pattern = "([^\:]+)\: ([\d]+) \(([^\)]+)\)";
	parser.matchers = {"first": 0, "number": 1, "second": 2}
	input_file = "../testdata/sixth.txt"

	table = parser.parse(schema, input_file)
	print(table)
	table.printit()

