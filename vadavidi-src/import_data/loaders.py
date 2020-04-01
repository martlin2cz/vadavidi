# The loaders module

from datas import Schema, Entry, Table
from base_parsers import BaseParser
from base_converters import BaseConverter

from abc import ABC, abstractmethod

########################################################################
# The common loader loader
class BaseLoader(ABC):
	
	# runs the import itself
	@abstractmethod
	def run(self, schema):
		yield Exception("Implement me!");	

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
		raw = self.parser.parse(schema, file_name)
		
		print("running analysis");
		converted = self.converter.convert(schema, raw)
		
		print("returning result");
		return converted

########################################################################
# Loader working with multiple files, 
# with various parsers and converters.
# Particular parser and converter gets obtained by its matcher.
class MultiFilesLoader(BaseLoader):
	# the list of files we are working with
	files_names: List[str]
	# the parsers
	parsers: Map[BaseFileMatcher, BaseParser]
	# the converters
	converters: Map[BaseFileMatcher, BaseConverter]
	
	# runs the load itself
	def run(self, schema):			
		table = DatasUtil.emptyTable(schema)
		for file_name in self.files_names:
			subtable = self.runForFile(file_name)
		return table

	# runs the load from the given file
	def runForFile(self, file_name):
		print("running parser");
		parser = self.pickParser(file_name)
		raw = parser.parse(schema, file_name)
		
		print("running analysis");
		converter = self.pickConverter(file_name)
		converted = converter.convert(schema, raw)
		
		print("returning result");
		return converted

	# picks the parser for given file
	def pickParser(self, file_name):
		return self.pickByMatcher(parsers, file_name)
	
	# picks the converter for given file
	def pickConverter(self, file_name):
		return self.pickByMatcher(converters, file_name)

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
		return dict_with.value(matcher)

########################################################################
if __name__== "__main__":
	print("Testing the loaders");
	# TODO

