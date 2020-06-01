""" The schemater producer. Generates the SchemaObjecterModel for given package 
and subclasses of some class. Optionally saves to file. """

from builtins import staticmethod
from functools import reduce
import importlib
from inspect import isabstract, signature
import inspect
import pkgutil
from typing import List, Dict, get_args, Any, _GenericAlias
import oyaml as yaml

from config.object_schemater_impl import SchematerModel, SchematerObjectModel, \
    IMPORTER_SCHEMATER_FILE
from config.value_obtainers_impls import SimpleValuePrompter,\
    ClassChoosePrompter, DictPrompter, ListPrompter
from abc import ABC, ABCMeta
from _collections import OrderedDict


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
        """ Lists the classes whose are definite and has given base_celass """
        
        return list(filter(
            lambda c: self.has_predcestor(c, base_class), classes))
        
    def has_predcestor(self, clazz, base_class):
        """ Returns true if given class is definite and has given base_class """
        
        if isabstract(clazz) or clazz is ABCMeta:
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
        fields_models = OrderedDict(map( \
                     lambda f: (f.name, self.model_of_field(f.annotation)), fields.values()))
        return SchematerObjectModel(base_class, fields_models)

    def list_fields(self, clazz):
        """ Lists the fields of the given class """

        sgn = signature(clazz.__init__)
        parameters = dict(sgn.parameters)
        return dict(filter(lambda p: p[0] is not "self", parameters.items()))
        
    def model_of_field(self, type_annot):
        """ Constructs the model (Obtainer) of the given field """
        
        print("~~ " + str(type_annot) + " ~ " + str(type(type_annot)))
        
        if type(type_annot) == ABCMeta or type_annot is ABC:
            return self.instance_choose_prompter(type_annot) 
        
        elif isinstance(type_annot, _GenericAlias) \
            and type_annot._name == "List": 
                #elif type_annot is List:
                return self.list_prompter(type_annot)
        
        elif isinstance(type_annot, _GenericAlias) \
            and type_annot._name == "Dict":
                #elif type_annot is Dict:
                return self.dict_prompter(type_annot)
        
        else:
            return self.value_prompter(type_annot)
        
        #prompt_text = "Gimme " + str(field) + "!"
        #prompt_type = "Any"
        #return SimpleValuePrompter(prompt_text, prompt_type)
    
    def instance_choose_prompter(self, type_annot):
        clazz = type_annot.__name__ 
        prompt_text = "Choose class implementing {0}".format(clazz)
        return ClassChoosePrompter(clazz, prompt_text)
    
    def list_prompter(self, type_annot):
        item_types = get_args(type_annot)
        item_type = item_types[0] if len(item_types) > 0 else Any
        
        item_prompter = self.model_of_field(item_type)
        prompt_text = "Specify list of {0}".format(item_type)
        return ListPrompter(prompt_text, item_prompter)
    
    def dict_prompter(self, type_annot):
        item_types = get_args(type_annot)
        key_type = item_types[0] if len(item_types) > 0 else Any
        value_type = item_types[1] if len(item_types) > 1 else Any
        
        key_prompter = self.model_of_field(key_type)
        value_prompter = self.model_of_field(value_type)
        prompt_text = "Specify dict of {0} and {1}".format(key_type, value_type)
        return DictPrompter(prompt_text, key_prompter, value_prompter)
        
    def value_prompter(self, type_annot):
        type = type_annot.__name__ 
        prompt_text = "Specify value of type {0}".format(type)
        return SimpleValuePrompter(prompt_text, type)
        
################################################################################

    @staticmethod
    def save(model, file_name):
        """ Saves the given model to given file """
        
        with open(file_name, "wt") as handle:
            yaml.dump(model, handle, Dumper=yaml.Dumper)
            
            
################################################################################
if __name__ == '__main__':
    print("Regenerating the importer schemater model file ...")

    producer = DefaultSchematerProducer()
    producer.lookup_package_names = ["import_data"]
    model = producer.generate_model("BaseParser")
    DefaultSchematerProducer.save(model, IMPORTER_SCHEMATER_FILE)
    
    print("Done!")
