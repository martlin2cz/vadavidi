# The base loaders module

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

