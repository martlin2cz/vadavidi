# The base loaders module

from abc import ABC, abstractmethod


########################################################################
# The common loader loader
class BaseLoader(ABC):
	
	# runs the import itself
	@abstractmethod
	def run(self, schema):
		yield Exception("Implement me!");	

########################################################################

