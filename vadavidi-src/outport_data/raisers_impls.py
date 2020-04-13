# the raisers impls package
from outport_data.base_raisers import IteratingRaiser
from common.simple_csv import SimpleCSV
from common.utils import FilesNamer

################################################################################
class SimpleCSVRaiser(IteratingRaiser):
    # the simple csv implementation
    csv = SimpleCSV()
    # the namer of the file
    namer = FilesNamer() 
    
    def __init__(self):
        self.namer.extension = "csv"
    
    # loads the items
    def loadItems(self, datasetName):
        fileName = self.namer.fileName(datasetName)
        return self.csv.listLines(fileName) 

    # converts the item to entry
    def convertItem(self, datasetName, schema, ordnum, itemLine):
        return self.csv.lineToEntry(ordnum, schema, itemLine)
    
################################################################################
