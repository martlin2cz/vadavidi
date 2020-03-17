# The base importers module
import datas
from abc import ABC, abstractmethod

# The general importer
class BaseImporter(ABC):
	# the file we are inputing from
	input_file = ""
	
	# runs the import itself
	@abstractmethod
	def run(self, schema):
		yield Exception("Implement me")
	
