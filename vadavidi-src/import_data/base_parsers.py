"""
The base module for parsers. The parser is responsible of parsing one single 
file to the table with raw values (string tokens).

"""

from abc import ABC, abstractmethod

from common.datas_util import RowsMutableTable


########################################################################
class BaseParser(ABC):
	""" The (base) parser. """
	
	@abstractmethod
	def parse(self, schema, file_name):
		""" Parses the given file """
		
		yield Exception("Implement me!");
		
	def report_invalid(self, ordnum, context, reason):
		""" Reports that the entry could not be parsed """
		
		print("Entry {0} cannot be parsed, because: {1}".format(ordnum, reason))
		print("{0}".format(context))
		print()


########################################################################
class IteratingParser(BaseParser):
	""" The iterating parser. Works in two stages, first lists some "fractions"
	(lines, elements), which are then 1:1 parsed to entries.
	""" 
	
	def parse(self, schema, file_name):
		fractions = self.fracte(schema, file_name)
		table = RowsMutableTable(schema)
		
		for ordnum, fraction in enumerate(fractions):
			try:
				entry = self.parse_fraction(ordnum, file_name, fraction, schema)
			except Exception as ex:
				context = self.stringify_fraction(fraction)
				self.report_invalid(ordnum, context, str(ex))
			else:
				table.add(entry)

		return table.to_table()

	@abstractmethod
	def fracte(self, schema, file_name):
		""" Converts the input file to list of fractions """
		
		yield Exception("Implement me!");
		
	@abstractmethod
	def parse_fraction(self, ordnum, file_name, fraction, schema):
		""" Converts given fraction to entry """
		
		yield Exception("Implement me!");
	
	@abstractmethod	
	def stringify_fraction(self, fraction):
		""" Converts given fraction to user-readable string """
		
		yield Exception("Implement me!");


########################################################################
class LinesSplittingParser(IteratingParser):
	""" The lines splitting parser. The fraction here is one line. """
	
	# converts the input file to list of fractions
	def fracte(self, schema, file_name):
		return self.load_lines(file_name);
		
	# converts given fraction to entry
	def parse_fraction(self, ordnum, file_name, fraction, schema):
		return self.parse_line(ordnum, file_name, fraction, schema);
		
	# loads the lines as a array
	def load_lines(self, file_name):
		with open(file_name, "r") as f:
			lines = f.readlines()
			clean = list(map(lambda line: line.replace('\n', ''), lines)) 
			return clean
		
	@abstractmethod
	def parse_line(self, ordnum, file_name, line, schema):
		""" Converts given line to entry """
		
		yield Exception("Implement me!");

	def stringify_fraction(self, line):
		return line
		
########################################################################
