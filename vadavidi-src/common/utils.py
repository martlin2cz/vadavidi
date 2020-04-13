# the various utilities module
from builtins import str
import re


################################################################################
# The tool for creating the file names
class FilesNamer:
    # the file extension
    extension: str
    
    # creates the name of the dataset
    def fileName(self, datasetName):
        name = self.basenameOfFile(datasetName)
        extension = self.extension
        
        return name + "." + extension
    
    # creates the basename of the file
    def basenameOfFile(self, datasetName):
        return re.sub("[^\w/.]", "_", datasetName)

################################################################################
if __name__ == '__main__':
    print("Testing the utils")
    namer = FilesNamer()
    namer.extension = "txt"
    
    print(namer.fileName("foo"))        
    print(namer.fileName("foo bar"))
    print(namer.fileName("foo/bar"))