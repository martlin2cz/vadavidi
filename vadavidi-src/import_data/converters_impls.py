# the module for the impls of the converters

from ast import parse
from datetime import datetime


from import_data.base_converters import ValueConverter, \
	ValuesConvertingConverter


########################################################################
# The default value converter. Supports only "str" and "int" types
class DefaultValueConverter(ValueConverter):

	# converts value of field in given context entry
	def convertValue(self, rawEntry, fieldName, fieldType, rawValue):
		if fieldType in ("str", "string"):
			return rawValue
			
		if fieldType in ("int", "integer"):
			return int(rawValue)
			
		if fieldType in ("float", "decimal"):
			return float(rawValue)	
		
		if fieldType in ("bool", "boolean"):
			return rawValue == "true"
				
		raise ValueError("Unsupported field '{0}' of type '{1}' with value '{2}'" \
				.format(fieldName, fieldType, rawValue))
		
########################################################################
# Converter by using python parser
class FormattedParserValueConverter(ValueConverter):
	# the format of the value
	formatOf: str 
	# which value to pick
	pickWhich: int = 0
	
	# converts value of field in given context entry
	def convertValue(self, rawEntry, fieldName, fieldType, rawValue):
		result = parse(self.formatOf, rawValue)
		if result == None:
			raise ValueError("No such match")
			
		return result[self.pickWhich]

########################################################################
# Converter of date and/or time with cusomt format
class DatetimeValueConverter(ValueConverter):
	# the format of the date/time value
	formatOf: str 
	
	# converts value of field in given context entry
	def convertValue(self, rawEntry, fieldName, fieldType, rawValue):
		return datetime.strptime(rawValue, self.formatOf)


########################################################################
# Converter using value converters based on field name or type
class DefaultValuesConvertingConverter(ValuesConvertingConverter):
	# the converters of field types
	convertersOfTypes: Mapping[str, ValueConverter] = {}
	# the converters if field names
	convertersOfFields: Mapping[str, ValueConverter] = {}
	# the default, fail-throught converter
	defaultConverter: ValueConverter = DefaultValueConverter()
	
	# finds the particular converter
	def pickTheValueConverter(self, schema, fieldName, fieldType):
		if fieldType in self.convertersOfTypes.keys():
			return self.convertersOfTypes[fieldType]
			
		if fieldType in self.convertersOfTypes.keys():
			return self.convertersOfTypes[fieldType]
			
		return self.defaultConverter


########################################################################	
if __name__== "__main__":
	print("See the converters_test module");
