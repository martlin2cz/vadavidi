"""
The implementations of the raisers.
"""

from common.simple_csv import SimpleCSV
from common.utils import FilesNamer
from outport_data.base_raisers import BaseRaiser


################################################################################
class SimpleCSVRaiser(BaseRaiser):
    """ The simple csv raiser. """
    
    # the simple csv implementation
    csv = SimpleCSV(True, True)
    # the namer of the file
    namer = FilesNamer() 
    
    def __init__(self):
        self.namer.extension = "csv"
    
    def run(self, dataset_name, schema):
        file_name = self.namer.file_name(dataset_name)
        return self.csv.load_table(schema, file_name)
    
################################################################################
