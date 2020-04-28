"""
The base module for dumpers. The dumper is responsible for dumping the table
to some "internal file" which allows simple, quick and efficient loading by 
Raiser. """

from abc import ABC, abstractmethod

import os.path as path
from common.utils import FilesNamer
from markups import abstract


########################################################################

class BaseDumper(ABC):
	""" The (base) dumper. """
	@abstractmethod
	def dump(self, dataset_name, table):
		""" Dumps the table, returns the file_name """
		
		yield Exception("Implement me!");

########################################################################
class BaseExistingFileHandler(ABC):
	""" Handler of already existing (dump) file. """
	
	@abstractmethod
	def handle(self, dataset_name, file_name):
		""" handles the existing file """
		
		yield Exception("Implement me!");

########################################################################
class FileDumper(BaseDumper):
	""" The file dumper. Dumps to file, the file gets completelly overriden,
		and specifies what to do with existing file. """
	
	# the namer
	namer: FilesNamer
	# the handler of the existing file
	existing_file_handler: BaseExistingFileHandler
	
	def __init__(self, file_extension):
		self.namer = FilesNamer(file_extension)


	def dump(self, dataset_name, table):
		file_name = self.namer.file_name(dataset_name)
		if path.exists(file_name):
			self.existing_file_handler.handle(dataset_name, file_name)
			
		self.dump_to_file(dataset_name, file_name, table)
		return file_name
	
	@abstractmethod
	def dump_to_file(self, dataset_name, file_name, table):
		""" Dumps table into the given file """
		
		yield Exception("Implement me!");

########################################################################
class CommonFileDumper(FileDumper):	
	""" Dumper dumping to file separatelly by heading and body. """
	
	def __init__(self, file_extension):
		super().__init__(file_extension)
	
	def dump_to_file(self, dataset_name, file_name, table):
		try:
			handle = self.open_the_file(dataset_name, file_name)
			
			schema = table.schema
			self.dump_header(dataset_name, file_name, handle, schema)
			
			entries = table.list()
			self.dump_body(dataset_name, file_name, handle, schema, entries)
		finally:
			self.close_the_file(dataset_name, file_name, handle)
	
	@abstractmethod	
	def open_the_file(self, dataset_name, file_name):
		""" Opens the file somehow, returns some handle to the file """
		
		yield Exception("Implement me!");
		
	@abstractmethod	
	def dump_header(self, dataset_name, file_name, handle, schema):
		""" Dumps the header (schema) orly prepares for the table """
		
		yield Exception("Implement me!");
	
	@abstractmethod	
	def dump_body(self, dataset_name, file_name, handle, schema, entries):
		""" Dumps the entries """
		
		yield Exception("Implement me!");
		
	@abstractmethod
	def close_the_file(self, dataset_name, file_name, handle):
		""" Closes the previously opened file """
		
		yield Exception("Implement me!");
		
########################################################################	
########################################################################
	
