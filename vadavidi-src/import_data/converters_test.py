# the test module for the converters

import unittest

from common.datas import Schema, Entry
from common.datas_util import  RowsMutableTable
from import_data.converters_impls import DefaultValuesConvertingConverter, \
	DefaultValueConverter, FormattedParserValueConverter, DatetimeValueConverter


########################################################################
# tests the converters
class TestConverters(unittest.TestCase):
	schema = Schema({"first": "string", "number": "integer", "second": "string"})
	
	def test_DefaultValuesConvertingConverter(self):
		table = self.create_table({"first": "hello", "number": "42", "second":"karel"})
		
		converter = DefaultValuesConvertingConverter()
		converter.converters_of_types = {}
		converter.converters_of_fields = {}
		
		self.run_converter(table, converter)
		
	def test_DefaultValueConverter(self):
		converter = DefaultValueConverter()
		self.print_running_converter(converter)
		
		self.run_value_converter("hello", "string", converter)
		self.run_value_converter("42", "integer", converter)
		self.run_value_converter("true", "boolean", converter)
		self.run_value_converter("12.5", "decimal", converter)

		self.run_value_converter("42.5", "integer", converter)
		self.run_value_converter("false", "boolean", converter)
		self.run_value_converter("33a1/3", "decimal", converter)

	def test_FormattedParserValueConverter(self):
		converter = FormattedParserValueConverter()
		converter.format = "{:d} buckets and {:d} boxes"
		converter.pick_which = 1
		self.print_running_converter(converter)
		
		self.run_value_converter("10 buckets and 11 boxes", "count with units", converter)
		self.run_value_converter("111 buckets and 10 boxes", "count with units", converter)
		self.run_value_converter("no buckets and any boxes", "count with units", converter)
		
	def test_DatetimeValueConverter(self):
		converter = DatetimeValueConverter()
		converter.format = "%d %b, %H:%M"
		self.print_running_converter(converter)
		
		self.run_value_converter("12 Feb, 11:42", "datetime", converter)
		self.run_value_converter("7 Dec, 10:59", "datetime", converter)
		self.run_value_converter("10 Feb, 9:10:11", "datetime", converter)
		self.run_value_converter("now", "datetime", converter)
		

	# creates table with one entry with given values
	def create_table(self, values):
		entry = Entry.create_new(self.schema, 0, "src-file", values)
		
		result = RowsMutableTable(self.schema)
		result += entry
		return result.to_table()
		
	# just prints that another converter gets run
	def print_running_converter(self, converter):
		print("=======================================================")
		print("Running converter " + str(converter))
		
	# runs the converting
	def run_converter(self, table, converter):
		print("=======================================================")
		print("Running converter " + str(converter))
		result = converter.convert(table)
		
		result.printit()
		
	# runs the converting
	def run_value_converter(self, raw_value, field_type, converter):
		#print("=======================================================")
		#print("Running converter " + str(converter))
		
		field_name = "testing"
		raw_entry = Entry({field_name: field_type})
		try:
			result = converter.convert_value(raw_entry, field_name, field_type, raw_value)
		except ValueError as ex:
			print("{0} \t-!-> FAILED {1}".format(raw_value, ex))
		else:
			print("{0} \t---> {1} ({2})".format(raw_value, result, type(result)))

########################################################################
if __name__ == '__main__':
	unittest.main()
