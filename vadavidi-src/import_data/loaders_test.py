"""
The test module for the loaders
"""
import unittest

from common.datas import Schema
from common.test_utils import TestUtils
from import_data.converters_impls import DefaultValuesConvertingConverter
from import_data.loaders_impls import FileNameMatcher, FirstLineMatcher, \
	SingleFileLoader, MultiFilesLoader, AllFilesMatchingMatcher
from import_data.parsers_impls import SimpleCSVParser, XMLElementParser


########################################################################
class TestLoaders(unittest.TestCase):
	schema = Schema({"first": "str", "number": "int", "second": "str"})
	
	def test_FileNameMatcher(self):
		matcher = FileNameMatcher()
		matcher.pattern_of_name = "(.+)\.csv"
		self.run_matcher(matcher, TestUtils.tfn("firts.csv"))
		self.run_matcher(matcher, TestUtils.tfn("fourth.xml"))
	
		matcher = FileNameMatcher()
		matcher.pattern_of_name = "fi((rst)|(fth)).(.+)"
		self.run_matcher(matcher, TestUtils.tfn("first.csv"))
		self.run_matcher(matcher, TestUtils.tfn("second.csv"))
	
	def test_FirstLineMatcher(self):
		matcher = FirstLineMatcher()
		matcher.pattern_of_line = "([^\t]+)\t([^\t]+)\t([^\t]+)"
		self.run_matcher(matcher, TestUtils.tfn("first.csv"))
		self.run_matcher(matcher, TestUtils.tfn("second.csv"))
	
		matcher = FirstLineMatcher()
		matcher.pattern_of_line = "\<\?xml"
		self.run_matcher(matcher, TestUtils.tfn("first.csv"))
		self.run_matcher(matcher, TestUtils.tfn("fourth.xml"))
	
	def test_SingleFilesLoader(self):
		loader = SingleFileLoader()
		loader.file_name = TestUtils.tfn("first.csv")
		loader.parser = SimpleCSVParser()
		loader.converter = DefaultValuesConvertingConverter()
		
		self.run_loader(loader)
	
	def test_MultiFilesLoader(self):
		loader = MultiFilesLoader()
		loader.files_names = [TestUtils.tfn("first.csv"), TestUtils.tfn("fourth.xml")]
		
		csv_parser = SimpleCSVParser()
		
		xml_parser = XMLElementParser()
		xml_parser.elem_path = "/records/record";
		xml_parser.fields_paths = {"first": "@first", "number": "@number", "second": "@second"}
		
		converter = DefaultValuesConvertingConverter()
		
		csv_matcher = FileNameMatcher()
		csv_matcher.pattern_of_name = "(.+)\.csv"
		
		xml_matcher = FileNameMatcher()
		xml_matcher.pattern_of_name = "(.+)\.xml"
		
		all_matcher = AllFilesMatchingMatcher()
		loader.parsers = { csv_matcher: csv_parser, xml_matcher: xml_parser }
		loader.converters = { all_matcher: converter }
		
		self.run_loader(loader)
		
	########################################################################

	def run_matcher(self, matcher, file_name):
		print("=======================================================")
		print("RUNNING MATCHER: " + str(matcher));
		
		match = matcher.matches(file_name)
		print("{0} \t -> {1}".format(file_name, match))
		
	def run_loader(self, loader):
		print("=======================================================")
		print("RUNNING LOADER: " + str(loader));
		
		table = loader.run(self.schema)
		
		table.printit()
	
	
	########################################################################
if __name__ == '__main__':
    unittest.main()
