# the module for the impls of the converters

from datetime import datetime
from typing import Mapping

from parse import  *

from import_data.base_converters import ValueConverter, \
	ValuesConvertingConverter


########################################################################
# 
class DefaultValueConverter(ValueConverter):
	""" The default value converter. Supports only str/string, 
	int/integer, float/decimal and bool/boolean types. """
	
	def convert_value(self, raw_entry, field_name, field_type, raw_value):
		if field_type in ("str", "string"):
			return raw_value
			
		if field_type in ("int", "integer"):
			return int(raw_value)
			
		if field_type in ("float", "decimal"):
			return float(raw_value)	
		
		if field_type in ("bool", "boolean"):
			return raw_value == "true"
				
		raise ValueError("Unsupported field '{0}' of type '{1}' with value '{2}'" \
				.format(field_name, field_type, raw_value))
		
########################################################################
class FormattedParserValueConverter(ValueConverter):
	""" Converter by using python parser. """
	
	# the format of the value
	format: str 
	# which value to pick
	pick_which: int = 0
	
	def convert_value(self, raw_entry, field_name, field_type, raw_value):
		result = parse(self.format, raw_value)
		if result == None:
			raise ValueError("No such match")
			
		return result[self.pick_which]

########################################################################
class DatetimeValueConverter(ValueConverter):
	""" Converter of date and/or time with cusomt format. """
	# the format of the date/time value
	format: str 
	
	# converts value of field in given context entry
	def convert_value(self, raw_entry, field_name, field_type, raw_value):
		return datetime.strptime(raw_value, self.format)

########################################################################
class DefaultValuesConvertingConverter(ValuesConvertingConverter):
	""" Converter using value converters based on field name or type. """
	
	# the converters of field types
	converters_of_types: Mapping[str, ValueConverter] = {}
	# the converters if field names
	converters_of_fields: Mapping[str, ValueConverter] = {}
	# the default, fail-throught converter
	default_converter: ValueConverter = DefaultValueConverter()
	
	# finds the particular converter
	def pick_the_value_converter(self, schema, field_name, field_type):
		if field_type in self.converters_of_types.keys():
			return self.converters_of_types[field_type]
			
		if field_type in self.converters_of_types.keys():
			return self.converters_of_types[field_type]
			
		return self.default_converter


########################################################################	
if __name__== "__main__":
	print("See the converters_test module");
