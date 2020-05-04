""" The default implementation of the schemater. Loads from the file. """
from builtins import staticmethod
from dataclasses import dataclass
import os
from typing import Mapping
from yaml import CLoader as Loader, load

from config.base_objecter import BaseObjectSchemater, BaseValueObtainer


################################################################################
################################################################################
@dataclass
class SchematerObjectModel:
    """ The schemater model of the object. """
    
    # base class of this object model
    base: str
    
    # the fields obtainers
    fields: Mapping[str, BaseValueObtainer]

################################################################################
@dataclass
class SchematerModel:
    # the mapping of class name to object mode
    objects: Mapping[str, SchematerObjectModel]
    
################################################################################
class DefaultObjectSchemater(BaseObjectSchemater):
    """ The default schemater. """
    
    model: SchematerModel
    
    def list_impls(self, clazz):
        return list(dict(filter(
                lambda no: clazz == no[1].base,
                self.model.objects.items()
            )).keys())
        
    def list_fields(self, clazz):
        return self.model.objects[clazz].fields


    @staticmethod
    def load(file_name):
        with open(file_name, "rt") as handle:
            model = load(handle, Loader=Loader)
            
            schemater = DefaultObjectSchemater()
            schemater.model = model
            
            return schemater
        
    def __str__(self):
        return "Schemater: " + str(self.model)
            
################################################################################
################################################################################
# The file with importer schemater model
IMPORTER_SCHEMATER_FILE = \
    os.path.dirname(os.path.abspath(__file__)) + "/importer.yaml"
    
################################################################################
if __name__ == '__main__':
    print("See objecter_test to test")

    