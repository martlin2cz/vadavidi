# The base module for parsers

from abc import ABC, abstractmethod
import re

import os.path as path


########################################################################
# The (base) dumper.
class BaseDumper(ABC):
	
	# dumps the table, returns the filename
	@abstractmethod
	def dump(self, datasetName, table):
		yield Exception("Implement me!");

########################################################################
# Handler of already existing file.
class BaseExistingFileHandler(ABC):
	
	# handles the existing file
	@abstractmethod
	def handle(self, datasetName, fileName):
		yield Exception("Implement me!");

########################################################################
# The file dumper. Dumps to file, the file gets completelly overriden,
# and specifies what to do with existing file.
class FileDumper(BaseDumper):
	# the handler of the existing file
	existingFileHandler: BaseExistingFileHandler

	# dumps the table, returns the filename
	def dump(self, datasetName, table):
		fileName = self.prepareFileName(datasetName)
		if path.exists(fileName):
			self.existingFileHandler.handle(datasetName, fileName)
			
		self.dumpToFile(datasetName, fileName, table)
		return fileName
	
	# prepares the file and returns its name
	@abstractmethod
	def prepareFileName(self, datasetName):
		yield Exception("Implement me!");
		

	# dumps table into the given file
	@abstractmethod
	def dumpToFile(self, datasetName, fileName, table):
		yield Exception("Implement me!");

########################################################################
# Dumper dumping to file with name based on datasetName and extension
class NamedFileDumper(FileDumper):
	# the extension of the dump file
	fileExtension: str
	
	# creates the name of the file
	def prepareFileName(self, datasetName):
		name = self.basenameOfFile(datasetName)
		extension = self.fileExtension
		
		return name + "." + extension
		
	# creates the basename of the file
	def basenameOfFile(self, datasetName):
		return re.sub("[^\w/.]", "_", datasetName)

########################################################################
# Dumper dumping to file separatelly by heading and body
class CommonFileDumper(NamedFileDumper):	
	
	# dumps table into the given file
	def dumpToFile(self, datasetName, fileName, table):		
		with self.openTheFile(datasetName, fileName) as handle:
			
			schema = table.schema
			self.dumpHeader(datasetName, fileName, handle, schema)
			
			entries = table.list()
			self.dumpBody(datasetName, fileName, handle, schema, entries)
	
	# opens the file, returns the handle
	@abstractmethod	
	def openTheFile(self, datasetName, fileName):
		yield Exception("Implement me!");
		
	# dumps some header (the schema, i guess)
	@abstractmethod	
	def dumpHeader(self, datasetName, fileName, handle, schema):
		yield Exception("Implement me!");
	
	# dumps the body (entries)
	@abstractmethod	
	def dumpBody(self, datasetName, fileName, handle, schema, entries):
		yield Exception("Implement me!");

########################################################################	
########################################################################
	
