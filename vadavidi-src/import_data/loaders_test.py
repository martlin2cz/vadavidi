# the test module for the loaders

import unittest

from import_data.converters_impls import DefaultValuesConvertingConverter
from import_data.datas import Schema
from import_data.loaders_impls import FileNameMatcher, FirstLineMatcher, \
	SingleFileLoader, MultiFilesLoader, AllFilesMatchingMatcher
from import_data.parsers_impls import SimpleCSVParser, XMLElementParser


########################################################################
# tests the parsers
class TestLoaders(unittest.TestCase):
	schema = Schema({"first": "str", "number": "int", "second": "str"})
	
	def test_FileNameMatcher(self):
		matcher = FileNameMatcher()
		matcher.patternOfName = "(.+)\.csv"
		self.runMatcher(matcher, "testdata/firts.csv")
		self.runMatcher(matcher, "testdata/fourth.xml")
	
		matcher = FileNameMatcher()
		matcher.patternOfName = "fi((rst)|(fth)).(.+)"
		self.runMatcher(matcher, "testdata/first.csv")
		self.runMatcher(matcher, "testdata/second.csv")
	
	def test_FirstLineMatcher(self):
		matcher = FirstLineMatcher()
		matcher.patternOfLine = "([^\t]+)\t([^\t]+)\t([^\t]+)"
		self.runMatcher(matcher, "testdata/first.csv")
		self.runMatcher(matcher, "testdata/second.csv")
	
		matcher = FirstLineMatcher()
		matcher.patternOfLine = "\<\?xml"
		self.runMatcher(matcher, "testdata/first.csv")
		self.runMatcher(matcher, "testdata/fourth.xml")
	
	def test_SingleFilesLoader(self):
		loader = SingleFileLoader()
		loader.file_name = "testdata/first.csv"
		loader.parser = SimpleCSVParser()
		loader.converter = DefaultValuesConvertingConverter()
		
		self.runLoader(loader)
	
	def test_MultiFilesLoader(self):
		loader = MultiFilesLoader()
		loader.files_names = ["testdata/first.csv", "testdata/fourth.xml"]
		
		csvParser = SimpleCSVParser()
		
		xmlParser = XMLElementParser()
		xmlParser.elemPath = "/records/record";
		xmlParser.fieldsPaths = {"first": "@first", "number": "@number", "second": "@second"}
		
		converter = DefaultValuesConvertingConverter()
		
		csvMatcher = FileNameMatcher()
		csvMatcher.patternOfName = "(.+)\.csv"
		
		xmlMatcher = FileNameMatcher()
		xmlMatcher.patternOfName = "(.+)\.xml"
		
		allMatcher = AllFilesMatchingMatcher()
		loader.parsers = { csvMatcher: csvParser, xmlMatcher: xmlParser }
		loader.converters = { allMatcher: converter }
		
		self.runLoader(loader)
		
		
	def runMatcher(self, matcher, file_name):
		print("=======================================================")
		print("RUNNING MATCHER: " + str(matcher));
		
		match = matcher.matches(file_name)
		print("{0} \t -> {1}".format(file_name, match))
		
	def runLoader(self, loader):
		print("=======================================================")
		print("RUNNING LOADER: " + str(loader));
		
		table = loader.run(self.schema)
		
		table.printit()
	
	
	########################################################################
if __name__ == '__main__':
    unittest.main()
