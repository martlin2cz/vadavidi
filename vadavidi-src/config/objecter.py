"""
The module responsible for the manipulating with the objects.
"""
################################################################################
from collections import deque
from dataclasses import dataclass
from docutils.nodes import field_name
from typing import Mapping, Any, Deque


################################################################################
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
        
    def __hash__(self):
        return 13 * id(self)
    
    def __eq__(self, another):
        return self == another

################################################################################
@dataclass
class DictItemEntry:
    """ The entry of the built dict. Just temporar. """
    key: Any
    value: Any
    
    def __init__(self):
        self.key = None
        self.value = None
    
    def add(self, value):
        """ Adds the given value to this entry (as a key or value) """
        
        if self.key is None:
            self.key = value
            return
            
        if self.value is None:
            self.value = value
            return
            
        raise ValueError("The dict item has already key and value")

################################################################################
class AutomatedObjectBuilder:
    """ An builder of the objects. See the test to see how to use. """
    
    object: AutomatedObjectEntry
    stack: Deque[AutomatedObjectEntry] = {}
    
    def __init__(self, clazz):
        self.object = AutomatedObjectEntry(clazz)
        self.stack = deque([self.object])
    
    def _add_to_current(self, value):
        """ Adds the value to the current entry """
        
        if self._is_current(AutomatedObjectEntry):
            raise ValueError("First specify field name")
        
        elif self._is_current(DictItemEntry):
            self._current_entry().add(value)
        
        elif self._is_current(list):
            self._current_entry().append(value)

        elif self._is_current(dict):
            pass # let if fail
        
        elif self._is_current(str):
            field_name = self._rollback_current(str)
            self._check_current(AutomatedObjectEntry)
            self._current_entry().add(field_name, value)
        
        else:    
            raise ValueError("Invalid current top " + \
                             str(self._current_entry()))
               
    
    def _new_current(self, new_entry):
        """ Marks the given entry to be current """
        
        return self.stack.append(new_entry)
    
    def _rollback_current(self, expected_type):
        """ Returns to previous current entry. Checks currrent type before """
        
        self._check_current(expected_type)
        return self.stack.pop()
        
    def _current_entry(self):
        """ Returns the current entry """
        
        return self.stack[-1]
    
    def _check_current(self, expected_type):
        """ Checks whether the current entry is of given type, fails if not """
        
        if not self._is_current(expected_type):
            raise ValueError("Expected {0} to be on top, but is {1}"
                             .format(expected_type, self._current_entry()))    

    
    def _is_current(self, the_type):
        """ Returns true if current entry is of given type """
        
        current = self._current_entry()
        return isinstance(current, the_type)

################################################################################

    def set_value(self, value):
        """ Adds the (native) value to the current entry """

        self._add_to_current(value)
        
################################################################################
    def new_object(self, clazz):
        """ Sets the current to the new object (of given clazz) entry """
        
        new_entry = AutomatedObjectEntry(clazz)
        self._add_to_current(new_entry)
        self._new_current(new_entry)

        return self
    
    def add_field(self, field_name):
        """ Sets the current to the new object field entry """
    
        self._check_current(AutomatedObjectEntry)

        new_entry = field_name
        self._new_current(new_entry)
        
        return self

    def end_object(self):
        """ Ends current object entry and goes back to previous one """
        
        self._rollback_current(AutomatedObjectEntry)
        
        return self

################################################################################
    
    def new_list(self):
        """ Sets the current entry to the new list """
        
        new_entry = []
        self._add_to_current(new_entry)
        self._new_current(new_entry)
        
        return self
        
    def add_list_item(self):
        """ Sets the current entry to the list item """
        
        self._check_current(list)
        
        # okay, just let the set_value to do the stuff
        return self
            
    def end_list(self):
        """ Ends the current list and goes back to previous """
        
        self._rollback_current(list)
        
        return self

################################################################################

    
    def new_dict(self):
        """ Sets the current entry to the new dict """
        
        new_entry = {}
        self._add_to_current(new_entry)
        self._new_current(new_entry)
        
        return self
        
    def add_dict_key(self):
        """ Sets current entry to the dict key entry """
        
        self._check_and_finish_dict_item()
        self._check_current(dict)
        
        new_entry = DictItemEntry()
        self._new_current(new_entry)
        
        return self
        
    def add_dict_value(self):
        """ Sets current entry to the dict value entry  """
        
        self._check_current(DictItemEntry)
        # okay, let it add
        
        return self
        
    def end_dict(self):
        """ Ends the current dict and goes back to previous """
        
        self._check_and_finish_dict_item()
                
        self._rollback_current(dict)
        
        return self
        
    def _check_and_finish_dict_item(self):
        """ Checks whether the current is dict item, and if so replaces it by
        normal key-value item """
        
        if self._is_current(DictItemEntry):
            entry = self._rollback_current(DictItemEntry)
            self._current_entry()[entry.key] = entry.value
            
################################################################################

################################################################################

    def printit(self):
        """ Just prints the currently collected structure """
        
        self._print_entry(self.object, 0)
    
    def _print_entry(self, entry, padding = 0, is_field_name = False):
        """ Prints the entry and its subentries """
        
        if isinstance(entry, AutomatedObjectEntry):
            print(("\t" * padding) + "new " + entry.clazz + ":")
            for fn, fv in entry.fields.items():
                self._print_entry(fn, padding + 1, True)
                self._print_entry(fv, padding + 2)
        
        elif isinstance(entry, DictItemEntry):
            print(("\t" * padding) + "key   " + entry.key + ",")
            print(("\t" * padding) + "value " + entry.value+ ";")
        
        elif isinstance(entry, list):
            print(("\t" * padding) + "list of:")
            for item in entry:
                self._print_entry(item, padding + 2)
                
        elif isinstance(entry, dict):
            print(("\t" * padding) + "dict of:")
            for key, val in entry.items():
                self._print_entry(key, padding + 1)
                self._print_entry(val, padding + 2)
        
        elif isinstance(entry, str) and is_field_name:
            print(("\t" * padding) + " - " + entry + ":")
            
        else:
            print(("\t" * padding)  + str(entry))
            
#           raise ValueError("Unknown entry: " + str(entry))
################################################################################
    
