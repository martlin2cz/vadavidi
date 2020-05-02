"""
The module responsible for the manipulating with the objects.
"""
################################################################################
from collections import deque
from dataclasses import dataclass
from typing import Mapping, Any, Deque


@dataclass
class AutomatedObjectEntry:
    """ The entry of the built object. Contains class name and map of fields 
    and their values. """
    
    clazz: str
    fields: Mapping[str, Any]
    
    def __init__(self, clazz):
        self.clazz = clazz
        self.fields = {}
    
    def add(self, field_name, field_value):
        """ Adds the given field with given value. """ 
        self.fields[field_name] = field_value

################################################################################
class AutomatedObjectBuilder:
    """ An builder of the objects. """
    
    object: AutomatedObjectEntry
    stack: Deque[AutomatedObjectEntry] = {}
    
    def __init__(self, clazz):
        self.object = AutomatedObjectEntry(clazz)
        self.stack = deque([self.object])
    
    def _current_object(self):
        """ Returns the currently built entry """
        
        return self.stack[-1]
    
    
    def _new_current(self, new_entry):
        """ Marks the given object to be build currently """
        
        return self.stack.append(new_entry)
    
    def _rollback_current(self):
        """ Returns to previous current object """
        
        return self.stack.pop()
    
################################################################################
    
    def set(self, field_name, field_value):
        """ Sets the value of the field of the current object """
        
        self._current_object().add(field_name, field_value)
    
    def set_object(self, field_name, clazz):
        """ Sets the value of the field to new object of given class """
        
        new_entry = AutomatedObjectEntry(clazz)
        self._current_object().add(field_name, new_entry)
        self._new_current(new_entry)
    
    def end_object(self):
        """ Ends to build current object and goes back to previous one """
        
        self._rollback_current()
    
    def printit(self):
        """ Just prints the currently collected structure """
        
        self._print_entry(self.object, 0)
    
    def _print_entry(self, entry, padding = 0):
        """ Prints the entry and its subentries """
        
        print(("\t" * padding) + entry.clazz)
        for field_name, field_value in entry.fields.items():
            if isinstance(field_value, AutomatedObjectEntry):
                print(("\t" * (padding + 1)) + field_name + " := ...")
                self._print_entry(field_value, padding + 2)
            else:
                print(("\t" * (padding + 1)) + field_name + " := " + str(field_value))
    
################################################################################
    
 