# the base queriers module
from abc import ABC

################################################################################
class BaseQuerier(ABC):
    
    def query(self, table, query):
        yield Exception("Implement Me!")
        
################################################################################
        