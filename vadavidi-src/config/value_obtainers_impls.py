"""
The implementation of the ValueObtainers.
"""
from dataclasses import dataclass

from config.base_objecter import AbstractValuePrompter, BaseValueObtainer
from typing import List, Mapping

################################################################################
@dataclass
class SimpleValuePrompter(AbstractValuePrompter):
    """ The obtainer which need to get one simple single value known from 
    the user. """

    # the human readable prompt text
    prompt_text: str
    # the type of the prompted value
    type: str
    
################################################################################
@dataclass
class ObjectConstructionPrompter(AbstractValuePrompter):
    """ The main prompter for the object construction. """
    
    clazz: str
    prompt_text: str
    
################################################################################
@dataclass
class ClassChoosePrompter(AbstractValuePrompter):
    """ The obtainer which lets the user to choose the particular class. """

    clazz: str
    prompt_text: str

################################################################################
@dataclass
class ListPrompter(AbstractValuePrompter):
    """ The obtainer which need to get list of values from the user. """
    # the human readable prompt text
    prompt_text: str
    # the obtainer for the particular items
    item_prompter: BaseValueObtainer
    
################################################################################
@dataclass
class DictPrompter(AbstractValuePrompter):
    """ The obtainer which need to get dict of values from the user. """
 
    # the human readable prompt text
    prompt_text: str
    # the obtainer for the particular items keys
    key_prompter: BaseValueObtainer
    # the obtainer for the particular items values
    value_prompter: BaseValueObtainer
