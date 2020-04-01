# the module for the impls of the converters

from datas import Schema, Entry, Table
from base_converters import ValuesConverter

########################################################################
# The default converter. Supports only "str" and "int" types
class DefaultConverter(ValuesConverter):

	def convertValue(self, fieldName, value):
		if field_type == "str":
			return value
			
		if field_type == "int":
			return int(value)
			
		return None
		
########################################################################
if __name__== "__main__":
	print("Runining Default converter");
	# TODO
