"""
The base queriers module. The querier executes the query on the specific table.
"""
from abc import ABC, abstractmethod
from builtins import str, staticmethod
from dataclasses import dataclass
from typing import Mapping, Callable, List

from common.datas import Table
from outport_data.base_query import Query


################################################################################
class BaseQuerier(ABC):
    """ The (base) querier. """
    
    def query(self, dataset_name:str, table:Table, query:Query):
        """ Runs the query on the table """
        
        yield Exception("Implement Me!")
        
    @staticmethod    
    def create_grouppers_names(groups_map):
        return list(filter(lambda gn: (groups_map[gn] is None), \
                           groups_map.keys()))
        

################################################################################
