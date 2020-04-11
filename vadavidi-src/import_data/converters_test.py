# the test module for the converters

import unittest

from import_data.converters_impls import DefaultValuesConvertingConverter, \
	DefaultValueConverter, FormattedParserValueConverter, DatetimeValueConverter
from import_data.datas import Schema, Entry
from import_data.datas_util import MutableTable


########################################################################
# tests the converters
class TestConverters(unittest.TestCase):
	schema = Schema({"first": "string", "number": "integer", "second": "string"})
	
	def test_DefaultValuesConvertingConverter(self):
		table = self.createTable({"first": "hello", "number": "42", "second":"karel"})
		
		converter = DefaultValuesConvertingConverter()
		converter.convertersOfTypes = {}
		converter.convertersOfFields = {}
		
		self.runConverter(table, converter)
		
	def test_DefaultValueConverter(self):
		converter = DefaultValueConverter()
		self.printRunningConverter(converter)
		
		self.runValueConverter("hello", "string", converter)
		self.runValueConverter("42", "integer", converter)
		self.runValueConverter("true", "boolean", converter)
		self.runValueConverter("12.5", "decimal", converter)

		self.runValueConverter("42.5", "integer", converter)
		self.runValueConverter("false", "boolean", converter)
		self.runValueConverter("33a1/3", "decimal", converter)

	def test_FormattedParserValueConverter(self):
		converter = FormattedParserValueConverter()
		converter.formatOf = "{:d} buckets and {:d} boxes"
		converter.pickWhich = 1
		self.printRunningConverter(converter)
		
		self.runValueConverter("10 buckets and 11 boxes", "count with units", converter)
		self.runValueConverter("111 buckets and 10 boxes", "count with units", converter)
		self.runValueConverter("no buckets and any boxes", "count with units", converter)
		
	def test_DatetimeValueConverter(self):
		converter = DatetimeValueConverter()
		converter.formatOf = "%d %b, %H:%M"
		self.printRunningConverter(converter)
		
		self.runValueConverter("12 Feb, 11:42", "datetime", converter)
		self.runValueConverter("7 Dec, 10:59", "datetime", converter)
		self.runValueConverter("10 Feb, 9:10:11", "datetime", converter)
		self.runValueConverter("now", "datetime", converter)
		

	# creates table with one entry with given values
	def createTable(self, values):
		entry = Entry.create(self.schema, 0, values)
		
		result = MutableTable(self.schema)
		result.add(entry)
		return result.toTable()
		
	# just prints that another converter gets run
	def printRunningConverter(self, converter):
		print("=======================================================")
		print("Running converter " + str(converter))
		
	# runs the converting
	def runConverter(self, table, converter):
		print("=======================================================")
		print("Running converter " + str(converter))
		result = converter.convert(self.schema, table)
		
		result.printit()
		
	# runs the converting
	def runValueConverter(self, rawValue, fieldType, converter):
		#print("=======================================================")
		#print("Running converter " + str(converter))
		
		fieldName = "testing"
		rawEntry = Entry(0, {fieldName: fieldType})
		try:
			result = converter.convertValue(rawEntry, fieldName, fieldType, rawValue)
		except Exception as ex:
			print("{0} \t-!-> FAILED {1}".format(rawValue, ex))
		else:
			print("{0} \t---> {1} ({2})".format(rawValue, result, type(result)))

########################################################################
if __name__ == '__main__':
    unittest.main()
