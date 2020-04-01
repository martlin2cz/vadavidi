# The base module for converters

from datas import Table, Entry
from abc import ABC, abstractmethod


########################################################################
# The (base) converter.
class BaseConverter(ABC):

	# runs the conversion itself	
	@abstractmethod
	def convert(schema, raw):
		print("converting");
		yield Exception("Implement me!");

########################################################################
# The default converter.
class ValuesConverter(BaseConverter):

	def convert(schema, raw):
		
		TODO:
		for row, col in raw:
			fieldName = ...
			value = ...
			converted = self.convertValue(fieldName, value)
			add converted somewhere
		
		return converted_table_whatever	
		
	@abstractmethod
	def convertValue(self, fieldName, value):
		print("converting value");
		yield Exception("Implement me!");

########################################################################
