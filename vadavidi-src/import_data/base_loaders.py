"""
The base loaders module. The loader is component responsible for loading the
table from the one or more files or any other sources.
"""

from abc import ABC, abstractmethod


########################################################################
class BaseLoader(ABC):
	""" The (base) loader. """
	
	@abstractmethod
	def run(self, schema):
		""" Runs the load itself """
		
		yield Exception("Implement me!");	

########################################################################

