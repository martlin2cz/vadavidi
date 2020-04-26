"""
The base module of the displayers. The displayers are responsible for showing
the resulting table to the user as a chart. Via the GUI or not (rendered to 
file).
"""
from dataclasses import dataclass
from builtins import str


################################################################################
@dataclass
class BaseSeriesStyle:
    """ The general style of the chart series. Extend to add particular 
    implementation/char kind specific fields. """
    
################################################################################
class StyleBuilder:
    """ An utility to simplify the construction of the style settings. """
    
    style: BaseSeriesStyle
    
    def __init__(self, clazz):
        """ Creates builder for given clazz """
    
        self.style = clazz()
        
    def set(self, property_name, property_value):
        """ Sets the value of the field """
        
        if property_name not in dir(self.style):
            raise ValueError("Not a field: " + property_name)
        
        self.style.__setattr__(property_name, property_value)
        return self
    
    def sets(self, **properties):
        """ Sets the values of the fields """
        
        for name, value in properties.items():
            self.set(name, value)
        return self

    def build(self):
        """ Returns the built instance """
        
        return self.style
    

################################################################################
#TODO the base displayer class
