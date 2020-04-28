"""
The implementations of the raisers.
"""

from common.simple_csv import SimpleCSV
from common.utils import FilesNamer
from outport_data.base_raisers import BaseRaiser
from common.sqlite_db import SQL_LITE_POOL


################################################################################
class SimpleCSVRaiser(BaseRaiser):
    """ The simple csv raiser. """
    
    # the simple csv implementation
    csv = SimpleCSV(True, True)
    # the namer of the file
    namer = FilesNamer("csv") 
    
    def run(self, dataset_name, schema):
        file_name = self.namer.file_name(dataset_name)
        return self.csv.load_table(schema, file_name)
    
################################################################################
class SQLLiteRaiser(BaseRaiser):
    """ The SQL Lite db file raiser. """
    
    def __init__(self):
        pass
    
    
    def run(self, dataset_name, schema):
        sqllite = SQL_LITE_POOL.get(dataset_name)
        return sqllite.load(schema)
    