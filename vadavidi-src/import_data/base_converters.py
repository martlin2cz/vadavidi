# The base module for converters

from datas import Table, Entry
from datas_util import MutableTable
from abc import ABC, abstractmethod
from typing import Mapping



########################################################################
# The (base) converter.
class BaseConverter(ABC):

	# runs the conversion itself	
	@abstractmethod
	def convert(self, schema, raw):
		print("converting");
		yield Exception("Implement me!");

	# reports that the value of the entry could not be converted
	def reportInvalid(self, contextEntry, fieldName, rawValue, reason):
		ordnum = contextEntry.ordernum()
		print("Field {1}'s value '{2}' (of entry {0}) cannot be converted, because: {3}".format(ordnum, fieldName, rawValue, reason))
		print("{0}".format(contextEntry))
		print()

########################################################################
# Converter using value converters
class EntriesConvertingConverter(BaseConverter):
	
	# runs the conversion itself
	def convert(self, schema, raw):
		result = MutableTable(schema)
		
		for entry in raw.list():
			converted = self.convertEntry(schema, entry)
			result.add(converted)
		
		return result.toTable()	

	# converts the given entry
	@abstractmethod
	def convertEntry(schema, rawEntry):
		yield Exception("Implement me!");
	
########################################################################
########################################################################
# The converter of one single value
class ValueConverter(ABC):
	
	# converts value of field in given context entry
	@abstractmethod
	def convertValue(self, rawEntry, fieldName, fieldType, rawValue):
		yield Exception("Implement me!");

########################################################################
# Converter using value converters
class ValuesConvertingConverter(EntriesConvertingConverter):
	
	# converts the given entry
	def convertEntry(self, schema, rawEntry):
		values = dict(map(
			lambda fn: (fn, self.convertValue(schema, rawEntry, fn)),
			schema.listFieldNames()))
		
		ordnum = rawEntry.ordernum()
		return Entry.create(schema, ordnum, values)

	# converts the value of the given entry's field
	def convertValue(self, schema, rawEntry, fieldName):
		fieldType = schema.typeOf(fieldName)
		converter = self.pickTheValueConverter(schema, fieldName, fieldType)
			
		rawValue = rawEntry.value(fieldName)
		try:
			return converter.convertValue(rawEntry, fieldName, fieldType, rawValue)
		except Exception as ex:
			self.reportInvalid(rawEntry, fieldName, rawValue, str(ex))

	# finds the particular converter
	@abstractmethod
	def pickTheValueConverter(self, schema, fieldName, fieldType):
		yield Exception("Implement me!");

########################################################################
