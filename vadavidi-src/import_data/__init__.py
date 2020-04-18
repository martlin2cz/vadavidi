"""
 The data import package.
 
 Implements the import of the data from one or more files to some "internal"
 storage, which supports efficient manipulation.
 
 The structure:
 Importer:
 	- Loader
		- Parser
		- Converter 
 	- Dumper

 The input (text) file contains fractions (lines, elements) 
 which contains parts (actual string values)
 to be then converted to actual values in the table.

"""
