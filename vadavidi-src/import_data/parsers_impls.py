# The base module for parsers

import csv
import re
from typing import Mapping
from lxml import etree

from import_data.base_parsers import LinesSplittingParser, IteratingParser
from import_data.datas import Entry


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
		
		return Entry.create(schema, ordnum, values)	

########################################################################
########################################################################
# The (proper) CSV files parser. Allows to specify the format.
class CSVParser(IteratingParser):
	# the csv input format configuration
	delimiter = ','
	doublequote = True
	escapechar = '\\'
	lineterminator = '\n'
	quotechar = '"'
	skipinitialspace = True
	strict = True
	
	# converts the input file to list of fractions
	def fracte(self, schema, file_name):
		with open(file_name, newline='') as csvfile:
			reader = csv.reader(csvfile, \
								delimiter = self.delimiter, \
								doublequote = self.doublequote, \
								escapechar = self.escapechar, \
								lineterminator = self.lineterminator, \
								quotechar = self.quotechar, \
								skipinitialspace = self.skipinitialspace, \
								strict = self.strict)
			return list(reader)
		
	# converts given fractionRecord to entry
	def parseFraction(self, ordnum, fractionRecord, schema):
		values = dict(list(map(
						lambda fn,val: (fn, val),
						schema.listFieldNames(), fractionRecord)));		
		return Entry.create(schema, ordnum, values)
		
	# converts given fraction ho user-readable string
	def stringifyFraction(self, fractionRecord):
		return self.delimiter.join(fractionRecord)
	
########################################################################
########################################################################
# The Excel "CSV" files parser. Uses the default excel format.
class ExcelCSVParser(CSVParser):
	# the csv input format configuration
	delimiter = ','
	doublequote = True
	escapechar = None
	lineterminator = '\r\n'
	quotechar = '"'
	skipinitialspace = False
	strict = False
		
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
		return Entry.create(schema, ordnum, values)

	# parses the given fieldName from given fractionElem
	def parsePart(self, fractionElem, fieldName):
		partPath = self.fieldsPaths.get(fieldName) 
		partXpath = etree.XPath(partPath) 
		partNodes = partXpath(fractionElem) 
		if len(partNodes) == 0:
			raise ValueError("No node with path '" + partPath + "' not found")
			
		part = partNodes[0]
		return (fieldName, part)
		
	# converts given fraction ho user-readable string
	def stringifyFraction(self, fractionElem):
		return etree.tostring(fractionElem, pretty_print = True)

	
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
		if len(matcher) == 0:
			raise ValueError("Line not matching the pattern")
		
		matches = matcher[0]
		if len(matches) < len(self.matchers.keys()):
			raise ValueError("Found only " + len(matches) + " match groups")
		
		values = dict(map(
				lambda fieldName: (fieldName, matches[self.matchers[fieldName]]), 
				schema.listFieldNames()))
		
		return Entry.create(schema, ordnum, values)	


########################################################################
########################################################################
if __name__== "__main__":
	print("Run parsers_text.TestParsers to test")
