""" The schemater producer. Generates the SchemaObjecterModel for given package 
and subclasses of some class. Optionally saves to file. """

from builtins import staticmethod
from functools import reduce
import importlib
from inspect import isabstract
import inspect
import pkgutil
from typing import List
from yaml import dump
from yaml.dumper import Dumper

from config.object_schemater_impl import SchematerModel, SchematerObjectModel, \
    IMPORTER_SCHEMATER_FILE
from config.value_obtainers_impls import SimpleValuePrompter


################################################################################
################################################################################
class DefaultSchematerProducer:
    """ An utility class which generates the schemater, and possibly saves it 
    then to file. """
    
    # the packages where to look for
    lookup_package_names: List[str]
    
 #   def __init__(self, lookup_package_names: List[str]):
 #       self.lookup_package_names = lookup_package_names

    def load_package(self, pn):
        """ Loads the given package """
        
        return __import__(pn)

    def list_packages(self):
        """ Lists all the packages in lookup_package_names """
        
        return list(map(lambda pn: self.load_package(pn), \
                        self.lookup_package_names))
    
    def load_package_modules(self, package):
        """ Loads the modules in the given package """
        
        return map(lambda mi: importlib.import_module(mi.name), \
                   pkgutil.walk_packages(\
                        path=package.__path__,
                        prefix=package.__name__ + '.'))
    
    def list_modules(self):
        """ Lists all the modules in lookup_package_names """
        
        return list(reduce(lambda x, y: x + y,
            map(lambda pkg: self.load_package_modules(pkg), \
                self.list_packages())))
    
    def load_module_classes(self, module):
        """ Lists all the classes in the given module """
        
        module_members = inspect.getmembers(module, inspect.isclass)
        return list(dict(module_members).values())
    
    def list_classes(self):
        """ Lists all classes in the lookup_package_names """
        
        return list(reduce(lambda x, y: x + y,
           map(lambda m: self.load_module_classes(m), \
               self.list_modules())))

################################################################################

    def generate_model(self, base_class):
        """ The main method. Genereates the model for the given base class """
        
        classes = self.list_classes()
        clases_with_base = self.with_base(classes, base_class)
        objects = self.to_objects_model(clases_with_base, base_class)
        
        return SchematerModel(objects)

    def with_base(self, classes, base_class):
        """ Lists the classes whose are definite and has given base_class """
        
        return list(filter(
            lambda c: self.has_predcestor(c, base_class), classes))
        
    def has_predcestor(self, clazz, base_class):
        """ Returns true if given class is definite and has given base_class """
        
        if isabstract(clazz):
            return False
        
        for base in clazz.mro():
            if base.__name__ is base_class:
                return True
            
        return False
    
    def to_objects_model(self, classes, base_class):
        """ Converts given classes to name -> ObjectModels dict """
        
        return dict(map(
            lambda c: (c.__name__, self.class_to_model(c, base_class)),
            classes))
    
    def class_to_model(self, clazz, base_class):
        """ Converts the given class to ObjectModel """
        
        fields = self.list_fields(clazz)
        fields_models = dict(map(lambda f: (f, self.model_of_field(f)), fields))
        return SchematerObjectModel(base_class, fields_models)

    def list_fields(self, clazz):
        """ Lists the fields of the given class """

        # TODO lists all
        return list(filter(lambda e: not e.startswith("_"), \
                           vars(clazz)))
        
    def model_of_field(self, field):
        """ Constructs the model (Obtainer) of the given field """
        
        # TODO ignores type
        prompt_text = "Gimme " + str(field) + "!"
        prompt_type = "Any"
        return SimpleValuePrompter(prompt_text, prompt_type)
    
################################################################################

    @staticmethod
    def save(model, file_name):
        """ Saves the given model to given file """
        
        with open(file_name, "wt") as handle:
            dump(model, handle, Dumper=Dumper)
            
            
################################################################################
if __name__ == '__main__':
    print("Regenerating the importer schemater model file ...")

    producer = DefaultSchematerProducer()
    producer.lookup_package_names = ["import_data"]
    model = producer.generate_model("BaseParser")
    DefaultSchematerProducer.save(model, IMPORTER_SCHEMATER_FILE)
