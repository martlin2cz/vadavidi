"""
The implementations of the loaders.
"""

from abc import ABC, abstractmethod
import re
from typing import List, Mapping

from import_data.base_converters import BaseConverter
from import_data.base_loaders import BaseLoader
from import_data.base_parsers import BaseParser
from common.datas_util import DatasUtil


########################################################################
class SingleFileLoader(BaseLoader):
	""" The loader running on only one input file. """
	
	# the one single file we are working with
	file_name: str
	# the parser
	parser: BaseParser
	# the converter
	converter: BaseConverter
	
	def run(self, schema):			
		raw = self.parser.parse(schema, self.file_name)
		converted = self.converter.convert(raw)
		return converted

########################################################################
class BaseFileMatcher(ABC):
	""" The base file matcher. Class responsible for recognition of the files 
	based on some condition. """
	
	@abstractmethod
	def matches(self, file_name):
		""" Matches the given file? """
		
		yield Exception("Implement me!");	

########################################################################
class FileNameMatcher(ABC):
	""" Matcher matching by file name (path). """
	
	# the pattern of the file
	pattern_of_name: str
	
	def matches(self, file_name):
		return bool(re.match(self.pattern_of_name, file_name))

########################################################################
# 
class FirstLineMatcher(ABC):
	""" Matcher matching by first line pattern. """
	
	# the pattern of the first line
	pattern_of_line: str
	
	def matches(self, file_name):
		line = self.readFirstLine(file_name)
		return bool(re.match(self.pattern_of_line, line))
		
	def readFirstLine(self, file_name):
		""" Reads the first line of the file """
		with open(file_name, "r") as f:
			return f.readline()

# TODO cached first-line matcher
# TODO first-nth line matcher

########################################################################
class AllFilesMatchingMatcher(ABC):
	""" Matcher matching allways. """
	
	def matches(self, file_name):
		return True
		
########################################################################
class NoFileMatchingFileMatcher(BaseFileMatcher):
	""" Matcher never matching. """ 
	
	# matches the given file?
	def matches(self, file_name):
		return False
		
# TODO xml schema / structure matcher

########################################################################
class MultiFilesLoader(BaseLoader):
	"""
	Loader working with multiple files, with various parsers and converters.
	Particular parser and converter gets obtained by its matcher.
	"""
	
	# the list of files we are working with
	files_names: List[str]
	# the parsers
	parsers: Mapping[BaseFileMatcher, BaseParser]
	# the converters
	converters: Mapping[BaseFileMatcher, BaseConverter]
	
	def __init__(self, files_names: List[str], \
				parsers: Mapping[BaseFileMatcher, BaseParser], \
				converters: Mapping[BaseFileMatcher, BaseConverter]):
		#TODO 
		pass
	
	def run(self, schema):			
		table = DatasUtil.empty_table(schema)
		for file_name in self.files_names:
			subtable = self.run_for_file(schema, file_name)
			table = DatasUtil.join_tables(table, subtable)
		return table

	def run_for_file(self, schema, file_name):
		""" Runs the load from the given file """
		parser = self.pick_parser(file_name)
		raw = parser.parse(schema, file_name)
		
		converter = self.pick_converter(file_name)
		converted = converter.convert(raw)

		return converted

	def pick_parser(self, file_name):
		""" Picks the parser for given file """
		
		return self.pick_by_matcher(self.parsers, file_name)
	
	def pick_converter(self, file_name):
		""" Picks the converter for given file """

		return self.pick_by_matcher(self.converters, file_name)

	def pick_by_matcher(self, dict_with, file_name):
		""" Picks value from given dict based on the matcher in the key """
		
		matching = list(filter(
					lambda m: m.matches(file_name), 
					dict_with.keys()))
		
		if len(matching) < 1:
			print("No matcher found")
		
		if len(matching) > 1:
			print("More than 1 matchers found")
		
		matcher = matching[0]
		return dict_with.get(matcher)

########################################################################
if __name__== "__main__":
	print("see loaders_test module for the tests");
