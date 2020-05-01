"""
The various utilities module.
"""
from builtins import str
import re


################################################################################
class FilesNamer:
    """ The tool for creating the dataset file names. """
    
    # the file extension
    extension: str
    
    def __init__(self, extension):
        self.extension = extension
    
    def file_name(self, dataset_name):
        """ Creates the name of the dataset. """
        
        name = self.basename_of_file(dataset_name)
        extension = self.extension
        
        return name + "." + extension
    
    def basename_of_file(self, dataset_name):
        """ Creates the basename of the file. """
        return re.sub("[^\w/.]", "_", dataset_name)

################################################################################
if __name__ == '__main__':
    print("Testing the utils")
    namer = FilesNamer()
    namer.extension = "txt"
    
    print(namer.file_name("foo"))        
    print(namer.file_name("foo bar"))
    print(namer.file_name("foo/bar"))