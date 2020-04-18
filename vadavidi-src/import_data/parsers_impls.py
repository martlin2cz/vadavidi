"""
The module implementing the parsers.
"""

import csv
import re
from typing import Mapping

from lxml import etree

from common.datas import Entry
from common.simple_csv import SimpleCSV
from import_data.base_parsers import LinesSplittingParser, IteratingParser,\
	BaseParser
from common.datas_util import DatasUtil


########################################################################
########################################################################
class SimpleCSVParser(BaseParser):
	"""
	The simple CSV parser.
	Assumes values on lines separated with one simple separator, no quotes, 
	no multilines, no escaped separators. Terminates on any failure.
	"""
	
	# the csv module impl
	csv = SimpleCSV(False, False)

	def parse(self, schema, file_name):
		try:
			return self.csv.load_table(schema, file_name)
		except Exception as ex:
			self.report_invalid(-1, "Some", str(ex))
			return DatasUtil.empty_table(schema)

########################################################################
########################################################################
class CSVParser(IteratingParser):
	""" The (proper) CSV files parser. Allows to specify the format. """
	# the csv input format configuration
	delimiter = ','
	doublequote = True
	escapechar = '\\'
	lineterminator = '\n'
	quotechar = '"'
	skipinitialspace = True
	strict = True
	
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
		
	def parse_fraction(self, ordnum, file_name, fraction_record, schema):
		if len(schema.list_raw()) > len(fraction_record):
			raise ValueError("Expected {0} fields, but record has only {1}" \
						.format(len(schema.list_raw()), len(fraction_record)))
			
		values = dict(list(map(
						lambda fn,val: (fn, val),
						schema.list_raw(), fraction_record)));		
		return Entry.create_new(schema, ordnum, file_name, values)
		
	def stringify_fraction(self, fraction_record):
		return self.delimiter.join(fraction_record)
	
########################################################################
########################################################################
class ExcelCSVParser(CSVParser):
	""" The Excel "CSV" files parser. Uses the default excel format. """
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
class XMLElementParser(IteratingParser):
	""" The parser of XML files iterating over specified elements. """
	
	# the xpaths for the values lookup
	# the xpath to list all the elements
	elem_path: str
	# the xpaths mapping to particular fieldNames
	fields_paths: Mapping[str, str]
	
	def fracte(self, schema, file_name):
		with open(file_name, newline='') as xmlfile:
			tree = etree.parse(xmlfile)
			elem_xpath = etree.XPath(self.elem_path)
			return elem_xpath(tree)

	def parse_fraction(self, ordnum, file_name, fraction_elem, schema):
		values = dict(list(map(lambda fn: self.parsePart(fraction_elem, fn),
						schema.list_raw())));		
		return Entry.create_new(schema, ordnum, file_name, values)

	def parsePart(self, fraction_elem, field_name):
		part_path = self.fields_paths.get(field_name) 
		part_xpath = etree.XPath(part_path) 
		part_nodes = part_xpath(fraction_elem) 
		if len(part_nodes) == 0:
			raise ValueError("No node with path '" + part_path + "' found")
			
		part = part_nodes[0]
		return (field_name, part)
		
	def stringify_fraction(self, fraction_elem):
		return etree.tostring(fraction_elem, pretty_print = True)

	
########################################################################
########################################################################
class PatternBasedLinedParser(LinesSplittingParser):
	""" The parser general (lined) files. How the line may be parsed is 
	specified by the pattern and mapping of matches to fields. """
	
	# the pattern of the line
	pattern: str
	# the mapping of the matches indexes to the field_names
	matchers: Mapping[str, int]
	# just the compiled pattern
	_pattern_re: None
	
	# runs the parsing itself
	def parse(self, schema, file_name):
		self._pattern_re = re.compile(self.pattern)
		
		return super().parse(schema, file_name)
	
	# converts given line to entry
	def parse_line(self, ordnum, file_name, line, schema):
		matcher = self._pattern_re.findall(line)
		if len(matcher) == 0:
			raise ValueError("Line " + ordnum + " not matching the pattern")
		
		matches = matcher[0]
		if len(matches) < len(self.matchers.keys()):
			raise ValueError("Found only " + len(matches) + " match groups")
		
		values = dict(map(
				lambda fn: (fn, matches[self.matchers[fn]]), 
				schema.list_raw()))
		
		return Entry.create_new(schema, ordnum, file_name, values)	


########################################################################
########################################################################
if __name__== "__main__":
	print("Run parsers_text.TestParsers to test")
