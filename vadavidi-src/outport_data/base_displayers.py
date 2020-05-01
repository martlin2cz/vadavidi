"""
The base module of the displayers. The displayers are responsible for showing
the resulting table to the user as a chart. Via the GUI or not (rendered to 
file).
"""
from abc import abstractmethod, ABC
from builtins import str, staticmethod
from dataclasses import dataclass


################################################################################
@dataclass
class BaseSeriesStyle:
    """ The general style of the chart series. Extend to add particular 
    implementation/char kind specific fields. """
    
    @staticmethod
    def create(clazz, **values):
        """ Creates the style with given class and properties values """
        
        style = clazz()
        
        for name, value in values.items():
            style.__setattr__(name, value)
            
        return style
    
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
class BaseDisplayer(ABC):
    """ The base displayer. Resposinble for displaying, showing chart of the
    table. Typically, the one field of the table is choosen as a x-value, others
    are shown as the series. """
    
    @abstractmethod
    def show(self, dataset_name, result, x_axis_name, series_names, styles):
        """ Shows the specified series of the given result table. """
