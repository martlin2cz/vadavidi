"""
The raiser is the opposite of the dumper. It picks the stored table and loads it
back to be used.
"""
from abc import ABC, abstractmethod
from common.datas_util import RowsMutableTable

################################################################################
class BaseRaiser(ABC):
    """ The (base) raiser. Loads table of the dataset. """
    
    # runs the raise
    @abstractmethod
    def run(self, dataset_name, schema):
        """ Runs the raise, returns the risen table """
        
        yield Exception("Implement me!");

################################################################################
class IteratingRaiser(BaseRaiser):
    """ The iterating raiser loads first some items, which are then converted
    to entries. """
    
    def run(self, dataset_name, schema):
        items = self.loadItems(dataset_name)
        return self.convertItems(dataset_name, schema, items)
    
    
    @abstractmethod
    def loadItems(self, dataset_name):
        """ Loads the items """
        
        yield Exception("Implement me!");    
    
    def convertItems(self, dataset_name, schema, items):
        """ Converts the items to entries """
        
        result = RowsMutableTable(schema)
        for item in items:
            entry = self.convert_item(dataset_name, schema, item)
            result.add(entry)
        
        return result.to_table()

    @abstractmethod
    def convertItem(self, dataset_name, schema, item):
        """ Converts the item to entry """
        
        yield Exception("Implement me!");

################################################################################
