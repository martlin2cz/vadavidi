"""
The module responsible for the manipulating with the objects. Specifies the 
base APIs.
"""
from abc import abstractmethod, ABC
from dataclasses import dataclass

################################################################################
NO_VALUE = object()
################################################################################
################################################################################
class BaseValueObtainer(ABC):
    """ The general obtainer of one value of the field. Can be both expression 
    or the specification what may be obtained from the user (and how)."""
    
    pass

################################################################################
@dataclass
class AbstractValuePrompter(BaseValueObtainer, ABC):
    """ The obtainer, which asks the user for the value. """
    
    prompt_text: str

################################################################################
@dataclass
class AbstractConfirmingPrompter(AbstractValuePrompter, ABC):
    """ The prompter which just asks user for confirmation, or, potentionally,
    allowing to interrupt the chain. Could not have no value at all. """
    
    pass
################################################################################
@dataclass
class AbstractValueExpression(BaseValueObtainer, ABC):
    """ The obtainer, which just somehow produces the value without user 
    interaction. """
    
    pass

################################################################################
################################################################################
class BaseObjectSchemater(ABC):
    """ Obtains the expected structure of the object to be constructed. """
    
    
    @abstractmethod
    def list_impls(self, clazz):
        """ Lists subclasses """
        
    @abstractmethod
    def list_fields(self, clazz):
        """ Lists the fields of that class as dict of ValueObtainers """
        
################################################################################
################################################################################
class BaseObjectBuilder(ABC):
    """ The object builder. Methods new_object, new_list and new_dict switches 
    to new entry (initial is no entry). Methods end_object, end_list 
    and end_dict respectivelly, returns to previous entry.
    
    When current entry is object, add_value is allowed and switches to field 
    entry. If current entry is list entry, add_list_item is allowed and switches
    Finally, if current entry is dict, add_dict_key and add_dict_value 
    (in this particular order) are suported and switches to dict key entry and 
    dict value entry respectivelly.
    
    When current entry is field name, list item or dict key/value entry, 
    set_value may be then called. It automatically switches back to 
    object/list/dict entry then. """
    
    @abstractmethod
    def set_value(self, value):
        """ Adds the (native) value to the current entry """

################################################################################
    @abstractmethod
    def new_object(self, clazz):
        """ Sets the current to the new object (of given clazz) entry """
    
    @abstractmethod
    def add_field(self, field_name):
        """ Sets the current to the new object field entry """

    @abstractmethod
    def end_object(self):
        """ Ends current object entry and goes back to previous one """

################################################################################
    @abstractmethod
    def new_list(self):
        """ Sets the current entry to the new list """

    @abstractmethod
    def add_list_item(self):
        """ Sets the current entry to the list item """

    @abstractmethod            
    def end_list(self):
        """ Ends the current list and goes back to previous """

################################################################################

    @abstractmethod
    def new_dict(self):
        """ Sets the current entry to the new dict """

    @abstractmethod
    def add_dict_key(self):
        """ Sets current entry to the dict key entry """

    @abstractmethod        
    def add_dict_value(self):
        """ Sets current entry to the dict value entry  """
        
    @abstractmethod
    def end_dict(self):
        """ Ends the current dict and goes back to previous """

################################################################################

    @abstractmethod
    def printit(self):
        """ Just prints the currently collected structure """
        
################################################################################
class BaseObjectPrompter(ABC):
    """ The whole big object prompter. Lists all the particilar prompters and
    collects the values obtained by user. At the end, the complete object may be
    obtainable. """
    
    
    @abstractmethod
    def to_next(self):
        """ Returns the next prompter """
        
    @abstractmethod
    def specify_value(self, value):
        """ Saves the given value and modifies the prompters chain regardin to 
        that value """
        
