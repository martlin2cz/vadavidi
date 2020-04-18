"""
The base module for converters. Specifies the abstract converter, which maps 
converts table of raw string tokens to table of particular typed values 
(numbers, dates, etc.)
"""

from abc import ABC, abstractmethod
from typing import Mapping

from common.datas import Entry
from common.datas_util import RowsMutableTable


########################################################################
class BaseConverter(ABC):
	""" The converter. """
	
	@abstractmethod
	def convert(self, raw):
		""" Converts the given raw table to table with particularly typed 
		values
		"""
		
		yield Exception("Implement me!");

	def report_invalid(self, context_entry, field_name, raw_value, reason):
		""" Reports that the value of the entry could not be converted """
		
		ordnum = context_entry.ordernum()
		print("""Field {1}'s value '{2}' (of entry {0}) cannot be converted, 
			because: {3}""".format(ordnum, field_name, raw_value, reason))
		
		print("{0}".format(context_entry))
		print()

########################################################################
class EntriesConvertingConverter(BaseConverter):
	""" Converter using value converters. """

	def convert(self, raw):
		result = RowsMutableTable(raw.schema)
		
		for entry in raw.list():
			converted = self.convert_entry(raw.schema, entry)
			result += converted
		
		return result.to_table()	

	@abstractmethod
	def convert_entry(self, schema, raw_entry):
		""" Converts the entry """
		
		yield Exception("Implement me!");
	
########################################################################
########################################################################
class ValueConverter(ABC):
	""" The converter of one single value. """
	
	@abstractmethod
	def convert_value(self, raw_entry, field_name, field_type, raw_value):
		""" Converts value of field in given context entry """
		
		yield Exception("Implement me!");

########################################################################
class ValuesConvertingConverter(EntriesConvertingConverter):
	""" Converter using value converters. """

	def convert_entry(self, schema, raw_entry):
		values = dict(map(
			lambda fn: (fn, self.convert_value(schema, raw_entry, fn)),
			schema))
		
		return Entry.create(schema, values)

	def convert_value(self, schema, raw_entry, field_name):
		""" Converts the value of the given entry's field """
		
		field_type = schema[field_name]
		converter = self.pick_the_value_converter(schema, field_name, field_type)
			
		raw_value = raw_entry.value(field_name)
		try:
			return converter.convert_value(raw_entry, field_name, field_type, raw_value)
		except Exception as ex:
			self.reportInvalid(raw_entry, field_name, raw_value, str(ex))

	# finds the particular converter
	@abstractmethod
	def pick_the_value_converter(self, schema, field_name, field_type):
		""" For given field picks the particular value converter """
		
		yield Exception("Implement me!");

########################################################################
