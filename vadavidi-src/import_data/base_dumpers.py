# The base module for parsers

from abc import ABC, abstractmethod

import os.path as path
from common.utils import FilesNamer


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
	# the namer
	namer = FilesNamer()
	# the handler of the existing file
	existingFileHandler: BaseExistingFileHandler

	# dumps the table, returns the filename
	def dump(self, datasetName, table):
		fileName = self.namer.fileName(datasetName)
		if path.exists(fileName):
			self.existingFileHandler.handle(datasetName, fileName)
			
		self.dumpToFile(datasetName, fileName, table)
		return fileName
	
	# dumps table into the given file
	@abstractmethod
	def dumpToFile(self, datasetName, fileName, table):
		yield Exception("Implement me!");


########################################################################
# Dumper dumping to file separatelly by heading and body
class CommonFileDumper(FileDumper):	
	
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
	
