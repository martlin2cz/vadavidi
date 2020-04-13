# The base module for the raisers
from abc import ABC, abstractmethod, abstractclassmethod
from common.datas_util import MutableTable

################################################################################
class BaseRaiser(ABC):
    
    # runs the raise
    @abstractmethod
    def run(self, datasetName, schema):
        yield Exception("Implement me!");

################################################################################
class IteratingRaiser(BaseRaiser):
    
    # runs the raise
    def run(self, datasetName, schema):
        items = self.loadItems(datasetName)
        return self.convertItems(datasetName, schema, items)
    
    
    # loads the items
    @abstractmethod
    def loadItems(self, datasetName):
        yield Exception("Implement me!");    
    
    # converts the items to entries
    def convertItems(self, datasetName, schema, items):
        result = MutableTable(schema)
        for (ordnum, item) in enumerate(items):
            entry = self.convertItem(datasetName, schema, ordnum, item)
            result.add(entry)
        
        return result.toTable()

    # converts the item to entry
    @abstractmethod
    def convertItem(self, datasetName, schema, ordnum, item):
        yield Exception("Implement me!");

################################################################################
