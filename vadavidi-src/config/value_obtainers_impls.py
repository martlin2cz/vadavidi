"""
The implementation of the ValueObtainers.
"""
from dataclasses import dataclass

from config.base_objecter import BaseValueObtainer

################################################################################
@dataclass
class SimpleValuePrompter(BaseValueObtainer):
    """ The obtainer which need to get one simple single value known from 
    the user. """

    # the human readable prompt text
    prompt_text: str
    # the type of the prompted value
    type: str
    
################################################################################
@dataclass
class ListPrompter(BaseValueObtainer):
    """ The obtainer which need to get list of values from the user. """

    # the human readable prompt text
    prompt_text: str
    # the obtainer for the particular items
    item_prompter: BaseValueObtainer
