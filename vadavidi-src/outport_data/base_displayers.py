"""
The base module of the displayers. The displayers are responsible for showing
the resulting table to the user as a chart. Via the GUI or not (rendered to 
file).
"""
from dataclasses import dataclass
from builtins import str

################################################################################
LINE = "line"
DOTTED = "dotted"
SCATTER = "scatter"
BAR = "bar"
PIE = "pie"


################################################################################
@dataclass
class SeriesStyle:
    # the kind of the chart (line, dotted, scatter, bar)
    kind: str
    # the color
    color: str
    # the width
    width: float
    # the line style (solid, dashed, dotted, none)
    style: str
    # the markers style (none, circles, squares, triangles)
    markers: str
    
    


################################################################################

