# The base module for parsers

from datas import Schema, Entry, Table
from abc import ABC, abstractmethod
from datas_util import MutableTable

########################################################################
# The (base) parser.
class BaseParser(ABC):
	
	# runs the parsing itself
	@abstractmethod
	def parse(self, schema, file_name):
		yield Exception("Implement me!");

########################################################################
# The iterating parser
class IteratingParser(BaseParser):
	
	# runs the parsing itself
	def parse(self, schema, file_name):
		fractions = self.fracte(schema, file_name)
		table = MutableTable(schema)
		for ordnum, fraction in enumerate(fractions):
			entry = self.parseFraction(ordnum, fraction, schema)
			table.add(entry)

		return table.toTable()

	# converts the input file to list of fractions
	@abstractmethod
	def fracte(self, schema, file_name):
		yield Exception("Implement me!");
		
	# converts given fraction to entry
	@abstractmethod
	def parseFraction(self, ordnum, fraction, schema):
		yield Exception("Implement me!");

########################################################################
# The iterating parser
class LinesSplittingParser(IteratingParser):
	
	# converts the input file to list of fractions
	def fracte(self, schema, file_name):
		return self.loadLines(file_name);
		
	# converts given fraction to entry
	def parseFraction(self, ordnum, fraction, schema):
		return self.parseLine(ordnum, fraction, schema);
		
	# loads the lines as a array
	def loadLines(self, file_name):
		with open(file_name, "r") as f:
			lines = f.readlines()
			clean = list(map(lambda line: line.replace('\n', ''), lines)) 
			return clean
		
	# converts given line to entry
	@abstractmethod
	def parseLine(self, ordnum, line, schema):
		yield Exception("Implement me!");

########################################################################
