# the test module for the parsers

import unittest

from common.datas import Schema
from import_data.parsers_impls import SimpleCSVParser, CSVParser, ExcelCSVParser, \
	XMLElementParser, PatternBasedLinedParser


########################################################################
# tests the parsers
class TestParsers(unittest.TestCase):
	schema = Schema({"first": "str", "number": "int", "second": "str"})
	
	def test_SimpleCSVParser(self):
		parser = SimpleCSVParser()
		
		self.run_parser(parser, "testdata/first.csv")
		self.run_parser(parser, "testdata/first-missing.csv")

	def test_CSVParser(self):
		parser = CSVParser()
		parser.delimiter = ';'
		
		self.run_parser(parser, "testdata/second.csv")
		self.run_parser(parser, "testdata/second-missing.csv")
		
	def test_ExcelCSVParser(self):
		parser = ExcelCSVParser()
		
		self.run_parser(parser, "testdata/third.csv")
		self.run_parser(parser, "testdata/third-missing.csv")
	
	def test_XMLElementParser_attributes(self):
		parser = XMLElementParser()
		parser.elemPath = "/records/record";
		parser.fieldsPaths = {"first": "@first", "number": "@number", "second": "@second"}
		
		self.run_parser(parser, "testdata/fourth.xml")
		self.run_parser(parser, "testdata/fourth-missing.xml")
				
	def test_XMLElementParser_childNodes(self):
		parser = XMLElementParser()
		parser.elemPath = "/records/record";
		parser.fieldsPaths = {"first": "first/text()", "number": "number/text()", "second": "second/text()"}
		
		self.run_parser(parser, "testdata/fifth.xml")
		self.run_parser(parser, "testdata/fifth-missing.xml")

	def test_PatternBasedLinedParser(self):
		parser = PatternBasedLinedParser()
		parser.pattern = "([^\:]+)\: ([\d]+) \(([^\)]+)\)";
		parser.matchers = {"first": 0, "number": 1, "second": 2}
		
		self.run_parser(parser, "testdata/sixth.txt")
		self.run_parser(parser, "testdata/sixth-missing.txt")


	# runs the parsing
	def run_parser(self, parser, input_file):
		print("=======================================================")
		print("RUNNING PARSER: " + str(parser));
		table = parser.parse(self.schema, input_file)
		
		#print(table)
		table.printit()
		
		print();

########################################################################
if __name__ == '__main__':
	unittest.main()
