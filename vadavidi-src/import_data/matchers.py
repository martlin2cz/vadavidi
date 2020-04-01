# The file matchers module

from abc import ABC, abstractmethod

########################################################################
# The abstract file matcher
class BaseFileMatcher(ABC):
	# checks whether the file matches
	@abstractmethod
	def matches(self, file_name):
		print("matching file");
		yield Exception("Implement me!");

########################################################################
# Matcher matched allways
class AlwaysMatchingFileMatcher(BaseFileMatcher):
	def matches(self, file_name):
		return true

########################################################################
# Matcher never matching
class NeverMatchingFileMatcher(BaseFileMatcher):
	def matches(self, file_name):
		return false

########################################################################
# The matcher checking for match of file name pattern
class FileNameMatchingFileMatcher(BaseFileMatcher):
	# file name pattern
	pattern: str
	
	def matches(self, file_name):
		return file_name.matches(self.pattern)

########################################################################
# The matcher checking for the first (or second) line pattern
class LineMatchingFileMatcher(BaseFileMatcher):
	# first line pattern
	first_line_pattern: str
	
	# second line pattern
	first_line_pattern: str
	
	def matches(self, file_name):
		(first_line, second_line) = readTwoFirstLines(file_name)
		
		if self.first_line_pattern:
			return first_line.matches(self.first_line_pattern)
			
		if self.second_line_pattern:
			return second_line.matches(self.second_line_pattern)
		
		yield Error("At least first or second line_pattern has to be specified")

	# reads the first two lines of the given file
	def readTwoFirstLines(self, file_name):
		#TODO
		print("readTwoFirstLines")

########################################################################
# The XML schema matcher
class XMLSchemaMatchingFileMatcher(BaseFileMatcher):

	def matches(self, file_name):
		TODO
		print("matching XML file");
		yield Exception("Implement me!");
