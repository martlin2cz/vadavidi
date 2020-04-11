# the loaders impls module

from abc import ABC, abstractmethod
import re
from typing import List, Mapping

from import_data.base_converters import BaseConverter
from import_data.base_loaders import BaseLoader
from import_data.base_parsers import BaseParser
from import_data.datas_util import DatasUtil


########################################################################
# The loader running on only one input file
class SingleFileLoader(BaseLoader):
	# the one single file we are working with
	file_name: str
	# the parser
	parser: BaseParser
	# the converter
	converter: BaseConverter
	
	def run(self, schema):			
		print("running parser");
		raw = self.parser.parse(schema, self.file_name)
		
		print("running analysis");
		converted = self.converter.convert(schema, raw)
		
		print("returning result");
		return converted

########################################################################
# The base file matcher.
class BaseFileMatcher(ABC):
	
	# matches the given file?
	@abstractmethod
	def matches(self, file_name):
		yield Exception("Implement me!");	

########################################################################
# Matcher matching by file name (path).
class FileNameMatcher(ABC):
	# the pattern of the file
	patternOfName: str
	
	# matches the given file?
	def matches(self, file_name):
		return bool(re.match(self.patternOfName, file_name))

########################################################################
# Matcher matching by first line pattern.
class FirstLineMatcher(ABC):
	# the pattern of the first line
	patternOfLine: str
	
	# matches the given file?
	def matches(self, file_name):
		line = self.readFirstLine(file_name)
		return bool(re.match(self.patternOfLine, line))
		
	# reads the first line of the file
	def readFirstLine(self, file_name):
		with open(file_name, "r") as f:
			return f.readline()

# TODO first-nth line matcher

########################################################################
# Matcher matching allways
class AllFilesMatchingMatcher(ABC):
	
	# matches the given file?
	def matches(self, file_name):
		return True
		
########################################################################
# Matcher never matching
class NoFileMatchingFileMatcher(BaseFileMatcher):
	
	# matches the given file?
	def matches(self, file_name):
		return False
		
# TODO xml schema / structure matcher
########################################################################
# Loader working with multiple files, 
# with various parsers and converters.
# Particular parser and converter gets obtained by its matcher.
class MultiFilesLoader(BaseLoader):
	# the list of files we are working with
	files_names: List[str]
	# the parsers
	parsers: Mapping[BaseFileMatcher, BaseParser]
	# the converters
	converters: Mapping[BaseFileMatcher, BaseConverter]
	
	# runs the load itself
	def run(self, schema):			
		table = DatasUtil.emptyTable(schema)
		for file_name in self.files_names:
			subtable = self.runForFile(schema, file_name)
			table = DatasUtil.joinTables(table, subtable)
		return table

	# runs the load from the given file
	def runForFile(self, schema, file_name):
		print("running parser");
		parser = self.pickParser(file_name)
		raw = parser.parse(schema, file_name)
		
		print("running analysis");
		converter = self.pickConverter(file_name)
		converted = converter.convert(schema, raw)
		#TODO add input file
		print("returning result");
		return converted

	# picks the parser for given file
	def pickParser(self, file_name):
		return self.pickByMatcher(self.parsers, file_name)
	
	# picks the converter for given file
	def pickConverter(self, file_name):
		return self.pickByMatcher(self.converters, file_name)

	# picks value from given dict based on the matcher in the key
	def pickByMatcher(self, dict_with, file_name):
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
